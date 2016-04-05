# Shape-key Distortion-Renderer: Joseph Majesky
# Input: an active blender mesh withb two shape-keys, one denoted as 'a'
# and the other denoted as 'z'
# Output: 100 Rendered image files of the shapekey's at varying levels,
# generated through iteration
# Special Notes: Before running, make sure the blender camera and lightsource
# are positioned correctly for your
# needs. Also, make sure the object you want warped is selected and active.
# ____________________Running the script___________________________________
# Open a blender project. Create two separate shapekeys for the model
# that will be warped, named 'a' and 'z'. Open this script via the scripting
# interface. Select the model to be warped, and run the script.
import bpy
# Grab the selected mesh
mesh = bpy.context.object.data

# Set both shapekeys to 0 to start
mesh.shape_keys.key_blocks['z'].value = .0
mesh.shape_keys.key_blocks['a'].value = .0
mesh.shape_keys.key_blocks['z'].keyframe_insert(data_path="value")
mesh.shape_keys.key_blocks['a'].keyframe_insert(data_path="value")

# Cycle through shapekey a
a = 0.0
while a <= 1.0:
    mesh.shape_keys.key_blocks['a'].value = a
    mesh.shape_keys.key_blocks['a'].keyframe_insert(data_path="value")
    z = 0.0
    # Cycle through shapekey z
    while z <= 1.0:
        mesh.shape_keys.key_blocks['z'].value = z
        mesh.shape_keys.key_blocks['z'].keyframe_insert(data_path="value")
        bpy.data.scenes["Scene"].render.filepath = '/Warps/plant_' + str(a) + \
            '_' + str(z) + '.jpg'
        bpy.ops.render.render(write_still=True)
        z += 0.1
    a += 0.1
# Exit iterations
