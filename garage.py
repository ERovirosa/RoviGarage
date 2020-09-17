import time
import smbus
import sys
import RPi.GPIO as GPIO

from flask import Flask, render_template, redirect
import constants

DEVICE_ADDR = 0x10
bus = smbus.SMBus(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def press(relay, duration):
	bus.write_byte_data(DEVICE_ADDR, relay, 0xFF)
	time.sleep(duration)
	bus.write_byte_data(DEVICE_ADDR, relay, 0x00)
	print("garage button pressed")

def checkStatus():
	if GPIO.input(17):
		print("garage open")
		return 1
	else:
		print("garage closed")
		return 0

app = Flask(__name__)

@app.route('/')
def default():
	return render_template("buttons.html")

@app.route('/press')
def open():
	press(1, .5)
	return redirect('/')

@app.route('/status')
def status():
	status = checkStatus()
	if status:
		return "garage open"
	else:
		return "garage closed"
	
def main():
	app.run(host = '0.0.0.0', port=constants.port, debug=True)

if __name__ == "__main__":
	main()
