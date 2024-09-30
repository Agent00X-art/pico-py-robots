"""This micropython program makes the motor1 and motor2
move in forward and backward directions."""

from machine import Pin, PWM
from L298N_motor import L298N
import time
from machine import Pin, I2C
from vl53l0x import VL53L0X

#v53l0x settings

sda = Pin(14)
scl = Pin(15)
id = 1
device_1_xshut = Pin(13, Pin.OUT)
print("setting up i2c", id)
device_1_xshut.value(0)
i2c = I2C(id=id, sda=sda, scl=scl)

print(repr(i2c.scan()))
if 0x29 not in i2c.scan():
    print("Failed to find device")
    raise RuntimeError()

tof = VL53L0X(i2c)

budget = tof.measurement_timing_budget_us
print("Budget was:", budget)
tof.set_measurement_timing_budget(40000)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 12)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 8)

# motors 

ENA = PWM(Pin(0))        
IN1 = Pin(2, Pin.OUT)         
IN2 = Pin(1, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(3, Pin.OUT)
ENB = PWM(Pin(5))

motor1 = L298N(ENA, IN1, IN2)     #create a motor1 object
motor2 = L298N(ENB, IN3, IN4)     #create a motor2 object

while True:
    distance = (50 - (tof.ping())) * 20
    print(distance)
    motor1.setSpeed(55000 - distance)
    motor2.setSpeed(55000 + distance)
    motor2.forward()
    motor1.forward()

