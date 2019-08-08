# Aero light-duty vehicles

This repo contains the code utilized to collect data to quantify aero benefits of close-following light-duty vehicles.
It is written in python and uses commercial hardware.

## Hardware

### 1. LeddarTech 8 segments 2D lidar

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/leddar_vu8.png"
     style="float: left; margin-right: 10px"
	 width="134"
	 height="200"/>
	 
A 2D lidar with 8 different segments and a range up to 80 meters in the most optimal conditions with reflective tape. It is manufactured and commercialized by [LeddarTech](https://leddartech.com/). Their measurements can be read by USB or CAN (it has one CAN bus). Therefore, it is a good option for automotive applications where the CAN protocol is widely used.


#### Leddar settings

Before using the lidar with CAN protocol with larger longitudinal range, some settings must be modified by using the official software provided by LeddarTech:


|      Parameter    |                Value             |
|:-----------------:|:--------------------------------:|
|  CAN Baud rate    |             500 kbps             |
|  Serial Baud rate |               9600               |
|  Accumulation     |                8                 |
| Oversampling      |                8                 | 
| Points            |                60                |    

### 2. National Instruments analog I/O device

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/nidaq_mx.jpg"
     style="float: left; margin-right: 10px"
	 width="250"
	 height="225"/>

This National Instrument device is connected to a laptop through USB and is used to read voltage analog measurements from the axle torque sensors and send voltages to the acceleration pedal of the car.

### 3. Comma AI Panda interface

#### 3.1. Grey Panda CAN interface

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/grey_panda.jpg"
     style="float: left; margin-right: 10px"
	 width="250"
	 height="166"/>
	 
The Grey Panda is a CAN shield sold by [CommaAI](https://comma.ai/) that is able to communicate with the car via the CAN protocol. It has three different CAN buses that can be used and is connected to the laptop via USB. Furthermore, the grey panda can read high-precission GPS coordinates via its serial port. Therefore, the grey panda is used to collect data.
	 
#### 3.2. White Panda CAN interface

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/white_panda.jpeg"
     style="float: left; margin-right: 10px"
	 width="200"
	 height="200"/>
	 
The White Panda is a CAN shield sold by [CommaAI](https://comma.ai/) that is able to communicate with the car via the CAN protocol. It has three different CAN buses that can be used and is connected to the laptop via USB. As the white panda does not read GPS coordinates, it is used to read the important CAN signals from the car: vehicle speed, distance with preceding vehicle, etc. send them to the laptop so that it can send voltage signals via the Nidaq-MX device. 



## Data Acquisition scripts

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_logger_mazda_cx9.py```  |     Successfully tested and integrated    |
|  2017 Ford F150  |  ```eems_aero19_logger_ford_f150.py```  | Successfully tested (except axle torques) |
| 2011 Ford Fusion | ```eems_aero19_logger_ford_fusion.py``` |   Successfully tested (except lidar)      |

## Data visualization and control

See shared folder

### a. Data visualization

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_visualization_mazda_cx9.py```  |     Successfully tested and integrated    |
|  2017 Ford F150  |  ```eems_aero19_visualization_ford_f150.py```  |  										    |
| 2011 Ford Fusion | ```eems_aero19_visualization_ford_fusion.py``` |        						  	 	    |

### b. Data visualization and cruise control

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_control_mazda_cx9.py```  |     							   |
|  2017 Ford F150  |  ```eems_aero19_control_ford_f150.py```  |  	Pedal model done			   |
| 2011 Ford Fusion | ```eems_aero19_control_ford_fusion.py``` |     Pedal model done               |

