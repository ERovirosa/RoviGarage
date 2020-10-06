import time
import smbus
import sys
import RPi.GPIO as GPIO

from flask import Flask, render_template, redirect
import constants

DEVICE_ADDR = 0x10
bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def press(relay, duration):
	bus.write_byte_data(DEVICE_ADDR, relay, 0xFF)
	time.sleep(duration)
	bus.write_byte_data(DEVICE_ADDR, relay, 0x00)
	print("garage button pressed")

def checkStatus(pin):
	if GPIO.input(pin):
		return True
	else:
		return False

app = Flask(__name__)

@app.route('/')
def default():
	if(checkStatus(4)):
		status = "fully closed"
	elif(checkStatus(27)):
		status = "fully open"
	else:
		status = "in the middle"
	return render_template("buttons.html", status = status)

@app.route('/press')
def open():
	press(1, .5)
	return redirect('/')

def main():
	app.run(host = '0.0.0.0', port=constants.port, debug=True)

if __name__ == "__main__":
	main()
