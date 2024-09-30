import machine
from machine import I2C, Pin
import time
sda=machine.Pin(8)
scl=machine.Pin(9)
i2c=I2C(0,sda=sda, scl=scl, freq=400000)
raw_result = i2c.readfrom_mem(0x11,0,10)
print(raw_result)
def get_line():
    raw_result = i2c.readfrom_mem(0x11,0,10)
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
while True:
    print(get_line())
    time.sleep(0.1)
