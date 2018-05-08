# Rotary Dial Parser
# Expects the following hardware rules:
# 1 is 1 pulse
# 9 is 9 pulses
# 0 is 10 pulses
# forget the above for now,
# rotary dial has its own will

import RPi.GPIO as GPIO
from threading import Timer
import time

class RotaryDial:

    # We'll be reading BCM GPIO 4 (pin 7 on board)
    pin_rotary = 2

    # We'll be reading on/off hook events from BCM GPIO 3
    pin_onhook = 3

    # After 900ms, we assume the rotation is done and we get
    # the final digit.
    digit_timeout = 0.3

    # We keep a counter to count each pulse.
    current_digit = 0

    # Simple timer for handling the number callback
    number_timeout = None

    last_input = 0

    # Timer to ensure we're on hook
    onhook_timer = None
    rotary_timer = None
    should_verify_hook = True

    def __init__(self):
        # Set GPIO mode to Broadcom SOC numbering
        GPIO.setmode(GPIO.BCM)

        # Listen for rotary movements
        GPIO.setup(self.pin_rotary, GPIO.IN)
        GPIO.add_event_detect(self.pin_rotary, GPIO.BOTH, callback = self.NumberCounter, bouncetime=100)

        # Listen for on/off hooks
        GPIO.setup(self.pin_onhook, GPIO.IN)
        GPIO.add_event_detect(self.pin_onhook, GPIO.BOTH, callback = self.HookEvent)

	self.number_timeout = Timer(self.digit_timeout, self.FoundNumber)

        self.onhook_timer = Timer(2, self.verifyHook)
        self.onhook_timer.start()

    def NumberCounter(self, channel):
	input = GPIO.input(self.pin_rotary)
	if input==1:
		if self.number_timeout.isAlive():
			self.number_timeout.cancel()
			self.number_timeout.join()
		else:
			self.current_digit=0
		self.current_digit += 1
		self.number_timeout = Timer(self.digit_timeout, self.FoundNumber)
		self.number_timeout.start()


    # Wrapper around the off/on hook event
    def HookEvent(self, channel):
        input = GPIO.input(self.pin_onhook)
        if input:
            self.hook_state = 0
            self.OnHookCallback()
        else:
            self.hook_state = 1
            self.OffHookCallback()

    def StopVerifyHook(self):
        self.should_verify_hook = False

    def verifyHook(self):
        while self.should_verify_hook:
            if input==0:
                state=1
            else:
                state = 1
            self.OnVerifyHook(state)
            time.sleep(1)

    # When the rotary movement has timed out, we callback with the final digit
    def FoundNumber(self):
        if self.current_digit == 10:
            self.current_digit = 0
        self.NumberCallback(self.current_digit)

    # Handles the callbacks we're supplying
    def RegisterCallback(self, NumberCallback, OffHookCallback, OnHookCallback, OnVerifyHook):
        self.NumberCallback = NumberCallback
        self.OffHookCallback = OffHookCallback
        self.OnHookCallback = OnHookCallback
        self.OnVerifyHook = OnVerifyHook

        input = GPIO.input(self.pin_onhook)
        if input:
            self.OnHookCallback()
        else:
            self.OffHookCallback()
