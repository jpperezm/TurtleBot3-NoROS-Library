# TurtleBot3-NoROS-Library
Python library designed to facilitate the control of the TurtleBot 3 Burger robot without the need to use ROS. With TurtleBot3-NoROS-Library, you can access the robot's low-level functions directly and easily without the learning curve of ROS. Additionally, the library is designed to be compatible with both the physical robot and the Webots simulator, allowing users to use the same code in both environments. This project also includes examples and guides to help you get started quickly, either in simulation or in the real world.

# TurtleBot3-NoROS-Library Usage Guide

![Turtlebot3 Burger](images/turtlebot3.jpg)

## Robot Components

### Raspberry Pi 3
TurtleBot3's brain, responsible for processing information and executing control algorithms.

![Raspberry Pi 3](images/Raspberry_Pi_3_B+_(26931245278).png)

### Dynamixel XL430-W250 Servomotors
High-precision motors that control the robot's movement.

![Servomotores Dynamixel XL430-W250](images/xl430_product.png)

### LDS-01 LiDAR
Sensor that measures distances and detects obstacles in 360° using a laser.

![LiDAR LDS-01](images/lds_small.png)

#### USB2LDS Board
Interface that connects the LiDAR to the Raspberry Pi.

![USB2LDS board](images/USB2LDS.jpeg)

### OpenCR 1.0 Board
Central controller that manages communication between the robot's components and the Raspberry Pi.

![OpenCR 1.0 board](images/opencr.png)

#### IMU (Inertial Measurement Unit)
Provides orientation and acceleration data, essential for the robot's navigation.

### Battery
11.1V, 1800mAh battery that powers all components, with an autonomy of approximately 2 hours and 30 minutes.

![LIPO Battery 11.1V 1,800mAh](images/bateriaTB3.jpeg)

## Preparing the Robot

### Using the Preloaded Firmware (ROS)
The robot comes with a firmware on the OpenCR 1.0 board for using ROS. If you wish to work with ROS, it is not necessary to change this firmware.  
If you change the board firmware and want to use it with ROS again, follow the steps shown in the following link:  
[Instrucciones para utilizar la openCR 1.0 con ROS](https://emanual.robotis.com/docs/en/platform/turtlebot3/opencr_setup/#opencr-setup)

### Loading the Program for the Python Library

To use the Python library, follow these steps:

1. **Download and Configure Arduino IDE:**
   - Download Arduino IDE from the following link: [Arduino IDE Download](https://www.arduino.cc/en/software)
   - Open Arduino IDE and go to `File -> Preferences -> Additional Boards Manager URLs`.
   - Add the following URL: `https://raw.githubusercontent.com/ROBOTIS-GIT/OpenCR/master/arduino/opencr_release/package_opencr_index.json`.
   - Install the **Dynamixel2Arduino** library from the Library Manager.

![Preferences](images/arduinoIDE1.PNG) ![Library Manager](images/libraryManager.PNG)

2. **Connect OpenCR 1.0 to the Computer:**
   - Connect the OpenCR 1.0 board to your computer via USB.

3. **Load the Program:**
   - Ensure the OpenCR 1.0 board is selected in Arduino IDE.
   - Load the correct program to use the Python library. Code is located in openCR_code folder of this repository.

### Connect to the Raspberry Pi 3

With the program loaded on the OpenCR 1.0 board, connect and configure the TurtleBot's Raspberry Pi 3 to load the library files.

1. **SSH Connection:**
   - Connect the Raspberry Pi 3 to the same network as your computer.
   - Use an SSH client (like PuTTY) to connect to the Raspberry Pi 3.

2. **Clone the Repository:**
   - Clone the library repository on the Raspberry Pi 3:
     ```bash
     git clone git@github.com:jpperezm/TurtleBot3-NoROS-Library.git
     ```

3. **Run Test Program:**
   - Run the test program to verify that the library works correctly:
     ```bash
     python turtlebot_python_wrapper/test_code/odometry.py
     ```
   If everything is set up correctly, the robot should move forward a few centimeters and stop.

## Using the Library with Webots (Simulator)

### Uploading Simulator Code to the Raspberry Pi 3

To upload the simulator code to the Raspberry Pi 3, create a `.sh` file in Ubuntu or a `.bat` file in Windows with the following content, replacing the variable values with your configuration:

**Ubuntu:**
```bash
#!/bin/bash

# Variables
TARGET="[nombre del fichero].py"
DESTINATION="ubuntu@[IP del turtlebot]:[ruta destino en el turtlebot]"
CODE_DIR="[ruta destino en el turtlebot]"
SSH_USER="ubuntu"
SSH_HOST="[IP del turtlebot]"

# Function to deploy the file
deploy() {
    scp "$TARGET" "$DESTINATION"
}

# Function to run the script on the robot
run() {
    scp "$TARGET" "$DESTINATION"
    ssh "$SSH_USER@$SSH_HOST" "cd $CODE_DIR && python3 $TARGET"
}

# Function to clean the target file on the robot
clean() {
    ssh "$SSH_USER@$SSH_HOST" "rm -f ${CODE_DIR}${TARGET}"
}

# Check the command line argument
if [ "$1" == "deploy" ]; then
    deploy
elif [ "$1" == "run" ]; then
    run
elif [ "$1" == "clean" ]; then
    clean
else
    echo "Usage: $0 {deploy|run|clean}"
    exit 1
fi
```

**Windows:**
```bash
@echo off

REM Variables
set TARGET="[nombre del fichero].py"
set DESTINATION="ubuntu@[IP del turtlebot]:[ruta destino en el turtlebot]"
set CODE_DIR="[ruta destino en el turtlebot]"
set SSH_USER="ubuntu"
set SSH_HOST="[IP del turtlebot]"

REM Function to deploy the file
:deploy
    scp %TARGET% %DESTINATION%
    goto :eof

REM Function to run the script on the robot
:run
    scp %TARGET% %DESTINATION%
    ssh %SSH_USER%@%SSH_HOST% "cd %CODE_DIR% && python3 %TARGET%"
    goto :eof

REM Function to clean the target file on the robot
:clean
    ssh %SSH_USER%@%SSH_HOST% "rm -f %CODE_DIR%%TARGET%"
    goto :eof

REM Check the command line argument
if "%1"=="deploy" goto deploy
if "%1"=="run" goto run
if "%1"=="clean" goto clean

REM Invalid argument
echo Usage: %~nx0 {deploy^|run^|clean}
exit /b 1
```

This file should be executed with the following command in Ubuntu:
```bash
./deploy.sh deploy
```

In Windows, execute it with the following command:

```bash
deploy.bat deploy
```
Alternatively, simply double-click the .bat file.
