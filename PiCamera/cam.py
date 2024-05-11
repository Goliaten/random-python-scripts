from picamera import PiCamera, Color
import time
#https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/7

path = '/home/pi/scripts/PiCamera/test.jpg'

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1260, 720)
camera.framerate = 25

camera.start_preview(alpha = 230) #0-255

# camera.annotate_text = 'Hello world!'
# camera.annotate_text_size = 50 #6-160
# camera.annotate_background = Color('blue')
# camera.annotate_foreground = Color('yellow')

# camera.brightness = 70 #0-100/50
# camera.contrast = 80 #0-100/50


# for x in camera.IMAGE_EFFECTS:
#     print(x, end='')
#     camera.image_effect = x
#     input()
# camera.image_effect = 'none'

# for x in camera.EXPOSURE_MODES:
#     print(x, end='')
#     camera.exposure_mode = x
#     input()
# camera.exposure_mode = 'auto'
input()

for x in camera.AWB_MODES:
    if x == 'off':
        continue
    print(x, end='')
    camera.awb_mode = x
    input()
camera.awb_mode = 'auto'


#po zakończeniu użyj polecenia:
# MP4Box -fps 25 -add myvid.h264 myvid.mp4
# camera.start_recording(f'/home/pi/scripts/PiCamera/testvid.h264')
# print('rec')
# input()
# camera.stop_recording()
# print('rec s')

# for x in range(5):
#     time.sleep(3)    #sleep for 2+ seconds for focus
#     camera.capture(f'/home/pi/scripts/PiCamera/test{x}.jpg')
    
camera.stop_preview()

