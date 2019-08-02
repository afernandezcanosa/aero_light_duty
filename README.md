# Aero light-duty vehicles

This repo contains the code utilized to collect data to quantify aero benefits of close-following light-duty vehicles.
It is written in python and uses commercial hardware.

## Hardware

### 1. National Instruments analog I/O device

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/nidaq_mx.jpg"
     style="float: left; margin-right: 10px"
	 width="250"
	 height="225"/>

This National Instrument device is connected to a laptop through USB and is used to read voltage analog measurements from the axle torque sensors and send voltages to the acceleration pedal of the car.

### 2. Comma AI Grey Panda CAN interface

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/grey_panda.jpg"
     style="float: left; margin-right: 10px"
	 width="250"
	 height="166"/>
	 
The Grey Panda is a CAN shield sold by CommaAI that is able to communicate with the car via the CAN protocol. It has three different CAN buses that can be used and is connected to the laptop via USB. Furthermore, the grey panda can read high-precission GPS coordinates via its serial port. Therefore, the grey panda is used to collect data.
	 
### 3. Comma AI White Panda CAN interface

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/white_panda.jpeg"
     style="float: left; margin-right: 10px"
	 width="200"
	 height="200"/>
	 
The White Panda is a CAN shield sold by CommaAI that is able to communicate with the car via the CAN protocol. It has three different CAN buses that can be used and is connected to the laptop via USB. As the white panda does not read GPS coordinates, it is used to read the important CAN signals from the car: vehicle speed, distance with preceding vehicle, etc. send them to the laptop so that it can send voltage signals via the Nidaq-MX device. 

## Data Acquisition scripts

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_logger_mazda_cx9.py```  |     Successfully tested and integrated    |
|  2017 Ford F150  |  ```eems_aero19_logger_ford_f150.py```  | Successfully tested (except axle torques) |
| 2011 Ford Fusion | ```eems_aero19_logger_ford_fusion.py``` |   Successfully tested (except lidar)      |

## Data visualization and control

See shared folder
