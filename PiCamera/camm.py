from picamera import PiCamera, Color
import time
from datetime import datetime
#https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7

path = '/home/pi/scripts/PiCamera/phot_fold'

camera = PiCamera(resolution=(700, 1000), framerate=1.7, sensor_mode=3)
camera.rotation = 180



while True:
    
    camera.start_preview(alpha = 255) #0-255
    
    camera.annotate_text = datetime.now().strftime("%Yr%mm%dd %Hh%Mm%Ss")
    camera.annotate_background = Color('white')
    camera.annotate_foreground = Color('black')

    camera.capture(f'{path}/{datetime.now().strftime("%Yr%mm%dd %Hh%Mm%Ss")}.jpg')
    
    time.sleep(280)
    camera.stop_preview()



