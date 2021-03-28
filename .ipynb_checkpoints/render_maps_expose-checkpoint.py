# tested with blender 2.79
# OSX: /Applications/Blender/blender.app/Contents/MacOS/blender base_expose.blend --background --python render_maps_expose.py 
# sensei: blender base_expose.blend --background --python render_maps_expose.py 


import sys
sys.path.append('/opt/conda/envs/repose/lib/python3.6/site-packages')
sys.path.append('/opt/conda/envs/repose/lib/python3.6/lib-dynload')
sys.path.append('/opt/conda/envs/repose/lib/python3.6')
sys.path.append('/opt/conda/envs/repose/lib/python36.zip')

import bpy
import os
cwd = os.getcwd()

sys.path.append(cwd)

import config_expose
target_folder = cwd + '/' + config_expose.target_folder

# source
file_path_source_obj = target_folder + config_expose.file_path_source_obj
file_path_source_cam = target_folder + config_expose.file_path_source_cam
old_objs = set(bpy.context.scene.objects)
bpy.ops.import_mesh.ply(filepath = file_path_source_obj)
imported_objs = set(bpy.context.scene.objects) - old_objs
obj1_name = list(imported_objs)[0].name
source_img_res_x = config_expose.source_img_res_x
source_img_res_y = config_expose.source_img_res_y
cam_sou_focal_length_in_px = config_expose.cam_sou_focal_length_in_px
cam_sou_sensor_width = config_expose.cam_sou_sensor_width
cam_sou_center_0 = config_expose.cam_sou_center_0
cam_sou_center_1 = config_expose.cam_sou_center_1
ob1 = bpy.data.objects[obj1_name]
me1 = ob1.data
ob1.rotation_euler[0] = 0

for scene in bpy.data.scenes:
    scene.render.resolution_x = source_img_res_x
    scene.render.resolution_y = source_img_res_y

bpy.data.objects['Camera_sou'].location[0] = 0
bpy.data.objects['Camera_sou'].location[1] = 0
bpy.data.objects['Camera_sou'].location[2] = 0
bpy.data.objects['Camera_sou'].rotation_euler[0] = 3.1415926
bpy.data.objects['Camera_sou'].rotation_euler[1] = 0
bpy.data.objects['Camera_sou'].rotation_euler[2] = 0

bpy.data.cameras['Camera_sou'].lens = float(cam_sou_focal_length_in_px) * float(cam_sou_sensor_width) / float(max((source_img_res_x,source_img_res_y)))
bpy.data.cameras['Camera_sou'].sensor_width = float(cam_sou_sensor_width)

bpy.data.cameras['Camera_sou'].shift_x = -(float(cam_sou_center_0) - float(source_img_res_x)/2.) / float(max((source_img_res_x,source_img_res_y)))
bpy.data.cameras['Camera_sou'].shift_y = (float(cam_sou_center_1) - float(source_img_res_y)/2.) / float(max((source_img_res_x,source_img_res_y)))

scene.camera = bpy.data.objects['Camera_sou']
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.filepath = target_folder+config_expose.file_path_source_obj+'_source_expose.png'
bpy.ops.render.render(write_still=True, use_viewport=True)


bpy.data.objects[obj1_name].hide=True
bpy.data.objects[obj1_name].hide_render=True


# target
file_path_target_obj = target_folder + config_expose.file_path_target_obj
file_path_target_cam = target_folder + config_expose.file_path_target_cam
old_objs = set(bpy.context.scene.objects)
bpy.ops.import_mesh.ply(filepath = file_path_target_obj)
imported_objs = set(bpy.context.scene.objects) - old_objs
obj2_name = list(imported_objs)[0].name
target_img_res_x = config_expose.target_img_res_x
target_img_res_y = config_expose.target_img_res_y
cam_tar_focal_length_in_px = config_expose.cam_tar_focal_length_in_px
cam_tar_sensor_width = config_expose.cam_tar_sensor_width
cam_tar_center_0 = config_expose.cam_tar_center_0
cam_tar_center_1 = config_expose.cam_tar_center_1
ob2 = bpy.data.objects[obj2_name]
me2 = ob2.data
ob2.rotation_euler[0] = 0

for scene in bpy.data.scenes:
    scene.render.resolution_x = target_img_res_x
    scene.render.resolution_y = target_img_res_y

bpy.data.objects['Camera_tar'].location[0] = 0
bpy.data.objects['Camera_tar'].location[1] = 0
bpy.data.objects['Camera_tar'].location[2] = 0
bpy.data.objects['Camera_tar'].rotation_euler[0] = 3.1415926
bpy.data.objects['Camera_tar'].rotation_euler[1] = 0
bpy.data.objects['Camera_tar'].rotation_euler[2] = 0

bpy.data.cameras['Camera_tar'].lens = float(cam_tar_focal_length_in_px) * float(cam_tar_sensor_width) / float(max((target_img_res_x,target_img_res_y)))
bpy.data.cameras['Camera_tar'].sensor_width = float(cam_tar_sensor_width)

bpy.data.cameras['Camera_tar'].shift_x = -(float(cam_tar_center_0) - float(target_img_res_x)/2.) / float(max((target_img_res_x,target_img_res_y)))
bpy.data.cameras['Camera_tar'].shift_y = (float(cam_tar_center_1) - float(target_img_res_y)/2.) / float(max((target_img_res_x,target_img_res_y)))

