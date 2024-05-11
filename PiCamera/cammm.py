from picamera import PiCamera, Color
import time
from datetime import datetime
from fractions import Fraction
#https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7

path = '/home/pi/scripts/PiCamera/phot_fold'

print('set1 start')
camera = PiCamera(resolution=(700, 1000), sensor_mode=3)
camera.rotation = 180
camera.resolution = (700, 1000)
camera.framerate = 0.17
camera.awb_mode = 'auto'
#camera.exposure_mode = 'verylong'
print('set1 end')

print('set2 start')

camera.iso = 800
camera.shutter_speed = 2000000
#camera.awb_mode = 'off'
#camera.awb_gains = (Fraction(417,256), Fraction(87,64))
print('set2 end')


print('preview start')
camera.start_preview()
time.sleep(5)
print('capture start')
camera.capture('/home/pi/scripts/PiCamera/awb_{x}.jpg')
print('capture end')
camera.stop_preview()
print('preview end')

quit()

for y, x in enumerate(camera.AWB_MODES):
    if y == 0:
        continue
    camera.start_preview()
    camera.awb_mode = x
    time.sleep(5)
    
    camera.capture(f'/home/pi/scripts/PiCamera/awb_{x}.jpg')
    
    
    
    camera.stop_preview()

camera.awb_mode = 'auto'

for y, x in enumerate(camera.EXPOSURE_MODES):
    if y == 0:
        continue
    camera.start_preview()
    camera.exposure_mode = x
    time.sleep(5)
    
    camera.capture(f'/home/pi/scripts/PiCamera/exposure_{x}.jpg')
    
    
    
    camera.stop_preview()
camera.exposure_mode = 'auto'
