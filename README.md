# Aero light-duty vehicles

This repo contains the code utilized to collect data to quantify aero benefits of close-following light-duty vehicles.
It is written in python and uses commercial hardware.

## 1. Hardware

### 1.1. LeddarTech 8 segments 2D lidar

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
|  Accumulation     |                64                |
| Oversampling      |                16                |
| Points            |                60                |    
| Segments Enabled  |           Two centrals           |

### 1.2. National Instruments analog I/O device

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/nidaq_mx.jpg"
     style="float: left; margin-right: 10px"
	 width="250"
	 height="225"/>

This National Instrument device is connected to a laptop through USB and is used to read voltage analog measurements from the axle torque sensors and send voltages to the acceleration pedal of the car.

### 1.3. Comma AI Panda interface

#### 1.3.1. Grey Panda CAN interface

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/grey_panda.jpg"
     style="float: left; margin-right: 10px"
	 width="250"
	 height="166"/>

The Grey Panda is a CAN shield sold by [CommaAI](https://comma.ai/) that is able to communicate with the car via the CAN protocol. It has three different CAN buses that can be used and is connected to the laptop via USB. Furthermore, the grey panda can read high-precission GPS coordinates via its serial port. Therefore, the grey panda is used to collect data.

#### 1.3.2. White Panda CAN interface

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/white_panda.jpeg"
     style="float: left; margin-right: 10px"
	 width="200"
	 height="200"/>

The White Panda is a CAN shield sold by [CommaAI](https://comma.ai/) that is able to communicate with the car via the CAN protocol. It has three different CAN buses that can be used and is connected to the laptop via USB. As the white panda does not read GPS coordinates, it is used to read the important CAN signals from the car: vehicle speed, distance with preceding vehicle, etc. send them to the laptop so that it can send voltage signals via the Nidaq-MX device.

### 1.4. Panda ports list

* Mazda CX9
  * Read CAN data: 53002c000c51363338383037
  * Send commands and read CAN data: 4e0046000651363038363036
* Ford F150
  * Read CAN data: 360024000c51363338383037
  * Send commands and read CAN data: 26003f000651363038363036
* Ford Fusion
  * Read CAN data: 240050000c51363338383037
  * Send commands and read CAN data: 540041000651363038363036		


## 2. Data Acquisition scripts

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_logger_mazda_cx9.py```  |     Successfully tested and integrated  |
|  2017 Ford F150  |  ```eems_aero19_logger_ford_f150.py```  | Successfully tested and integrated      |
| 2011 Ford Fusion | ```eems_aero19_logger_ford_fusion.py``` |   Successfully tested (except lidar)    |

## 3. Data visualization and control

See shared folder

### 3.1. Data visualization

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_visualization_mazda_cx9.py```  |     Successfully tested and integrated    |
|  2017 Ford F150  |  ```eems_aero19_visualization_ford_f150.py```  |     Successfully tested and integrated 	|
| 2011 Ford Fusion | ```eems_aero19_visualization_ford_fusion.py``` |     Successfully tested and integrated 	|    						  	 	    

### 3.2. Data visualization and cruise control

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_control_mazda_cx9.py```  |     Pedal model done and tested    |
|  2017 Ford F150  |  ```eems_aero19_control_ford_f150.py```  |  	Pedal model done and tested	   |
| 2011 Ford Fusion | ```eems_aero19_control_ford_fusion.py``` |     Pedal model done and tested    |


## 4. Axle-torque scaling

|      Vehicle     |                Voltage (V)        |                   Axle Torque (N.m)        |
|:----------------:|:---------------------------------:|:------------------------------------------:|
|  2016 Mazda CX9  |  10                               |     2000                                   |
|  2017 Ford F150  |  10                               |  	1000	                                |
| 2011 Ford Fusion | 10                                |     3389.5                                 |


## 5. Lessons learned

### 5.1. F150 Pedal Model Issues
The accelerator pedal of the F150 is very sensitive and small perturbation seems to affect the performance of the "voltage vs pedal" model. In some cases, for small pedal percentages (which are the ones that we can control), we can even lose the control of the accelerator pedal without the possibility of reversing the current with the diode.

### 5.2. Temperature effects of the diode voltage drop
The temperature of the circuit affects the voltage drop of the diode and therefore, we can lose the control of the accelerator pedal.

### 5.3. Lidar settings and measurements
To successfully perform these tests, we need accurate measurements of the 2D lidar. A trade-off between long enough range, accuracy, reliability, and measurement rate is required. In order to do so, the settings of the lidar must be modified:

* We need a narrow strip of tape on the rear-back of the vehicles that we want to test
* As we only care about the longitudinal position of the vehicles (gap), we can select only the two central channels. This way, we can increase the measurement rate and speed up both data loggers and control/visualizations.
* Play around with accumulation/oversampling/points settings in order to obtain a measurement range of around 70 meters with high accuracy.

### 5.4. Lidar 655.35 distance measurement in Ford Fusion

During our tests, the lidar mounted in the Ford Fusion, frequently measures a distance of 655.35 meters, which, including the scaling factor, corresponds with a CAN message = 0xFFFF.
We will run a test with the company to troubleshoot the unit. It looks a power issue.

** UPDATE: It wasn't a problem of the Ford Fusion. The problem was sensor 1 that has been discarded. The rest of the sensors don't have this issue **

### 5.5. Gains of the controllers

We tested our controllers on Navistar and found the following parameters that minimize oscillations for the Ford Fusion and the Mazda CX9. We realized that far from the target point (gap, speed), the oscillations are extremely large, so before turning the APP override ON, approach the target point manually.

|      Vehicle     |  a_max (m/s^2)  |  a_min (m/s^2)  | K_p       |      K_d   |
|:----------------:|:---------------:|:---------------:|:---------:|:----------:|
|  2016 Mazda CX9  |  0.8            |    -0.8         | 0.1       |    0.35    |
|  2017 Ford F150  |                 |  	    	       |           |            |
| 2011 Ford Fusion | 0.8             |     -0.8        |  0.1      |   0.35     |

### 5.6. Correct angle of the lidars

The 2D lidars seem to work better upside down. We tested them with the F150 and the Fusion inside Argonne.
