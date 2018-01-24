# PythonOpenCV

Based on Rodrigo Agundez code at PyData Tutorial. https://github.com/rragundez/PyData
For explanation search PyData video on youtube.
Developed on Windows 7 and Raspberry Pi 3.

- IDE used: PyCharm Edu v3.0.1
	- Platform: Windows 7 / Raspbian Jessie
	- Python: Version 2.7
	- Project: Face recognition based attendance system (Trial)
  
  
- Dependencies:
  - Python 2.7
    - OpenCV 3.0.1
    - PyQt 5
    - numpy
    - matplotlib
    - Visual Studio 2012 Express
		- CMake 2.8.11.2 GUI / CMake

	1. Get OpenCV 3.1.0 from OpenCV Master archive
		a. On Windows: Download and extract the archive
		b. On Raspbian:
			$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.1.0.zip
			$ unzip opencv.zip
	
	2. Download OpenCV_contrib from OpenCV_Contrib tag 3.1.0
		OpenCV_contrib Master contain the most recent module and totally different from tag 3.1.0
		a. On Windows: Download and extract the archive
		b. On Raspbian:
			$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.1.0.zip
			$ unzip opencv_contrib.zip
			
	3. Download python modules:
		a. pip for pip install
		b. pip install numpy
		c. pip install matplotlib

	4. Test python import:
		a. import numpy
		b. import matplotlib
	
		
	5. Compile OpenCV 
	*This should be the step after step 4 (installing python modules)
		On Windows:
		
			Requirements: 
				Visual Studio 2012 Express
				CMake GUI
				Copy cv2.pyd from build folder1 to C:\Python27\Lib\site-packages
				refer: http://audhootchavancv.blogspot.my/2015/08/how-to-install-opencv-30-and.html
			1. Create "build" folder inside the opencv-3.1.0
			2. Open Cmake and browse source to the OpenCV folder
			3. Browse Build folder to the folder that we just created
			4. Configure: Select Visual Studio 11 and "use default native compilers"
			5. Click "finish" and wait Cmake analyse 
			6. After it done mark appropriate field (leave as default is fine)
			7. Select the "OPENCV_EXTRA_MODULES_PATH" and browse the "opencv_contrib-3.1.0\modules"
			8. Generate and this will create "OpenCV.sln" 
			9. Open the "OpenCV.sln" with Visual Studio 2012
			10. In solution explorer right-click on ALL_BUILD and build (this is the Debug)
			11. Once the debug is built, select (Release) and build again
			12. After that, build (Release) for INSTALL and then build once again on (Debug).
			13. Everything will be created in the "install" folder
			14. Copy "cv2.pyd" from "build\lib\Release" to "C:\Python27\Lib\site-packages"
			15. Create In system variable (To use with Visual Studio)
				Create system variable
				Variable name: OPENCV_BUILD
				value: C:\opencv_path\build
				Path: C:\opencv_Pth\build\install\x86\vc11\bin
			
		
		On Raspbian :
			1. Expand File System
				$ sudo raspi-config
					Expand File System
					Reboot
			2. Upgrade and update existing packages
				$ sudo apt-get update
				$ sudo apt-get upgrade
				
			3. Install dependencies:
				// Get developer tools including CMake
				$ sudo apt-get install build-essential cmake pkg-config
				
				// Get image I/O packages
				// install the latest version if available
				// if encounter error try installing each package one-by-one
				$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
				
				// Get Video I/O packages
				$ sudo apt-get install libavcodec-dev libavformat-dev libswcale-dev libv4l-dev
				$ sudo apt-get install libxvidcore-dev libx264-dev
				
				// OpenCV come with sub-module "highgui" for basic GUIs
				// to compile this would require GTK development library
				$ sudo apt-get install libgtk2.0-dev
				
				// make sure python is the latest version
				$ sudo apt-get install python2.7-dev
				
				// Compile and Install OpenCV *required numpy to be installed first
				// Cmake OpenCV
				$ cd ~/opencv-3.1.0/
				$ mkdir build
				$ cd build
				$ cmake -D CMAKE_BUILDE_TYPE=RELEASE \
				    -D CMAKE_INSTALL_PREFIX=/usr/local \
				    -D INSTALL_PYTHON_EXAMPLES=ON \
				    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
				    -D BUILD_EXAMPLES=ON
				
				// Analyse Output
				// Compile OpenCV using all 4 core 
				// ISSUE/CAUTION: Raspberry Pi might overheat up to 86
				// SOLUTION: Require Heat sink and fan or some kind of cooling system
				$ make -j4 
				
				// If error using multiple core, else skip this
				$ make clean
				$ make 
				
				// Analyse the output
				// Now time to install OpenCV
				$ sudo make install
				$ sudo ldconfig
				
				// final step check installation
				$ python
				>> import cv2
				>> from cv2 import face
				>> import cv2.face
				>> cv2.__version__
			
reference: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
