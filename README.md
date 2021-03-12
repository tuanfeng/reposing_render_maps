# reposing_render_maps
<img width="600" alt="teaser" src="https://user-images.githubusercontent.com/8480701/110965666-5151ca80-834c-11eb-8112-eaec55b5f82c.png">

render flow map and mask map between source pose and target pose

step 1:

in config.py, update the following:

target_folder = './' #where you want to put the results (flowmap.png, maskmap.png)

file_path_source_obj = './sample_data/AdobeStock_387107537/000.obj' #smplx obj file
file_path_source_cam = './sample_data/AdobeStock_387107537/000.pkl' #camera estimation from smplifyx
source_img_res_x = 1651
source_img_res_y = 1101

file_path_target_obj = './sample_data/AdobeStock_387107683/000.obj' #smplx obj file
file_path_target_cam = './sample_data/AdobeStock_387107683/000.pkl' #camera estimation from smplifyx
target_img_res_x = 1651
target_img_res_y = 1101

step 2:

the script is based on blender 2.79

run: blender base.blend --background --python render_maps.py

in OSX, you may want to replace blender with /Applications/Blender/blender.app/Contents/MacOS/blender




