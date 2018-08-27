import RPi.GPIO as io
import time
import cv2
from PIL import Image
from pytesseract import image_to_string
import pyttsx as speak
from time import sleep

io.setwarnings(False)

io.setmode(io.BOARD)

TRIG1 = 3
ECHO1 = 5
SWITCH = 7

io.setup(TRIG1, io.OUT)
io.setup(ECHO1, io.IN)

io.setup(SWITCH, io.IN)


def say(tosay):
    speaker = speak.init()
    speaker.setProperty('rate', 250)
    speaker.setProperty('voice', 'english-us')
    speaker.setProperty('gender', 'female')
    speaker.say(tosay)
    a = speaker.runAndWait()


def ultra1():
    io.output(TRIG1, False)
    sleep(0.2)

    io.output(TRIG1, True)
    sleep(0.00001)

    io.output(TRIG1, False)

    while io.input(ECHO1) == 0:
        pulse_start = time.time()

    while io.input(ECHO1) == 1:
        pulse_end = time.time()

    t1 = pulse_end - pulse_start

    d1 = t1 * 17150

    d1 = round(d1, 2)
    print d1

    say("Object is")
    say(d1)
    say("centimetres away")


def blindreader():
    # IMAGE_FILE = 'imageToRead.jpeg'

    flag = 0
    print "Defining say()"

    def say(tosay):
        speaker = speak.init()
        speaker.setProperty('rate', 120)
        speaker.setProperty('voice', 'english-us')
        speaker.setProperty('gender', 'female')
        speaker.say(tosay)
        a = speaker.runAndWait()

    # loop forever

    say("Blind Reader Started")
    print("Blind Reader Started")

    while True:

        flag = flag + 1

        try:

            camera = cv2.VideoCapture(0)
            camera.set(3, 480)
            camera.set(4, 360)

            for i in xrange(10):
                temp = camera.read()

            img1 = camera.read()[1]
            camera.release()

            cv2.imshow("Result", img1)
            if cv2.waitKey(10) == ord('q'):
                break

            # convert image array to bytes image
            img1 = Image.fromarray(img1)
            img2 = img1.convert('L')
            print "::::::::::::::::::::::::::::::" + str(flag) + "::::::::::::::::::::::::::::::"
            words = None

            words = image_to_string(img2).strip()
            if words:
                print "Words are : "
                print words
                say(words)


        except KeyboardInterrupt:
            print "^C pressed."
            print "Something Else occured."
            print "Resources Cleared."
            camera.release()
            cv2.destroyAllWindows()
        except:
            print "Something Else occured."
            print "Resources Cleared."
            camera.release()
            cv2.destroyAllWindows()

        sleep(1)


while True:
    c = io.input(SWITCH)

    if (c == 1):
        ultra1()

    elif (c == 0):
        blindreader()