from machine import Pin, I2C, PWM
from vl53l0x import setup_tofl_device, TBOOT
import utime
from L298N_motor import L298N
import time
from vl53l0x import VL53L0X


sda1 = Pin(8)
scl1 = Pin(9)
id1 = 0
led = Pin("LED",Pin.OUT)
print("setting up i2c", id)

i2c = I2C(id=id1, sda=sda1, scl=scl1)

sda_l=Pin(14)
scl_l=Pin(15)
i2c_l=I2C(1,sda=sda_l, scl=scl_l, freq=400000)

def get_line():
    raw_result = i2c_l.readfrom_mem(0x11,0,10)
    # print(raw_result)
    analog_result = [0, 0, 0, 0, 0]
    for i in range(0, 5):
        high_byte = raw_result[i*2] << 8
        low_byte = raw_result[i*2+1]
        analog_result[i] = high_byte + low_byte
        if analog_result[i] > 1024:
	        continue
    # print(analog_result)
    average = [0, 0, 0, 0, 0]
    lt_list = [[], [], [], [], []]
    lt = analog_result
    for lt_id in range(0, 5):
		  lt_list[lt_id].append(lt[lt_id])
    for lt_id in range(0, 5):
         average[lt_id] = int(sum(lt_list[lt_id])/3)
    return(average)

print(repr(i2c.scan()))
if 0x29 not in i2c.scan():
    print("Failed to find device")
    raise RuntimeError()

front = VL53L0X(i2c)

from machine import Pin, I2C, PWM
from vl53l0x import setup_tofl_device, TBOOT
import utime
from L298N_motor import L298N
import time
from vl53l0x import VL53L0X


sda1 = Pin(8)
scl1 = Pin(9)
id1 = 0
led = Pin("LED",Pin.OUT)
print("setting up i2c", id)

i2c = I2C(id=id1, sda=sda1, scl=scl1)

sda_l=Pin(14)
scl_l=Pin(15)
i2c_l=I2C(1,sda=sda_l, scl=scl_l, freq=400000)

def get_line():
    raw_result = i2c_l.readfrom_mem(0x11,0,10)
    # print(raw_result)
    analog_result = [0, 0, 0, 0, 0]
    for i in range(0, 5):
        high_byte = raw_result[i*2] << 8
        low_byte = raw_result[i*2+1]
        analog_result[i] = high_byte + low_byte
        if analog_result[i] > 1024:
	        continue
    # print(analog_result)
    average = [0, 0, 0, 0, 0]
    lt_list = [[], [], [], [], []]
    lt = analog_result
    for lt_id in range(0, 5):
		  lt_list[lt_id].append(lt[lt_id])
    for lt_id in range(0, 5):
         average[lt_id] = int(sum(lt_list[lt_id])/3)
    return(average)

print(repr(i2c.scan()))
if 0x29 not in i2c.scan():
    print("Failed to find device")
    raise RuntimeError()

front = VL53L0X(i2c)

budget = front.measurement_timing_budget_us
print("Budget was:", budget)
front.set_measurement_timing_budget(40000)
front.set_Vcsel_pulse_period(front.vcsel_period_type[0], 12)
front.set_Vcsel_pulse_period(front.vcsel_period_type[1], 8)



# device_1_xshut = Pin(13, Pin.OUT)
# i2c_1 = I2C(id=1, sda=Pin(14), scl=Pin(15))

# # Set this low to disable device 1
# print("Setting up device 0")
# device_1_xshut.value(0)
# tofl0 = setup_tofl_device(i2c_1, 40000, 12, 8)
# tofl0.set_address(0x31)

