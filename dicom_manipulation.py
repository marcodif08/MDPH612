import pydicom as dicom
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import imageio
import os

#if you want to run the methods individually, here are some of the paths from the 3 DICOM files provided with code
#Abdomen structure_path = './Abdomen/RS.PYTIM05_.dcm' beam_path = './Abdomen/RP.PYTIM05_PS2.dcm'
#ENT structure_path = './ENT/RS.1.2.246.352.71.4.2088656855.2401823.20110920093221.dcm' beam_path = './ENT/RP.1.2.246.352.71.5.2088656855.377514.20110921073559.dcm'
#Prostate structure_path = './Prostate/RS.1.2.246.352.71.4.2088656855.2404649.20110920153449.dcm' beam_path = './Prostate/RP.1.2.246.352.71.5.2088656855.377401.20110920153647.dcm'


#This gets the 3D data of the contours in question and saves the data as a csv of [x,y,z] triplets
def get3DData(path):
    #reads structure file
    rt_struct = dicom.dcmread(path)

    #body contour data
    #Abdomen ROIContourSequence[3]
    #ENT ROIContourSequence[0]
    #Prostate ROIContourSequence[0]
    num_slices = len(rt_struct.ROIContourSequence[0].ContourSequence)

    x = []
    y = []
    z = []
    for i in range (0,num_slices):
        this_slice = rt_struct.ROIContourSequence[0].ContourSequence[i].ContourData
        counter = 0
        while counter <len(this_slice):
            x = np.append(x,this_slice[counter])
            y = np.append(y,this_slice[counter+1])
            z = np.append(z,this_slice[counter+2])
            counter = counter + 3
    #Name of the path csv should be adjusted to your preference
    np.savetxt('Saved_Data/Prostate_Data.csv',[x,y,z])

#This gives the 3D data of the different beams in the RT plan and returns the [x,y,z] points of the lines that trace the beam
def beamLine(path,beam):
    #reads RT plan path
    rt_plan = dicom.dcmread(path)

    #Finds the isocenter position and gantry angle of the specific beam
    cx,cy,cz = rt_plan.BeamSequence[beam].ControlPointSequence[0].IsocenterPosition
    angle = rt_plan.BeamSequence[beam].ControlPointSequence[0].GantryAngle

    #Used to generate the line that models the beam
    hyp_length = []
    i = 0
    while i < 90:
        hyp_length = np.append(hyp_length,(300/90*(i+1)))
        i = i+1
    xbeam = []
    ybeam = []
    i = 0
    while i < 90:
        xbeam = np.append(xbeam,(cx + hyp_length[i]*np.sin((2*np.pi/360)*angle)))
        ybeam = np.append(ybeam,(cy - hyp_length[i]*np.cos((2*np.pi/360)*angle)))
        i = i+1

    return xbeam,ybeam,cz

#This function returns the 3D data with contours and beams as a figure. elevation and azimuthal parameters are for the camera angles
def plot3D(contourdata_path,beams_path,elevation,azimuthal):
    #loads data path
    x,y,z = np.loadtxt(contourdata_path)
    #every fourth slice is taken to reduce rendering time
    x=x[::4]
    y=y[::4]
    z=z[::4]

    fig = plt.figure()
    ax = fig.add_subplot(projection = '3d')

    #making a complete white background with no grid
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_xaxis.line.set_color("white")
    ax.w_yaxis.line.set_color("white")
    ax.w_zaxis.line.set_color("white")

    #body render
    ax.view_init(elev=elevation,azim=azimuthal)
    ax.scatter3D(x, y, z, marker='.', s=1, alpha = 0.5 )

    #loops through all beams and plots them
    rt_plan = dicom.dcmread(beams_path)
    beam_num = len(rt_plan.BeamSequence)
    i = 0
    while i < beam_num:
        xbeam,ybeam,cz = beamLine(beams_path,i)
        ax.scatter3D(xbeam, ybeam, cz, marker='.',s=30, color='orange')
        i=i+1

    return fig

#rotates the model 360 degrees and screenshots at every degree
def saveSC(contourdata_path,beams_path):
    for i in range(0,360,1):
        f = plot3D(contourdata_path,beams_path,30,i)
        #name the images what you would like. it should be "name"+pic%d.png because later functions call on the ending to be 'pic%d.png'
        #choose where you want to save the screenshots as well. 360 images will generate. remember the path because it will be used to generate gif
        plt.savefig('Saved_Data/ENT_SC/ENTpic%d.png' % i)

def makeVid():
    #path to the folder of 360 screenshots
    png_dir = 'Saved_Data/ENT_SC'
    images = []
    for i in range(0,360,1):
        for file_name in sorted(os.listdir(png_dir)):
            if file_name.endswith('c'+str(i)+'.png'):
                file_path = os.path.join(png_dir, file_name)
                images.append(imageio.imread(file_path))
    #name gif what you like. it should be saved in 'static/images/' because the web app calls for this later
    imageio.mimsave('static/images/ENT.gif', images, fps = 30)
