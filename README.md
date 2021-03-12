# reposing_render_maps
<img width="600" alt="teaser" src="https://user-images.githubusercontent.com/8480701/110965666-5151ca80-834c-11eb-8112-eaec55b5f82c.png">

render flow map and mask map between source pose and target pose

step 1:

in config.py, update the following:

target_folder = './' #where you want to put the results (flowmap.png, maskmap.png)

file_path_source = './sample_data/hello_smpl_KXRULS.obj' #source body obj

file_path_target = './sample_data/hello_smpl_X0JGKP.obj' #target body obj

step 2:

run blender base.blend --background --python render_maps.py

in OSX, you may want to replace blender with /Applications/Blender/blender.app/Contents/MacOS/blender




