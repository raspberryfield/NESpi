'''
raspberryfield.life 2020-07
'''
import traceback
import yaml
import RPi.GPIO as GPIO
import time
from evdev import UInput, ecodes as e

### NEScontroller.py ###
class NEScontroller:
	def __init__(self, config, uinput):
		self.config = config
		self.clock = config["Clock"]
		self.setupGPIO(self.config)
		self.uinput = uinput

	def __del__(self):
		print ("--Deconstructor called.")
		self.uinput.close()

	def setupGPIO(self, settings):
		print ("---GPIO settings: %s" % settings)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(settings["Latch"], GPIO.OUT, initial=0)
		GPIO.setup(settings["Data"], GPIO.OUT, initial=1)
		GPIO.setup(settings["Clock"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	def exec(self):
		if GPIO.input(self.clock):
			GPIO.output(18, 1)
			self.uinput.write(e.EV_KEY, e.KEY_A, 1) #2 hold
		else:
			GPIO.output(18, 0)
			self.uinput.write(e.EV_KEY, e.KEY_A, 0)
		self.uinput.syn()


### Main ###
def getConfig():
	with open('config.yaml') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)
	print ("--Config: %s" % data)
	return data


def main():
	print ("--Starting NESpi.py.")
	try:
		config = getConfig()
		uinput = UInput()
		print ("--Player1:")
		player1 = NEScontroller(config["Player1"], uinput)
		while True:
			player1.exec()
			#uinput.syn()
			time.sleep(1)

	except KeyboardInterrupt:
		print ("\n--Ctrl+C, Exiting program.")
	except Exception as e:
		print ("An unforseen error has occurred!")
		print ("Error message: ", e)
		print (traceback.format_exc())
		print ("-----")
	finally:
		del player1
		print ("--Good bye!")
		GPIO.cleanup()
		uinput.close()

if __name__ == '__main__':
	main()

