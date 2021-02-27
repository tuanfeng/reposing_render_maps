# reposing_render_maps

![source](https://user-images.githubusercontent.com/8480701/109393387-3d07d980-7919-11eb-85c7-6566844d879c.png)
![target](https://user-images.githubusercontent.com/8480701/109393388-3d07d980-7919-11eb-8d4c-154af52d40b6.png)
![flowmap](https://user-images.githubusercontent.com/8480701/109393384-38432580-7919-11eb-8fe9-197026be0f27.png)
![maskmap](https://user-images.githubusercontent.com/8480701/109393385-39745280-7919-11eb-9c45-6e568f311516.png)

render flow map and mask map between source pose and target pose

step 1:

in config.py, update the following:

target_folder = './' #where you want to put the results (flowmap.png, maskmap.png)

file_path_source = './sample_data/hello_smpl_KXRULS.obj' #source body obj

file_path_target = './sample_data/hello_smpl_X0JGKP.obj' #target body obj

step 2:

run blender base.blend --background --python render_maps.py

in OSX, you may want to replace blender with /Applications/Blender/blender.app/Contents/MacOS/blender




