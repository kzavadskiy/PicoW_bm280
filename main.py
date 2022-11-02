from machine import Pin, I2C
import time
import bme280
import BlynkLib
import network

ssid = 'zlio' #phone wifi 
password = 'kos28kos28' #password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

BLYNK_AUTH='ntu-cD5ar9_i0E7yC1LcDB6G3kbjNIpI'

blynk = BlynkLib.Blynk(BLYNK_AUTH)

T_VPIN = 1 #Virtual Pin 1, Gauge temperature
P_VPIN = 2 #Virtual Pin 2, Gauge pressure
H_VPIN = 3 #Virtual Pin 3, Gauge humidity

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
bme = bme280.BME280(i2c=i2c) #BME280 object created

while True:
    temperature = bme.values[0] #reading the value of temperature
    pressure = bme.values[1]    
    humidity = bme.values[2]    
    blynk.virtual_write(T_VPIN, float(temperature[:len(temperature)-1])) #writing to blynk virtual value
    blynk.virtual_write(P_VPIN, float(pressure[:len(pressure)-3]))
    blynk.virtual_write(H_VPIN, float(humidity[:len(humidity)-1]))
    
while True:
   blynk.run()
