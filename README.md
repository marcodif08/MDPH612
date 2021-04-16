# MDPH612
MDPH612 Final Project

A program that renders a 3D model of body and RT beams from DICOM structure and DICOM plan files. The 3D model is saved as a gif and displayed in a web app for patients to view their 3D RT plan.

###Requirements
`Python 3`

Packages: 
* numpy
* pydicom
* matplotlib
* psycopg2
* Flask
* imageio

##dicom_manipulation.py

To use, first install missing packages in the code using pip install [missing package].
The code assumes that RTstructure and RTplan are in the same folder. The path can be specified by the user. The files must end in .dcm.
Several functions are defined inside of dicom_manipulation.py. They are defined in the code, and the requirements are as follows:

```
def get3DData(path):
```
The requirement for get3DData is that you have the path to the RTStructure file, and that you know the index of the body structure in the ROIContourSequence dicom tag list. This function can also be used generate the 3D data for any other structure. The second requirement is that you have a folder called Saved_Data where most of the data in this program will be stored for quick 3D rendering.

```
def beamLine(path,beam):
```
beamLine simply requires the path to the RTPlan file.

```
def plot3D(contourdata_path,beams_path,elevation,azimuthal):
```
plot3D requires the path to the saved data from the get3DData function, and the path to the RTPlan file.

```
def saveSC(contourdata_path,beams_path):
```
saveSC requires the path to the saved data from the get3DData function, and the path to the RTPlan file. It also requires there to be a folder in Saved_Data to store the 360 screenshots that simulate the rotation of the 3D model.

```
def makeVid():
```
requires the path to the saved screenshot folder, and it requires the program to have a /static/images/ path. This is later used for the html code and the folders must be called the same way.
