from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
import sys

import time
import RPi.GPIO as GPIO

#sets the on/off switch for voltage
ON = GPIO.HIGH
OFF = GPIO.LOW

#morse code unit definitions
MORSE_UNIT = 0.2
DOT = (1 * MORSE_UNIT)
DASH = (3 * MORSE_UNIT)
SPC = (1 * MORSE_UNIT)
CHR_S = (2 * MORSE_UNIT) #is acually 3, but every char has 1 unit space already 
WRD_S = (4 * MORSE_UNIT) #is actually 7, but every letter already has 3 units space

def setPins():
	PINR = 11
	PINS = [PINR]
	return PINS

#initialize GPIO and set pins to output mode
def GPIOSetup():
    
	GPIO.setmode(GPIO.BOARD)
	
	for i in PINS:
		GPIO.setup(i, GPIO.OUT)
	#end for
#end def

#create a custom window
class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(200, 200, 300, 300)
		self.setWindowTitle("LED GUI Program")		
		self.initUI()
		
	def initUI(self):
		self.fieldEdit = QLineEdit(self)
		self.fieldEdit.move(100, 10)
		self.fieldEdit.setMaxLength(12)
		
		morseCodeBlinker = LEDBlinker(PINS[0])
		self.rB = MyButton(self, qtw.QPushButton, "Blink LED", 100, 50, lambda:morseCodeBlinker(self.fieldEdit.text()))
		self.eB = MyButton(self, qtw.QPushButton, "Exit", 100, 130, self.close)
		
	def closeEvent(self, event):
		turnOff()
		GPIO.cleanup()
		return
#end def

#custom button class
class MyButton:
	def __init__(self, win, buttonType, text, x, y, response):
        
		self.win = win
		self.text = text
		self.x = x
		self.y = y
		self.response = response
		
		self.InitButton(buttonType)
		
	#initialize button
	def InitButton(self, buttonType):
        
        #render radio button in selected window
		self.button = buttonType(self.win)
		self.button.setText(self.text)
		self.button.move(self.x, self.y)
		self.button.clicked.connect(self.response)
	#end def
#end class
	

#action when button is clicked
class LEDBlinker:
    
    #button recieves output pin
	def __init__(self, pin):
		self.pin = pin
		self.message = ""
		
	#searches pin array for selected pin
	def __call__(self, message):
		self.message = message
		self.buzzMessage(self.message)
		
	#receives an array of characters and feeds each character into the self.buzzChar method
	#then adds a delay for the word break at the end of the message
	def buzzMessage(self, message):
		#from first element to final element in message
		for letter in message:
			self.buzzChar(letter)
	    
		time.sleep(WRD_S);
	#end def

	#receives a character and determines what type of morse signal to send depending on that
	#afterwords ads a delay for the character break.
	def buzzChar(self, letter):

		#morse code doesn't detect case, so give all letters a standardized case
		letter = letter.lower()
	    
		if (letter == ' '):
			time.sleep(WRD_S);
		elif (letter == 'a'):
			self.buzz(DOT)
			self.buzz(DASH)
		elif (letter == 'b'):
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DOT)
		elif (letter == 'c'):
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DOT)
		elif (letter == 'd'):
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DASH)
		elif (letter == 'e'):
			self.buzz(DOT)
		elif (letter == 'f'):
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DOT)
		elif (letter == 'g'):
			self.buzz(DASH)
			self.buzz(DASH)
			self.buzz(DOT)
		elif (letter == 'h'):
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DOT)
		elif (letter == 'i'):
			self.buzz(DOT)
			self.buzz(DOT)
		elif (letter == 'j'):
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DASH)
			self.buzz(DASH)
		elif (letter == 'k'):
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DASH)
		elif (letter == 'l'):
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DOT)
		elif (letter == 'm'):
			self.buzz(DASH)
			self.buzz(DASH)
		elif (letter == 'n'):
			self.buzz(DASH)
			self.buzz(DOT)  
		elif (letter == 'o'):
			self.buzz(DASH)
			self.buzz(DASH)
			self.buzz(DASH)
		elif (letter == 'p'):
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DASH)
			self.buzz(DOT)
		elif (letter == 'q'):
			self.buzz(DASH)
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DASH)
		elif (letter == 'r'):
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DOT)
		elif (letter == 's'):
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DOT)
		elif (letter == 't'):
			self.buzz(DASH)
		elif (letter == 'u'):
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DASH)
		elif (letter == 'v'):
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DOT)
			self.buzz(DASH)
		elif(letter == 'w'):
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DASH)  
		elif (letter == 'x'):
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DOT)
		elif (letter == 'y'):
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DASH)
			self.buzz(DASH)
		elif (letter == 'z'):
			self.buzz(DASH)
			self.buzz(DASH)
			self.buzz(DOT)
			self.buzz(DOT)
		#endifs

		#we'e finishd a character, so add the chararacter delay
		time.sleep(CHR_S)
	#enddef
	
	#turns on a selected device for the given amount of time, then turn it off and delay for 1 morse code unit
	def buzz(self, amount):
		GPIO.output(self.pin, ON)
		time.sleep(amount);
		GPIO.output(self.pin, OFF)
		time.sleep(SPC)
	#end def
#end class


#main window
def window():
	app = QApplication(sys.argv)
	win = MyWindow()
	
	win.show()
	sys.exit(app.exec_())
#end def
	

#shutdown procedure to turn all pins off
def turnOff():
	for pin in PINS:
		GPIO.output(pin, OFF)
#end def

PINS = setPins()
GPIOSetup()
turnOff()
window()
