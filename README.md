# Aero light-duty vehicles

This repo contains the code utilized to collect data to quantify aero benefits of close-following light-duty vehicles.
It is written in python and uses commercial hardware.

## Hardware

### 1. National Instruments analog I/O device

<img src="https://github.com/afernandezcanosa/aero_light_duty/blob/master/images/nidaq_mx.jpg"
     style="float: left; margin-right: 10px; width="200" height="180"" />

## Data Acquisition scripts

|      Vehicle     |                Code               |                   Status                  |
|:----------------:|:---------------------------------:|:-----------------------------------------:|
|  2016 Mazda CX9  |  ```eems_aero19_logger_mazda_cx9.py```  |     Successfully tested and integrated    |
|  2017 Ford F150  |  ```eems_aero19_logger_ford_f150.py```  | Successfully tested (except axle torques) |
| 2011 Ford Fusion | ```eems_aero19_logger_ford_fusion.py``` |   Successfully tested (except lidar)      |

## Data visualization and control

See shared folder