scene.camera = bpy.data.objects['Camera_tar']
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.filepath = target_folder+config_expose.file_path_target_obj+'_target_expose.png'
bpy.ops.render.render(write_still=True, use_viewport=True)



#####render done

offset3 = [ [0]*3 for i in range(len(me1.vertices))]
for i in range(len(me1.vertices)):
    offset3[i][0] = me2.vertices[i].co[0] - me1.vertices[i].co[0]
    offset3[i][1] = me2.vertices[i].co[1] - me1.vertices[i].co[1]
    offset3[i][2] = me2.vertices[i].co[2] - me1.vertices[i].co[2]

offset2 = [ [0]*2 for i in range(len(me1.vertices))]
vis1 = [0]*len(me1.vertices)
vis2 = [0]*len(me2.vertices)

import bmesh
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

scene = bpy.context.scene
cam_sou = bpy.data.objects['Camera_sou']
cam_tar = bpy.data.objects['Camera_tar']
cs, ce = cam_tar.data.clip_start, cam_tar.data.clip_end
mat_world_1 = bpy.data.objects[obj1_name].matrix_world
mat_world_2 = bpy.data.objects[obj2_name].matrix_world
for i in range(len(me1.vertices)):
    co_ndc_1 = world_to_camera_view(scene, cam_sou, mat_world_1 * me1.vertices[i].co)
    co_ndc_2 = world_to_camera_view(scene, cam_tar, mat_world_2 * me2.vertices[i].co)
    if (0.0 < co_ndc_1.x < 1.0 and 0.0 < co_ndc_1.y < 1.0 and cs < co_ndc_1.z <  ce):
        vis1[i] = 1
    if (0.0 < co_ndc_2.x < 1.0 and 0.0 < co_ndc_2.y < 1.0 and cs < co_ndc_2.z <  ce):
        vis2[i] = 1
    offset2[i][0] = co_ndc_2.x - co_ndc_1.x
    offset2[i][1] = co_ndc_2.y - co_ndc_1.y
    
bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
for f in bm.faces:
    for l in f.loops:
        luv = l[uv_layer]
        luv.uv = tuple([offset2[l.vert.index][0]*.2+.5,offset2[l.vert.index][1]*.2+.5])

bmesh.update_edit_mesh(me2)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

mat = bpy.data.materials.get("tex_2")
if ob2.data.materials:
    ob2.data.materials[0] = mat
else:
    ob2.data.materials.append(mat)

scene.camera = bpy.data.objects['Camera_tar']
bpy.data.scenes['Scene'].render.filepath = target_folder+'flowmap_scale_0.2.png'
bpy.ops.render.render(write_still=True, use_viewport=True)


bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
for f in bm.faces:
    for l in f.loops:
        luv = l[uv_layer]
        luv.uv = tuple([offset2[l.vert.index][0]*.4+.5,offset2[l.vert.index][1]*.4+.5])

bmesh.update_edit_mesh(me2)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

mat = bpy.data.materials.get("tex_2")
if ob2.data.materials:
    ob2.data.materials[0] = mat
else:
    ob2.data.materials.append(mat)

scene.camera = bpy.data.objects['Camera_tar']
bpy.data.scenes['Scene'].render.filepath = target_folder+'flowmap_scale_0.4.png'
bpy.ops.render.render(write_still=True, use_viewport=True)


bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
for f in bm.faces:
    for l in f.loops:
        luv = l[uv_layer]
        luv.uv = tuple([offset2[l.vert.index][0]*.8+.5,offset2[l.vert.index][1]*.8+.5])

bmesh.update_edit_mesh(me2)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

mat = bpy.data.materials.get("tex_2")
if ob2.data.materials:
    ob2.data.materials[0] = mat
else:
    ob2.data.materials.append(mat)

scene.camera = bpy.data.objects['Camera_tar']
bpy.data.scenes['Scene'].render.filepath = target_folder+'flowmap_scale_0.8.png'
bpy.ops.render.render(write_still=True, use_viewport=True)


bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
for f in bm.faces:
    for l in f.loops:
        luv = l[uv_layer]
        luv.uv = tuple([offset2[l.vert.index][0]*1.6+.5,offset2[l.vert.index][1]*1.6+.5])

bmesh.update_edit_mesh(me2)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

mat = bpy.data.materials.get("tex_2")
if ob2.data.materials:
    ob2.data.materials[0] = mat
else:
    ob2.data.materials.append(mat)

scene.camera = bpy.data.objects['Camera_tar']
bpy.data.scenes['Scene'].render.filepath = target_folder+'flowmap_scale_1.6.png'
bpy.ops.render.render(write_still=True, use_viewport=True)









from mathutils.bvhtree import BVHTree

bvhtree = BVHTree.FromObject(ob1, bpy.context.scene)
vis1 = [0]*len(me1.vertices)
for i in range(len(me1.vertices)):
    hit_loc = bvhtree.ray_cast(cam_sou.location, me1.vertices[i].co-cam_sou.location)
    if not hit_loc[0]:
        continue
    if (hit_loc[0]-me1.vertices[i].co).length < 1e-5:
        vis1[i] = 1

bpy.context.scene.objects.active = ob2
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me2)
uv_layer = bm.loops.layers.uv.verify()
bm.faces.layers.tex.verify()
tuv_w = [.2,.2]
tuv_b = [.7,.2]

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

scene.camera = bpy.data.objects['Camera_tar']
bpy.data.scenes['Scene'].render.filepath = target_folder+'maskmap.png'
bpy.ops.render.render(write_still=True, use_viewport=True)




    
    
    
    
    