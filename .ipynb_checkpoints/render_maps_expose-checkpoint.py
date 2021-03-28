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







