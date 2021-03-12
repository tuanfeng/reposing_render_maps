# OSX
# /Applications/Blender/blender.app/Contents/MacOS/blender base.blend --background --python render_maps.py 


import bpy
import os
cwd = os.getcwd()
import sys

sys.path.append(cwd)

import config
target_folder = cwd + '/' + config.target_folder
file_path_source_obj = cwd + '/' + config.file_path_source_obj
file_path_source_cam = cwd + '/' + config.file_path_source_cam

file_path_target_obj = cwd + '/' + config.file_path_target_obj
file_path_target_cam = cwd + '/' + config.file_path_target_cam

#for o in bpy.context.scene.objects:
#    if o.type == 'MESH':
#        o.select = True
#    else:
#        o.select = False
# bpy.ops.object.delete()

# source
old_objs = set(bpy.context.scene.objects)
bpy.ops.import_scene.obj(filepath = file_path_source_obj, split_mode='OFF')
imported_objs = set(bpy.context.scene.objects) - old_objs
obj1_name = list(imported_objs)[0].name
source_img_res_x = config.source_img_res_x
source_img_res_y = config.source_img_res_y

#target
old_objs = set(bpy.context.scene.objects)
bpy.ops.import_scene.obj(filepath = file_path_target_obj, split_mode='OFF')
imported_objs = set(bpy.context.scene.objects) - old_objs
obj2_name = list(imported_objs)[0].name
target_img_res_x = config.target_img_res_x
target_img_res_y = config.target_img_res_y

import numpy as np
cam_sou = np.load(file_path_source_cam,allow_pickle=True)
cam_tar = np.load(file_path_target_cam,allow_pickle=True)


for scene in bpy.data.scenes:
    scene.render.resolution_x = target_img_res_x
    scene.render.resolution_y = target_img_res_y

bpy.data.objects['Camera'].location[0]= -cam_tar['camera_translation'][0][0]
bpy.data.objects['Camera'].location[1]= -cam_tar['camera_translation'][0][2]
bpy.data.objects['Camera'].location[2]= cam_tar['camera_translation'][0][1]
bpy.data.objects['Camera'].rotation_euler[0]=np.pi/2
bpy.data.objects['Camera'].rotation_euler[1]=0
bpy.data.objects['Camera'].rotation_euler[2]=0

ob1 = bpy.data.objects[obj1_name]
me1 = ob1.data
ob2 = bpy.data.objects[obj2_name]
me2 = ob2.data

#ob1.rotation_euler[0] = 0
#ob2.rotation_euler[0] = 0

import numpy as np
offset3 = np.zeros((len(me1.vertices),3))

for i in range(len(me1.vertices)):
    offset3[i,0] = me2.vertices[i].co[0] - me1.vertices[i].co[0]
    offset3[i,1] = me2.vertices[i].co[1] - me1.vertices[i].co[1]
    offset3[i,2] = me2.vertices[i].co[2] - me1.vertices[i].co[2]

offset2 = np.zeros((len(me1.vertices),2))
vis1 = np.zeros((len(me1.vertices),1))
vis2 = np.zeros((len(me2.vertices),1))

import bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

scene = bpy.context.scene
cam = bpy.data.objects['Camera']
cs, ce = cam.data.clip_start, cam.data.clip_end
mat_world_1 = bpy.data.objects[obj1_name].matrix_world
mat_world_2 = bpy.data.objects[obj2_name].matrix_world
for i in range(len(me1.vertices)):
    co_ndc_1 = world_to_camera_view(scene, cam, mat_world_1 * me1.vertices[i].co)
    co_ndc_2 = world_to_camera_view(scene, cam, mat_world_2 * me2.vertices[i].co)
    if (0.0 < co_ndc_1.x < 1.0 and 0.0 < co_ndc_1.y < 1.0 and cs < co_ndc_1.z <  ce):
        vis1[i] = 1
    if (0.0 < co_ndc_2.x < 1.0 and 0.0 < co_ndc_2.y < 1.0 and cs < co_ndc_2.z <  ce):
        vis2[i] = 1
    offset2[i,0] = co_ndc_2.x - co_ndc_1.x
    offset2[i,1] = co_ndc_2.y - co_ndc_1.y


bpy.data.objects[obj1_name].hide=True
bpy.data.objects[obj1_name].hide_render=True


from random import random
bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
for f in bm.faces:
    for l in f.loops:
        luv = l[uv_layer]
        luv.uv = tuple(offset2[l.vert.index]*1+.5)

bmesh.update_edit_mesh(me2)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.shade_smooth()


mat = bpy.data.materials.get("tex_2")
if ob2.data.materials:
    ob2.data.materials[0] = mat
else:
    ob2.data.materials.append(mat)

bpy.data.scenes['Scene'].render.filepath = target_folder+'flowmap.png'
bpy.ops.render.render(write_still=True, use_viewport=True)




from mathutils.bvhtree import BVHTree

bvhtree = BVHTree.FromObject(ob1, bpy.context.scene)
vis1 = np.zeros((len(me1.vertices),1))
for i in range(len(me1.vertices)):
    hit_loc = bvhtree.ray_cast(cam.location, me1.vertices[i].co-cam.location)
    if not hit_loc[0]:
        continue
    if (hit_loc[0]-me1.vertices[i].co).length < 1e-3:
        vis1[i] = 1



from random import random
bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
tuv_w = .2 * np.ones((2,1))
tuv_b = .2 * np.ones((2,1));tuv_b[1,0] = .7

for f in bm.faces:
    for l in f.loops:
        luv = l[uv_layer]
        if vis1[l.vert.index] == 1:
            luv.uv = tuple(tuv_w)
        else:
            luv.uv = tuple(tuv_b)            
        

bmesh.update_edit_mesh(me2)
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.shade_smooth()


mat = bpy.data.materials.get("tex_1")
if ob2.data.materials:
    ob2.data.materials[0] = mat
else:
    ob2.data.materials.append(mat)

bpy.data.scenes['Scene'].render.filepath = target_folder+'maskmap.png'
bpy.ops.render.render(write_still=True, use_viewport=True)





