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
		self.latch = config["Latch"]
		self.data = config["Data"]
		self.clock = config["Clock"]
		self.__setupGPIO(self.config)
		self.uinput = uinput

	def __del__(self):
		print ("--Deconstructor called.")
		self.uinput.close()

	def __setupGPIO(self, settings):
		print ("---GPIO settings: %s" % settings)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(settings["Latch"], GPIO.OUT, initial=0)
		GPIO.setup(settings["Data"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		GPIO.setup(settings["Clock"], GPIO.OUT, initial=1)

	def __latch(self):
		#print ("---Latch called.")
		GPIO.output(self.latch, 1)
		GPIO.output(self.latch, 0)

	def __clock(self):
		#print ("--Clock called.")
		GPIO.output(self.clock, 0)
		GPIO.output(self.clock, 1)

	def exec(self):
		self.__latch()
		if GPIO.input(self.data):
			#GPIO.output(18, 1)
			self.uinput.write(e.EV_KEY, e.BTN_TL, 0) #2 hold
			#print ("---A NOT pressed")
		else:
			#GPIO.output(18, 0)
			self.uinput.write(e.EV_KEY, e.BTN_TL, 1)
			#print ("---A IS pressed")
		self.__clock() #B
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_TR, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_TR, 1)
		self.__clock() #SELECT
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_TL2, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_TL2, 1)
		self.__clock() #START
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_TR2, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_TR2, 1)
		self.__clock() #UP
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_A, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_A, 1)
		self.__clock() #DOWN
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_B, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_B, 1)
		self.__clock() #LEFT
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_C, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_C, 1)
		self.__clock() #RIGT
		if GPIO.input(self.data):
			self.uinput.write(e.EV_KEY, e.BTN_Y, 0)
		else:
			self.uinput.write(e.EV_KEY, e.BTN_Y, 1)
		self.__clock()
		self.uinput.syn()


### Main ###
def getConfig():
	with open('config.yaml') as f:
		data = yaml.load(f, Loader=yaml.FullLoader)
	print ("--Config: %s" % data)
	return data

