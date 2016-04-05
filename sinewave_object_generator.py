#Sine Wave object generator (for use with Blender 2.6 and above)
#May 27, 2015
#Author: Joseph Majesky
#Run via command in terminal: >> blender  --python sinewave.py -- length width frequency amplitude
#For circles do >> blender  --python sinewave.py -- radius frequency amplitude
#length A float between 0 and 5 
#frequency: Any positive float
#radius: Any positive float
#amplitude: a float between 0 and 5

import bpy
import math
from mathutils import Vector
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
import sys

def create_sine_wave(length, width, frequency, amplitude):
    
    #create vertices and edges
    verts = [] 
    edges = []
    faces = []   

    #length ranges from - to + N Pi for the range
    x=-1*length*3.14

    while x< length*3.15:

        #vertices for a step of .001 for a smooth shape.
        
        verts.append(Vector((x, 1*width, amplitude*math.sin(frequency*x))))
        verts.append(Vector((x, -1*width, amplitude*math.sin(frequency*x))))
        verts.append(Vector((x,1*width, -3.0)))
        verts.append(Vector((x,-1*width, -3.0)))
        x=x+.001
        verts.append(Vector((x, 1*width, amplitude*math.sin(frequency*x))))
        verts.append(Vector((x, -1*width, amplitude*math.sin(frequency*x))))
        verts.append(Vector((x,1*width, -3.0)))
        verts.append(Vector((x,-1*width, -3.0)))
        x=x+.001
    
    #nonsense way to make faces by simply connecting the vertices of each step
    
    y=0
    while y< (len(verts)-4):
        
        faces.append([y,y+4,y+5,y+1])
        faces.append([y,y+4,y+6,y+2])
        faces.append([y+1,y+5,y+7,y+3])
        y=y+4 
    
    #faces for ends of object and structure stability
    faces.append([0,1,3,2])
    faces.append([len(verts)-4,len(verts)-3,len(verts)-1,len(verts)-2])
    faces.append([3,2, len(verts)-2,len(verts)-1])
    
    #create the mesh
    mesh = bpy.data.meshes.new("sine_wave")
    mesh.from_pydata(verts,[],faces)

    #create the object
    object = bpy.data.objects.new("sine_wave",mesh)
    object.location = (0,0,0)
    bpy.context.scene.objects.link(object)

    #set active and print for confirmation
    print(bpy.data.objects["sine_wave"])
    bpy.context.scene.objects.active=bpy.data.objects["sine_wave"]
    bpy.ops.object.select_pattern(pattern="sine_wave")



def create_circular_sine_wave(radius, frequency, amplitdue):
     #create vertices and edges
    verts = [] 
    edges = []
    faces = []   

    #work our way out from the center of the circle, calculating the length of the wave at each step
    angle_theta=0.0
    radius=radius*math.pi

    while angle_theta<=(math.pi):

        #Solve for length of the wave and the distance from the edge using trig
        length_of_side= radius * math.sin(angle_theta)
        y=radius*math.cos(angle_theta)

        #calculate vertices
        verts.append(Vector((length_of_side, y , amplitude * math.sin(frequency*y))))
        verts.append(Vector((-length_of_side, y , amplitude*math.sin(frequency*y))))
        verts.append(Vector((length_of_side, y , -amplitdue-1 )))
        verts.append(Vector((-length_of_side, y , -amplitude-1)))

        #step of .001 and repeat for smooth shape 
        angle_theta= angle_theta+.001

     #nonsense way to make faces by simply connecting the vertices of each step
    
    y=0
    while y< (len(verts)-4):
        
        faces.append([y,y+4,y+5,y+1])
        faces.append([y,y+4,y+6,y+2])
        faces.append([y+1,y+5,y+7,y+3])
        faces.append([y+2, y+3, y+7, y+6])
        y=y+4 
    
    #faces for ends of object 
    faces.append([0,1,3,2])
    faces.append([len(verts)-4,len(verts)-3,len(verts)-1,len(verts)-2])
    
    #create the mesh
    mesh = bpy.data.meshes.new("circle_sine_wave")
    mesh.from_pydata(verts,[],faces)

    #create the object
    object = bpy.data.objects.new("circle_sine_wave",mesh)
    object.location = (0,0,0)
    bpy.context.scene.objects.link(object)

    #set active and print for confirmation
    print(bpy.data.objects["circle_sine_wave"])
    bpy.context.scene.objects.active=bpy.data.objects["circle_sine_wave"]
    bpy.ops.object.select_pattern(pattern="circle_sine_wave")


#wrappers for exporting to STL files
def rectangle_export_to_stl(lenl, wid, freq, amp):
    bpy.ops.export_mesh.stl(filepath="Sine_Curve_Len_"+ lenl+ "_Wid_"+wid+"_Freq_"+ freq+"_Amp_" + amp+ ".stl",
    check_existing=False,
    ascii=False) 

def circle_export_to_stl(rad, freq, amp):
    bpy.ops.export_mesh.stl(filepath="Sine_Curve_Rad_"+ rad +"_Freq_"+ freq+"_Amp_" + amp+ ".stl",
    check_existing=False,
    ascii=False) 

#other helper methods
def display_help():
    print("usage:")
    print(" Rectangular Shapes: \n >> blender --python sinewave_object_generator.py --  -r length width frequency amplitude")
    print(" Circular Shapes: \n >> blender --python sinewave_object_generator.py -- -c radius frequency amplitude")
    
def clear_objects():
    objcts=[objct.name for objct in bpy.data.objects if objct.type=="MESH"]

    for objct in objcts:
        bpy.data.objects[objct].select =True

    bpy.ops.object.delete()

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


#main logic of program 

#Prepare file

clear_objects()

#if no command line args, do a 1 by 1 by 1 by 1 rectangle and print help message

if len(sys.argv)!= 7 and len(sys.argv) !=8:
    create_sine_wave(1, 1, 1,1)
    rectangle_export_to_stl( "1","1", "1", "1")

    display_help()

    # else read as length&width or radius of object, frequency of wave, and amplitude of wave
elif len(sys.argv)==7 and sys.argv[3]=="-c":
    radius=float(sys.argv[5])
    frequency = float(sys.argv[6])
    amplitude = float(sys.argv[7])

    #Create wave and export it to stl
    create_circular_sine_wave(radius, frequency, amplitude)
    circle_export_to_stl(sys.argv[5], sys.argv[6], sys.argv[7])

elif len(sys.argv)==9 and sys.argv[4]=="-r":


    length= float(sys.argv[5])
    width = float(sys.argv[6])
    frequency = float(sys.argv[7])
    amplitude = float(sys.argv[8])
    
    #Create wave and export it to stl
    create_sine_wave(length, width, frequency, amplitude)
    rectangle_export_to_stl(sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])

else: #print help message
    display_help()