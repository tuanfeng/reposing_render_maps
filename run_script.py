import os
import glob
import numpy as np
from PIL import Image

bf = "../deepfashion_dataset/deepfashion_pair/"
lst = sorted(glob.glob(bf+'*'))

for idx in lst:
    t1 = idx.rfind('/')
    t2 = idx.rfind('jpg_')
    p1 = idx[t1+1:t2+3]
    p2 = idx[t2+4:]
    c1 = np.load(idx+'/'+p1+'_params.npz',allow_pickle=True)
    c2 = np.load(idx+'/'+p2+'_params.npz',allow_pickle=True)
    im1 = Image.open(idx+'/'+p1)
    im2 = Image.open(idx+'/'+p2)
    f = open("config_expose.py", "w")
    f.write("target_folder = \'"+idx+"/\'\n")
    f.write("file_path_source_obj = '"+p1+".ply'\n")
    f.write("file_path_source_cam = '"+p1+"_params.npz'\n")
    f.write("source_img_res_x = "+str(im1.size[0])+'\n')
    f.write("source_img_res_y = "+str(im1.size[1])+'\n')
    f.write("cam_sou_focal_length_in_px = "+str(c1['focal_length_in_px'])+'\n')
    f.write("cam_sou_sensor_width = "+str(c1['sensor_width'])+'\n')
    f.write("cam_sou_center_0 = "+str(c1['center'][0])+'\n')
    f.write("cam_sou_center_1 = "+str(c1['center'][1])+'\n')
    f.write("file_path_target_obj = '"+p2+".ply'\n")
    f.write("file_path_target_cam = '"+p2+"_params.npz'\n")
    f.write("target_img_res_x = "+str(im2.size[0])+'\n')
    f.write("target_img_res_y = "+str(im2.size[1])+'\n')
    f.write("cam_tar_focal_length_in_px = "+str(c2['focal_length_in_px'])+'\n')
    f.write("cam_tar_sensor_width = "+str(c2['sensor_width'])+'\n')
    f.write("cam_tar_center_0 = "+str(c2['center'][0])+'\n')
    f.write("cam_tar_center_1 = "+str(c2['center'][1])+'\n')    
    f.close()
    bashCommand = "blender base_expose.blend --background --python render_maps_expose.py"
    os.system(bashCommand)
    