def getUInput():
	global e
	cap={e.EV_KEY : [e.KEY_A, e.KEY_D, e.KEY_F, e.KEY_G, e.KEY_H, e.KEY_J, e.KEY_S, e.KEY_W]}
	'''
	cap={('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('?', 4), ('?', 17), ('?', 20)], ('EV_KEY', 1): [('KEY_ESC', 1), ('KEY_1', 2), ('KEY_2', 3), ('KEY_3', 4), ('KEY_4', 5), ('KEY_5', 6), ('KEY_6', 7), ('KEY_7', 8), ('KEY_8', 9), ('KEY_9', 10), ('KEY_0', 11), ('KEY_MINUS', 12), ('KEY_EQUAL', 13), ('KEY_BACKSPACE', 14), ('KEY_TAB', 15), ('KEY_Q', 16), ('KEY_W', 17), ('KEY_E', 18), ('KEY_R', 19), ('KEY_T', 20), ('KEY_Y', 21), ('KEY_U', 22), ('KEY_I', 23), ('KEY_O', 24), ('KEY_P', 25), ('KEY_LEFTBRACE', 26), ('KEY_RIGHTBRACE', 27), ('KEY_ENTER', 28), ('KEY_LEFTCTRL', 29), ('KEY_A', 30), ('KEY_S', 31), ('KEY_D', 32), ('KEY_F', 33), ('KEY_G', 34), ('KEY_H', 35), ('KEY_J', 36), ('KEY_K', 37), ('KEY_L', 38), ('KEY_SEMICOLON', 39), ('KEY_APOSTROPHE', 40), ('KEY_GRAVE', 41), ('KEY_LEFTSHIFT', 42), ('KEY_BACKSLASH', 43), ('KEY_Z', 44),('KEY_X', 45), ('KEY_C', 46), ('KEY_V', 47), ('KEY_B', 48), ('KEY_N', 49), ('KEY_M', 50), ('KEY_COMMA', 51), ('KEY_DOT', 52), ('KEY_SLASH', 53), 
		('KEY_RIGHTSHIFT', 54), ('KEY_KPASTERISK', 55), ('KEY_LEFTALT', 56), ('KEY_SPACE', 57), ('KEY_CAPSLOCK', 58), ('KEY_F1', 59), ('KEY_F2', 60), ('KEY_F3', 61), ('KEY_F4', 62), ('KEY_F5', 63), ('KEY_F6', 64), ('KEY_F7', 65), ('KEY_F8', 66), ('KEY_F9', 67), ('KEY_F10', 68), ('KEY_NUMLOCK', 69), ('KEY_SCROLLLOCK', 70), ('KEY_KP7', 71), ('KEY_KP8', 72), ('KEY_KP9', 73), ('KEY_KPMINUS', 74), ('KEY_KP4', 75), ('KEY_KP5', 76), ('KEY_KP6', 77), ('KEY_KPPLUS', 78), ('KEY_KP1', 79), ('KEY_KP2', 80), ('KEY_KP3', 81), ('KEY_KP0', 82), ('KEY_KPDOT', 83), ('KEY_102ND', 86), ('KEY_F11', 87), ('KEY_F12', 88), ('KEY_RO', 89), ('KEY_HENKAN', 92), ('KEY_KATAKANAHIRAGANA', 93), ('KEY_MUHENKAN', 94), ('KEY_KP JPCOMMA', 95), ('KEY_KPENTER', 96), ('KEY_RIGHTCTRL', 97), ('KEY_KPSLASH', 98), ('KEY_SYSRQ', 99), ('KEY_RIGHTALT', 100), ('KEY_HOME', 102), ('KEY_UP', 103), ('KEY_PAGEUP', 104), ('KEY_LEFT', 105), ('KEY_RIGHT', 106), ('KEY_END', 107), ('KEY_DOWN', 108), ('KEY_PAGEDOWN', 109), ('KEY_INSERT', 110), ('KEY_DELETE', 111), 
		(['KEY_MIN_INTERESTING', 'KEY_MUTE'], 113), ('KEY_VOLUMEDOWN', 114), ('KEY_VOLUMEUP', 115), ('KEY_POWER', 116), ('KEY_KPEQUAL', 117), ('KEY_PAUSE', 119), ('KEY_KPCOMMA', 121), (['KEY_HANGEUL', 'KEY_HANGUEL'], 122), ('KEY_HANJA', 123), ('KEY_YEN', 124), ('KEY_LEFTMETA', 125), ('KEY_RIGHTMETA', 126), ('KEY_COMPOSE', 127), ('KEY_STOP', 128), ('KEY_AGAIN', 129), ('KEY_PROPS', 130), ('KEY_UNDO', 131), ('KEY_FRONT', 132), ('KEY_COPY', 133), ('KEY_OPEN', 134), ('KEY_PASTE', 135), ('KEY_FIND', 136), ('KEY_CUT', 137), ('KEY_HELP', 138), ('KEY_F13', 183), ('KEY_F14', 184), ('KEY_F15', 185), ('KEY_F16', 186), ('KEY_F17', 187), ('KEY_F18', 188), ('KEY_F19', 189), ('KEY_F20', 190), ('KEY_F21', 191), ('KEY_F22', 192), ('KEY_F23', 193), ('KEY_F24', 194), ('KEY_UNKNOWN', 240)], ('EV_MSC', 4): [('MSC_SCAN', 4)], ('EV_LED', 17): [('LED_NUML', 0), ('LED_CAPSL', 1), ('LED_SCROLLL', 2)]}
	'''

	#cap = {0:[0, 1], 1:[30, 32, 33, 34, 35, 36, 31, 37]}
	print(cap)

	#uinput = UInput(events=cap, name='NESpi', vendor='test', product=0x1, version=0x3, bustype=3)
	uinput = UInput()
	print(uinput)
	return uinput

def main():
	print ("--Starting NESpi.py. v.0.2")
	try:
		config = getConfig()
		global e
		cap={e.EV_KEY : [e.KEY_A]}
		#uinput = UInput(cap, name='NESpi', version=0x3)
		uinput=getUInput()
		print ("--Player1:")
		player1 = NEScontroller(config["Player1"], uinput)
		while True:
			player1.exec()
			#uinput.syn()
			time.sleep(0.05)

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

