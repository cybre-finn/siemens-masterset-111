from threading import Timer
import time
import alsaaudio
import wave
import RPi.GPIO as GPIO

class Ringtone:
    shouldring = 0
    ringtone = None
    ringfile = None

    ringstart = 0

    shouldplayhandset = 0
    handsetfile = None
    timerHandset = None

    config = None

    def __init__(self, config):
        self.config = config
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26, GPIO.OUT)
	GPIO.setup(21, GPIO.OUT)
	
    def start(self):
        self.shouldring = 1
        self.ringtone = Timer(0, self.doring)
        self.ringtone.start()
        self.ringstart = time.time()

    def stop(self):
        self.shouldring = 0
        if self.ringtone is not None:
            self.ringtone.cancel()

    def starthandset(self, file):
        self.shouldplayhandset = 1
        self.handsetfile = file
        if self.timerHandset is not None:
            print "[RINGTONE] Handset already playing?"
            return

        self.timerHandset = Timer(0, self.playhandset)
        self.timerHandset.start()

    def stophandset(self):
        self.shouldplayhandset = 0
        if self.timerHandset is not None:
            self.timerHandset.cancel()
            self.timerHandset = None

    def playhandset(self):
        print "Starting dialtone"
        wv = wave.open(self.handsetfile)
        device = alsaaudio.PCM(card="Device")
        #device.setchannels(wv.getnchannels())
        #device.setrate(wv.getframerate())
        #device.setperiodsize(320)

        data = wv.readframes(320)
        while data and self.shouldplayhandset:
            device.write(data)
            data = wv.readframes(320)
        wv.rewind()
        wv.close()


    def playfile(self, file):
        wv = wave.open(file)
        self.device = alsaaudio.PCM(card="ALSA")
        self.device.setchannels(wv.getnchannels())
        self.device.setrate(wv.getframerate())
        self.device.setperiodsize(320)

        data = wv.readframes(320)
        while data:
            self.device.write(data)
            data = wv.readframes(320)
        wv.rewind()
        wv.close()

    def doring(self):
        n=0
        while self.shouldring:
            n+=1
            GPIO.output(26, GPIO.HIGH)
            GPIO.output(21, GPIO.LOW)
            time.sleep(0.025)
            GPIO.output(26, GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)
            time.sleep(0.025)
            if n==24:
                time.sleep(3)
                n=0
                    if time.time() - 40 > self.ringstart:
                        self.stop()