ENA = PWM(Pin(0))        
IN1 = Pin(2, Pin.OUT)         
IN2 = Pin(1, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(3, Pin.OUT)
ENB = PWM(Pin(5))


motor1 = L298N(ENA, IN1, IN2)     #create a motor1 object
motor2 = L298N(ENB, IN3, IN4)     #create a motor2 object
def left():
    try:
        print("Now setting up device 1")
        # Re-enable device 1 - on the same bus
        device_1_xshut.value(1)
        utime.sleep_us(TBOOT)

        tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
        time.sleep(0.1)

        while True:
            frontd = front.ping()
            right, left = tofl0.ping(), tofl1.ping()
            print(left, 'mm, ', right, 'mm', frontd, "mm")
            # distance = (160 - right)*(400)
            distance = (80 - left)*(-400 )
            print(distance)
            motor1.setSpeed(62000 - distance)
            motor2.setSpeed(62000 + distance)
            motor2.forward()
            motor1.forward()
            if left>300 and left < 1000:
                motor1.setSpeed(0)
                motor2.setSpeed(0)
                time.sleep(5) 
                break
    finally:
        # Restore default address
        print("Restoring")
        tofl0.set_address(0x29)
def right():
    time.sleep(1)
    try:
        print("Now setting up device 1")
        # Re-enable device 1 - on the same bus
        device_1_xshut.value(1)
        utime.sleep_us(TBOOT)
    
        tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
        blue = 0
        final = 0
        while True:
            if final == 1:
                break
            else:
                while True:
                    # led.value(1)
                    line = get_line()
                    print(line[1],line[2],line[3], "blue:", blue)
                    frontd = front.ping()
                    right, left = tofl0.ping(), tofl1.ping()
                    print(left, 'mm, ', right, 'mm')
                    distance = (160 - right)*(180)
                    # distance = (100 - left)*(-200)
                    motor1.setSpeed(62000 - distance)
                    motor2.setSpeed(62000 + distance)
                    motor2.forward()
                    motor1.forward()
                    if line[1] < 47.5 and line [2] < 49.3 and line[3] < 50:
                        final = 1
                        print("stop")
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.forward()
                        motor1.forward()
                        blue = 3
                       # ПРОЕЗД К ФИНИШУ
                        time.sleep(0.3)
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        led.value(0)
                        for i in range (blue):
                            led.value(1)
                            time.sleep(0.5)
                            led.value(0)
                            time.sleep(0.5)
                        time.sleep(50)
                        break
                    if frontd <70:
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        time.sleep(0)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor1.backward()
                        motor2.forward()
                        time.sleep(0.2)

                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        # time.sleep(1)
                        # motor1.setSpeed(62000)
                        # motor2.setSpeed(62000)
                        # motor1.forward()
                        # motor2.forward()
                        # time.sleep(2)
                        break
                    elif right > 250:
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        time.sleep(0)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.forward()
                        motor1.forward()
                        time.sleep(0.1)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.backward()
                        motor1.forward()
                        time.sleep(0.3)
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.forward()
                        motor1.forward()
                        time.sleep(0.5)
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        time.sleep(0)
                        break
                    # if line[2] < 70 and line [2] > 55 :
                    #     blue +=1 
                    #     motor1.setSpeed(62000)
                    #     motor2.setSpeed(62000)
                    #     motor2.forward()
                    #     motor1.forward()
                    #     time.sleep(0.1)
                    #     print(blue)
    finally:
        # Restore default address
        print("Restoring")
        tofl0.set_address(0x29)
motor1.setSpeed(62000)
motor2.setSpeed(62000)
while True:
    line = get_line()
    print(line[0],line[1],line[2],line[3],line[4])
    if line[0] < 40:
        motor1.setSpeed(62000)
        motor2.setSpeed(40000)
        motor2.forward()
        motor1.forward()
         # вправо сильно
    if line[1] < 40:
        motor1.setSpeed(62000)
        motor2.setSpeed(52000)
        motor2.forward()
        motor1.forward()
         # вправо не сильно
    if line[2] < 40:
        motor1.setSpeed(62000)
        motor2.setSpeed(62000)
        motor2.forward()
        motor1.forward()
         # прямо
    if line[3] < 40:
        motor1.setSpeed(50000)
        motor2.setSpeed(62000)
        motor2.forward()
        motor1.forward()
         # влево не сильно
    if line[4] < 40:
        motor1.setSpeed(42000)
        motor2.setSpeed(62000)
        motor2.forward()
        motor1.forward()
         # влево сильно

budget = front.measurement_timing_budget_us
print("Budget was:", budget)
front.set_measurement_timing_budget(40000)
front.set_Vcsel_pulse_period(front.vcsel_period_type[0], 12)
front.set_Vcsel_pulse_period(front.vcsel_period_type[1], 8)



# device_1_xshut = Pin(13, Pin.OUT)
# i2c_1 = I2C(id=1, sda=Pin(14), scl=Pin(15))

# # Set this low to disable device 1
# print("Setting up device 0")
# device_1_xshut.value(0)
# tofl0 = setup_tofl_device(i2c_1, 40000, 12, 8)
# tofl0.set_address(0x31)

ENA = PWM(Pin(0))        
IN1 = Pin(2, Pin.OUT)         
IN2 = Pin(1, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(3, Pin.OUT)
ENB = PWM(Pin(5))


motor1 = L298N(ENA, IN1, IN2)     #create a motor1 object
motor2 = L298N(ENB, IN3, IN4)     #create a motor2 object
def left():
    try:
        print("Now setting up device 1")
        # Re-enable device 1 - on the same bus
        # device_1_xshut.value(1)
        utime.sleep_us(TBOOT)

        # tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
        time.sleep(0.1)

        while True:
            frontd = front.ping()
            right, left = tofl0.ping(), tofl1.ping()
            print(left, 'mm, ', right, 'mm', frontd, "mm")
            # distance = (160 - right)*(400)
            distance = (80 - left)*(-400 )
            print(distance)
            motor1.setSpeed(62000 - distance)
            motor2.setSpeed(62000 + distance)
            motor2.forward()
            motor1.forward()
            if left>300 and left < 1000:
                motor1.setSpeed(0)
                motor2.setSpeed(0)
                time.sleep(5) 
                break
    finally:
        # Restore default address
        print("Restoring")
        tofl0.set_address(0x29)
def right():
    time.sleep(1)
    try:
        print("Now setting up device 1")
        # Re-enable device 1 - on the same bus
        device_1_xshut.value(1)
        utime.sleep_us(TBOOT)
    
        tofl1 = setup_tofl_device(i2c_1, 40000, 12, 8)
        blue = 0
        final = 0
        while True:
            if final == 1:
                break
            else:
                while True:
                    # led.value(1)
                    line = get_line()
                    print(line[1],line[2],line[3], "blue:", blue)
                    frontd = front.ping()
                    right, left = tofl0.ping(), tofl1.ping()
                    print(left, 'mm, ', right, 'mm')
                    distance = (160 - right)*(180)
                    # distance = (100 - left)*(-200)
                    motor1.setSpeed(62000 - distance)
                    motor2.setSpeed(62000 + distance)
                    motor2.forward()
                    motor1.forward()
                    if line[1] < 47.5 and line [2] < 49.3 and line[3] < 50:
                        final = 1
                        print("stop")
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.forward()
                        motor1.forward()
                        blue = 3
                       # ПРОЕЗД К ФИНИШУ
                        time.sleep(0.3)
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        led.value(0)
                        for i in range (blue):
                            led.value(1)
                            time.sleep(0.5)
                            led.value(0)
                            time.sleep(0.5)
                        time.sleep(50)
                        break
                    if frontd <70:
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        time.sleep(0)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor1.backward()
                        motor2.forward()
                        time.sleep(0.2)

                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        # time.sleep(1)
                        # motor1.setSpeed(62000)
                        # motor2.setSpeed(62000)
                        # motor1.forward()
                        # motor2.forward()
                        # time.sleep(2)
                        break
                    elif right > 250:
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        time.sleep(0)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.forward()
                        motor1.forward()
                        time.sleep(0.1)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.backward()
                        motor1.forward()
                        time.sleep(0.3)
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        motor1.setSpeed(62000)
                        motor2.setSpeed(62000)
                        motor2.forward()
                        motor1.forward()
                        time.sleep(0.5)
                        motor1.setSpeed(0)
                        motor2.setSpeed(0)
                        time.sleep(0)
                        break
                    # if line[2] < 70 and line [2] > 55 :
                    #     blue +=1 
                    #     motor1.setSpeed(62000)
                    #     motor2.setSpeed(62000)
                    #     motor2.forward()
                    #     motor1.forward()
                    #     time.sleep(0.1)
                    #     print(blue)
    finally:
        # Restore default address
        print("Restoring")
        tofl0.set_address(0x29)
motor1.setSpeed(62000)
motor2.setSpeed(62000)
while True:
    line = get_line()
    print(line[0],line[1],line[2],line[3],line[4])
    if line[0] < 40:
        motor1.setSpeed(62000)
        motor2.setSpeed(40000)
        motor2.forward()
        motor1.forward()
         # вправо сильно
    if line[1] < 40:
        motor1.setSpeed(62000)
        motor2.setSpeed(52000)
        motor2.forward()
        motor1.forward()
         # вправо не сильно
    if line[2] < 40:
        motor1.setSpeed(62000)
        motor2.setSpeed(62000)
        motor2.forward()
        motor1.forward()
         # прямо
    if line[3] < 40:
        motor1.setSpeed(50000)
        motor2.setSpeed(62000)
        motor2.forward()
        motor1.forward()
         # влево не сильно
    if line[4] < 40:
        motor1.setSpeed(42000)
        motor2.setSpeed(62000)
        motor2.forward()
        motor1.forward()
         # влево сильно