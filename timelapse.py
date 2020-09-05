from picamera import PiCamera
from os import system
import datetime
from time import sleep
import sys

make_video = input("would you like to compile the video? (yes/no) -- If you are using a piZero (no) is recommended: ")

while True:
    try:
        tlminutes = int(input("Enter the number of minutes you wish to run your timelapse camera: ")) #set this to the number of minutes you wish to run your timelapse camera
    except ValueError:
        print("Invalid Input, a number is expected")
        continue
    else:
        break

while True:    
    try:
        secondsinterval = int(input("Enter the number of seconds delay between each photo taken: ")) #number of seconds delay between each photo taken
    except ValueError:
            print("Invalid Input, a number is expected")
            continue
    else:
        break

if make_video == "yes":
    while True:
        try:
            fps = int(input("Enter the video fps: ")) #frames per second timelapse video
        except ValueError:
            print("Invalid Input, a number is expected")
            continue
        else:
            break

numphotos = (int(tlminutes)*60)/int(secondsinterval) #number of photos to take
print("number of photos to take = ", int(numphotos))

dateraw= datetime.datetime.now()
datetimeformat = dateraw.strftime("%Y-%m-%d_%H:%M")
print("RPi started taking photos for your timelapse at: " + datetimeformat)

camera = PiCamera()
camera.resolution = (1920, 1080)

system('rm /home/pi/Pictures/*.jpg') #delete all photos in the Pictures folder before timelapse start

for i in range(int(numphotos)):
    camera.capture('/home/pi/Pictures/image{0:06d}.jpg'.format(i))
    sleep(secondsinterval)
print("Done taking photos.")

if make_video == "yes":
    print("Please standby as your timelapse video is created.")
    system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/Pictures/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/Videos/{}.mp4'.format(fps, datetimeformat))
    print('Timelapse video is complete. Video saved as /home/pi/Videos/{}.mp4'.format(datetimeformat))

else:
    sys.exit("Video not compiled")