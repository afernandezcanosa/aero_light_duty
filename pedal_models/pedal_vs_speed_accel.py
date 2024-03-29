#!/usr/bin/env python
from __future__ import print_function

"""
This class includes the pedal models of the three vehicles studied. Accelerator
pedal as a function of the vehicle speed and the vehicle acceleration as well as
the analog voltages as a function of the accelerator pedal. 

    1. self.coeffs -> Accel_pedal = Accel_pedal(Veh_speed, Veh_accel)
    2. self.ch0_coeffs -> APP_1 = APP_1(Accel_pedal)
    3. self.ch1_coeggs -> APP_2 = APP_2(Accel_pedal)
    
Note 1:  that we try to replicate the voltages that are sent from the Accelerator Pedal
to the Powertrain Control Module (PCM)

Note 2: Accel pedal models were fitted by using UDDS and HWY dyno cycles 
"""

class PedalModel(object):

    def __init__(self, car):

        self.car = car

        if self.car == 'mazda_cx9':
            self.coeffs = [-2.15112766e+00,
                           1.59435249e+00, 2.54082287e+01,
                           -5.65619082e-02, -4.96890927e-01, -1.04503861e+01,
                           7.97139394e-04, 2.55779716e-02, 2.12937717e-01, 1.64147857e+00]

            self.ch0_coeffs = [1.5011, 3.6]
            self.ch1_coeffs = [0.9757, 1.81]

        elif self.car == 'ford_f150':
            self.coeffs = [2.01805436e-01,
                           6.02884579e-01, 6.36548308e+00,
                          -1.67426622e-02, 1.04169336e+00, -2.43369234e-01,
                           4.63490229e-04, -9.14509267e-03, -2.10704875e-01, 1.55521523e-01]

            self.ch0_coeffs = [0.7953, 2.83]
            self.ch1_coeffs = [0.3981, 1.42]
            
            """ Model with diodes and correction 
            self.ch0_coeffs = [1.4283, 3.17]
            self.ch1_coeffs = [0.8317, 1.49]

            self.ch0_coeffs_corr = [1.3974, 3.51]
            self.ch1_coeffs_corr = [0.772, 0.0]
            """

        elif self.car == 'ford_fusion':
            self.coeffs = [-1.58738238e+00,
                           1.15274390e+00, 1.31335620e+01,
                          -3.63003606e-02, 1.12372052e-01, -5.05241104e+00,
                           6.23982212e-04, 2.53013196e-02, 3.42877674e-01, 7.16712738e-01]

            self.ch0_coeffs = [1.463, 3.134]
            self.ch1_coeffs = [0.777, 1.593]

        else:
            raise ValueError("Please introduce a valid vehicle")

    def pedal_per(self, speed_mps, accel_mps2):

        """ Polynomial model of the percentage of acceleration pedal as a
        function of speed and acceleration of the vehicle """

        accel_pedal = (self.coeffs[0] +
                       self.coeffs[1]*speed_mps + self.coeffs[2]*accel_mps2 +
                       self.coeffs[3]*speed_mps**2 + self.coeffs[4]*speed_mps*accel_mps2 + self.coeffs[5]*accel_mps2**2 +
                       self.coeffs[6]*speed_mps**3 + self.coeffs[7]*speed_mps**2*accel_mps2 + self.coeffs[8]*speed_mps*accel_mps2**2 +
                       self.coeffs[9]*accel_mps2**3)

        if accel_pedal < 0:
            accel_pedal = 0
        if accel_pedal > 100:
            accel_pedal = 100

        return accel_pedal

    def voltage_from_pedal(self, pedal_per):

        """ What are the voltages that need to be sent to the pedal to
        reach the desired acceleration pedal position """

        pedal = 0.01*pedal_per

        v_0 = self.ch0_coeffs[0] + self.ch0_coeffs[1]*pedal
        v_1 = self.ch1_coeffs[0] + self.ch1_coeffs[1]*pedal

        """ Model with diodes and correction
        if self.car == 'ford_f150' and pedal_per < 11:
            v_0 = self.ch0_coeffs_corr[0] + self.ch0_coeffs_corr[1]*pedal
            v_1 = self.ch1_coeffs_corr[0] + self.ch1_coeffs_corr[1]*pedal
        """

        return v_0, v_1

if __name__ == "__main__":
    mph_to_mps = 0.44704

    cars = ['mazda_cx9', 'ford_f150', 'ford_fusion']
    pedals = []

    for car in cars:
        pedals.append(PedalModel(car = car))

    speed_mps = 70*mph_to_mps
    accel_mps2 = 0.2
    for pedal in pedals:
        per = pedal.pedal_per(speed_mps, accel_mps2)
        print('PEDAL MODEL: ')
        print('v = %.2f m/s, a = %.2f m/s^2, car = %s ==> pedal_per = %.2f %%' %(speed_mps, accel_mps2, pedal.car, per))

    per = 15
    for pedal in pedals:
        v0, v1 = pedal.voltage_from_pedal(per)
        print('VOLTAGE MODEL: ')
        print('pedal_per = %.2f %% ==> v0 = %.3f V, v1 = %.3f V, car = %s' %(per, v0, v1, pedal.car))
