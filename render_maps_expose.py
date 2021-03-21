# tested with blender 2.79
# OSX: /Applications/Blender/blender.app/Contents/MacOS/blender base_expose.blend --background --python render_maps_expose.py 


import bpy
import os
cwd = os.getcwd()
import sys

#cwd = '/Users/yangtwan/OneDrive - Adobe/adobe_projects/reposing/reposing_render_maps/'

sys.path.append(cwd)

import config_expose
target_folder = cwd + '/' + config_expose.target_folder
file_path_source_obj = cwd + '/' + config_expose.file_path_source_obj
file_path_source_cam = cwd + '/' + config_expose.file_path_source_cam

# source
old_objs = set(bpy.context.scene.objects)
bpy.ops.import_mesh.ply(filepath = file_path_source_obj)
imported_objs = set(bpy.context.scene.objects) - old_objs
obj1_name = list(imported_objs)[0].name
source_img_res_x = config_expose.source_img_res_x
source_img_res_y = config_expose.source_img_res_y

import numpy as np
cam_sou = np.load(file_path_source_cam,allow_pickle=True)

ob1 = bpy.data.objects[obj1_name]
me1 = ob1.data
ob1.rotation_euler[0] = 0

#bpy.data.objects[obj2_name].hide=True
#bpy.data.objects[obj2_name].hide_render=True

for scene in bpy.data.scenes:
    scene.render.resolution_x = source_img_res_x
    scene.render.resolution_y = source_img_res_y

bpy.data.objects['Camera_sou'].location[0] = 0
bpy.data.objects['Camera_sou'].location[1] = 0
bpy.data.objects['Camera_sou'].location[2] = 0
bpy.data.objects['Camera_sou'].rotation_euler[0] = np.pi
bpy.data.objects['Camera_sou'].rotation_euler[1] = 0
bpy.data.objects['Camera_sou'].rotation_euler[2] = 0

bpy.data.cameras['Camera_sou'].lens = float(cam_sou['focal_length_in_px']) * float(cam_sou['sensor_width']) / float(np.max((source_img_res_x,source_img_res_y)))
bpy.data.cameras['Camera_sou'].sensor_width = float(cam_sou['sensor_width'])

bpy.data.cameras['Camera_sou'].shift_x = -(float(cam_sou['center'][0]) - float(source_img_res_x)/2.) / float(np.max((source_img_res_x,source_img_res_y)))
bpy.data.cameras['Camera_sou'].shift_y = (float(cam_sou['center'][1]) - float(source_img_res_y)/2.) / float(np.max((source_img_res_x,source_img_res_y)))

scene.camera = bpy.data.objects['Camera_sou']
bpy.data.scenes['Scene'].render.resolution_percentage = 100
bpy.data.scenes['Scene'].render.filepath = target_folder+'source_expose.png'
bpy.ops.render.render(write_still=True, use_viewport=True)




