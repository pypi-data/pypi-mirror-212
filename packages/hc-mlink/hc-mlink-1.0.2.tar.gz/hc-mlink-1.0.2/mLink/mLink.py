########################################################################
# FILE:    mLink.py
# DATE:    07/06/23
# VERSION: 1.0.2
# AUTHOR:  Andrew Davies
   
# 01/06/23 version 1.0.1: Original release version
# 07/06/23 version 1.0.2: Added additional bPad_Read_Key_Index() & 
#						  bPad_Read_Key() function for keypad module

# This library adds hardware support for the Hobby Components mLink 
# range of serial I2C modules. Current supported boards:

# mLink 12 Bit port expander (SKU: HCMODU0180)
# mLink DHT22 temperature and humidity sensor (SKU: HCMODU0181)
# mLink 1 channel relay module (SKU: HCMODU0182)
# mLink 2 channel relay module (SKU: HCMODU0183)
# mLink 4 channel relay module (SKU: HCMODU0184)
# mLink RGBW light controller (SKU: HCMODU0185)
# mLink NTC Temperature sensor module (SKU: HCMODU0186)
# mLink Matrix 4x4 Keypad (SKU: HCMODU0188)
# mLink 1602 & 2004 Character LCD (SKU: HCMODU0190A & HCMODU0190B)
# mLink 6 Button Keypad (SKU: HCMODU0193)
# mLink Home Sensor (SKU: HCMODU0198)

# Please see LICENSE file for terms of use.
########################################################################

# Import the SMBus2 module
from smbus2 import SMBus
from time import sleep

class mLink:
	# Standard mLink registers
	STATUS_REG = 				0
	ADD_REG = 					1
	TYPE_REG = 					2
	SUBTYPE_REG = 				3
	SW_VER_REG = 				4
	SLEEP_REG = 				5
	
	STATUS_REG_COM_ERROR =		(1 << 0)	# COM error
	STATUS_REG_ACCESS_ERROR =	(1 << 1)	# Reg acc error
	STATUS_REG_BUSY	=			(1 << 2)	# Device busy flag

	def __init__(self, i2C_port):
		self.i2cbus = SMBus(i2C_port)

	# Generic register byte read function
	def read(self, add, reg):
		data = self.i2cbus.read_byte_data(add, reg)
		return data

	# Generic register integer read function
	def readInt(self, add, reg):
		#data = self.i2cbus.read_byte_data(add, reg) << 8
		#data |= self.i2cbus.read_byte_data(add, reg) 
		return self.i2cbus.read_word_data(add, reg)
	
	# Generic register bt read function
	def readBit(self, add, reg, bit):
		data = self.i2cbus.read_byte_data(add, reg)
		return (data >> bit) & 0b1
	
	# Generic register byte write function
	def write(self, add, reg, data):
		self.i2cbus.write_byte_data(add, reg, data)
		
	# Generic register word write function	
	def writeInt(self, add, reg, data):
		self.i2cbus.write_word_data(add, reg, data)

	# Generic register bit write function
	def writeBit(self, add, reg, bit, state):
		data = self.i2cbus.read_byte_data(add, reg)
		data = (data & ~(1 << bit)) | (state << bit)
		self.i2cbus.write_byte_data(add, reg, data)

	# Returns the current state of the status register
	def Status(self, add):
		return self.i2cbus.read_byte_data(add, self.STATUS_REG)
	
	# Checks the state of the busy bit in the status register.
	# Returns true if the device is busy, false if not.
	def busy(self, add):
		if self.i2cbus.read_byte_data(add, self.STATUS_REG) & self.STATUS_REG_BUSY:
			return True
		else:
			return False

	# Changes the address of a module.
	def Change_Address(self, add, new_add):
		flag = False
		# First test to see if there is a module at the current address
		try:
			data = self.read(add, self.ADD_REG)
		
			if data != add:
				return "Error: Unknown device at address " + hex(add)
		except IOError:
			return "Error: Device not found at address " + hex(add)
		
		# Next, make sure there isn't already a module at the new address	
		try:
			self.read(new_add, self.ADD_REG)
			return "Error: Device already exists at address " + hex(new_add)
		except IOError:
			flag = True
		
		# If the above is ok then change the address	
		if(flag):
			self.write(add, self.ADD_REG, 0x55)
			self.write(add, self.ADD_REG, 0xAA)
			self.write(add, self.ADD_REG, new_add)
			
			# Check to see if the address has been changed
			try:
				sleep(0.1)
				self.read(new_add, self.ADD_REG)
				return "OK"
			except IOError:
				return "Error: Failed"

	
	# Returns the module type at the specified address		
	def Get_Type(self, add):
		moduleType = self.read(add, self.TYPE_REG)
		
		if moduleType == 0x00:
			return "Digital IO"
		elif moduleType == 0x01:
			return "Sensor"
		elif moduleType == 0x02:
			return "Relay"
		elif moduleType == 0x03:
			return "Light controller"
		elif moduleType == 0x04:
			return "Input"
		elif moduleType == 0x05:
			return "Display"
		else:
			return "Unknown: " + hex(moduleType)


	# Returns the module subtype at the specified address
	def Get_Subtype(self, add):
		typeSubtype = self.read(add, self.TYPE_REG) << 8
		typeSubtype |= self.read(add, self.SUBTYPE_REG)
		
		if typeSubtype == 0x0000:
			return "12 Pin IO"
		
		elif typeSubtype == 0x0100:
			return "DHT22 Temp/Hum"
		elif typeSubtype == 0x0101:
			return "NTC Temperature"
		elif typeSubtype == 0x0103:
			return "Home Sensor"
		
		elif typeSubtype == 0x0200:
			return "1 Channel Relay"
		elif typeSubtype == 0x0201:
			return "2 Channel Relay"
		elif typeSubtype == 0x0202:
			return "4 Channel Relay"
		
		elif typeSubtype == 0x0300:
			return "RGBW"
		
		elif typeSubtype == 0x0400:
			return "Matrix 4x4 Keypad"
		elif typeSubtype == 0x0401:
			return "6 Button Keypad"
		
		elif typeSubtype == 0x0500:
			return "1602 LCD"
		elif typeSubtype == 0x0501:
			return "2004 LCD"

		else:
			return "Unknown: " + hex((typeSubtype & 0xFF)) 
	
	
	# Returns the current software version in string format
	def Get_SW_Ver(self, add):
		ver = self.read(add, self.SW_VER_REG)
		sVer = str(ver >> 4) + "."
		if (ver & 0x0F) < 10:
			sVer += "0"
		sVer += str(ver & 0x0F)
		return sVer
	
	
	# Scans the I2C bus for mLink devices and returns a list of found 
	# devices with each entry in the list containing the devices 
	# address in hex, module type, module subtype, and software version
	def Find_Devices(self):
		devList = []
		for i in range(1,128):
			try:
				add = self.read(i, self.ADD_REG)
				if add == i:
					moduleType = self.Get_Type(i)
					subType = self.Get_Subtype(i)
					Ver = self.Get_SW_Ver(i)
					devList.append([hex(i), moduleType, subType, Ver])
			except:
				pass
				
		return devList
	
	
	####################################################################
	# 			MLINK 12 BIT PORT EXPANDER (HCMODU0180)
	####################################################################
	
	# Modules registers
	DIO12_DIR0_REG = 				10
	DIO12_DIR1_REG = 				11
	DIO12_DATA0_REG = 				12
	DIO12_DATA1_REG = 				13
	
	DIO12_D0 =						0
	DIO12_D1 =						1
	DIO12_D2 =						2
	DIO12_D3 =						3
	DIO12_D4 =						4
	DIO12_D5 =						5
	DIO12_D6 =						6
	DIO12_D7 =						7
	DIO12_D8 =						0
	DIO12_D9 =						1
	DIO12_D10 =						2
	DIO12_D11 =						3
	
	DIO12_OUTPUT =					0
	DIO12_INPUT =					1

	# Sets the direction of all 12 pins where bit 0 = pin 0 and bit 11 =
	# pin 11
	# Writing a 0 to a bit will set the appropriate pin to an output and
	# writing a 1 will set it to an input
	def DIO12_Port_Dir(self, add, direction):
		self.writeInt(add, self.DIO12_DIR0_REG, direction)
	
	# Sets the state of any pins configured to be an output where bit 
	# 0 = pin 0 and bit 11 = pin 11
	def DIO12_Port_Write(self, add, data):
		self.writeInt(add, self.DIO12_DATA0_REG, data)
	
	# Reads the state of all 12 pins and outputs it as an integer where 
	# bit 0 = pin 0 and bit 11 = pin 11
	def DIO12_Port_Read(self, add):
		return self.readInt(add, self.DIO12_DATA0_REG)
	
	def DIO12_Pin_Dir(self, add, pin, direction):
		data = self.readInt(add, self.DIO12_DIR0_REG)
		data = (data & ~(1 << pin)) | (direction << pin)
		self.writeInt(add, self.DIO12_DIR0_REG, data)
	
	# Sets the state of a single output pin (0 to 11)
	def DIO12_Pin_Write(self, add, pin, state):
		reg = self.DIO12_DATA0_REG
		if pin > 7:
			reg = self.DIO12_DATA1_REG
			pin -= 8
		
		self.writeBit(add, reg, pin, state)

	
	# Reads the state of a single input pin (0 to 11)
	def DIO12_Pin_Read(self, add, pin):
		reg = self.DIO12_DATA0_REG
		if pin > 7:
			reg = self.DIO12_DATA1_REG
			pin -= 8
		
		return self.readBit(add, reg, pin)

	####################################################################
	
	
	####################################################################
	# 					MLINK DHT22 (HCMODU0181)
	####################################################################
	
	# Modules registers
	DHT22_DHTREAD_REG =				10
	DHT22_TEMPL_REG = 				11
	DHT22_TEMPH_REG = 				12
	DHT22_HUML_REG = 				13
	DHT22_HUMH_REG = 				14
	
	# Triggers the start of a temp/hum measurement. The busy bit must
	# then be polled via the busy() function to check when the 
	# measurement is complete. When complete the new temp & humidity can
	# be read using the DHT22_Read_Temp() & DHT22_Read_Hum() functions
	def DHT22_Start(self, add):
		self.write(add, self.DHT22_DHTREAD_REG, 1)
	
	# Returns the current temperature. Note, to get the latest
	# temperature you must first run the DHT22_Start() function
	def DHT22_Read_Temp(self, add):
		data = self.readInt(add, self.DHT22_TEMPL_REG)
		if (data & 0x8000):
			data = (data ^ 0xFFFF) * - 1 
		return data / 10
	
	# Returns the current humidity. Note, to get the latest
	# humidity you must first run the DHT22_Start() function
	def DHT22_Read_Hum(self, add):
		return self.readInt(add, self.DHT22_HUML_REG) / 10
		
	####################################################################
	
	
	####################################################################
	# 					MLINK 4CH RELAY (HCMODU0184)
	####################################################################
	
	# Modules registers
	RELAY_STATE_REG = 				10
	RLY0_ON_TIME_L = 				11
	RLY0_ON_TIME_H = 				12
	RLY1_ON_TIME_L = 				13
	RLY1_ON_TIME_H = 				14
	RLY2_ON_TIME_L = 				15
	RLY2_ON_TIME_H = 				16
	RLY3_ON_TIME_L = 				17
	RLY3_ON_TIME_H = 				18
	
	RELAY_0	=						0
	RELAY_1	=						1
	RELAY_2	=						2
	RELAY_3	=						3
	
	RELAY_ON =						1
	RELAY_OFF = 					0
	
	
	# Sets the state of one of the relays (0 to 3) where state = 0 is
	# de-energised and state = 1 is energised
	def Relay_Set(self, add, relay, state):
		self.writeBit(add, self.RELAY_STATE_REG, relay, state)
	
	# Energises (turns on) relay 0
	def Relay0_On(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_0, self.RELAY_ON)
	
	# De-energises (turns off) relay 0
	def Relay0_Off(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_0, self.RELAY_OFF)
	
	# Energises (turns on) relay 1
	def Relay1_On(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_1, self.RELAY_ON)
	
	# De-energises (turns off) relay 1
	def Relay1_Off(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_1, self.RELAY_OFF)
	
	# Energises (turns on) relay 2
	def Relay2_On(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_2, self.RELAY_ON)
	
	# De-energises (turns off) relay 2
	def Relay2_Off(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_2, self.RELAY_OFF)
	
	# Energises (turns on) relay 3
	def Relay3_On(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_3, self.RELAY_ON)
	
	# De-energises (turns off) relay 3
	def Relay3_Off(self, add):
		self.writeBit(add, self.RELAY_STATE_REG, self.RELAY_3, self.RELAY_OFF)
	
	# Sets the amount of time in seconds relay 0 will stay energised for
	# after it is trigger. After this time the relay will automatically
	# de-energise. Writing a time 0 seconds will disable this feature
	def Relay0_On_Time(self, add, time):
		self.writeInt(add, self.RLY0_ON_TIME_L, time)
	
	# Sets the amount of time in seconds relay 1 will stay energised for
	# after it is trigger. After this time the relay will automatically
	# de-energise. Writing a time 0 seconds will disable this feature
	def Relay1_On_Time(self, add, time):
		self.writeInt(add, self.RLY1_ON_TIME_L, time)
	
	# Sets the amount of time in seconds relay 2 will stay energised for
	# after it is trigger. After this time the relay will automatically
	# de-energise. Writing a time 0 seconds will disable this feature	
	def Relay2_On_Time(self, add, time):
		self.writeInt(add, self.RLY2_ON_TIME_L, time)
	
	# Sets the amount of time in seconds relay 3 will stay energised for
	# after it is trigger. After this time the relay will automatically
	# de-energise. Writing a time 0 seconds will disable this feature
	def Relay3_On_Time(self, add, time):
		self.writeInt(add, self.RLY3_ON_TIME_L, time)
			
	####################################################################
	
	
	####################################################################
	# 				MLINK RGBW CONTROLLER (HCMODU0185)
	####################################################################
	
	# Modules registers
	RGBW_R_REG = 					10
	RGBW_G_REG = 					11
	RGBW_B_REG = 					12
	RGBW_W_REG = 					13
	RGBW_BRIGHT_REG = 				14
	RGBW_LOAD_CYCLE_REG = 			15
	RGBW_PAT_STEP_SPEED_L_REG = 	16
	RGBW_PAT_STEP_SPEED_H_REG = 	17
	RGBW_PAT_STEPS_REG = 			18
	RGBW_PAT_COLOURS_REG =			19
	
	RGBW_I2C_R_0_REG =				20
	RGBW_I2C_G_0_REG =				21
	RGBW_I2C_B_0_REG =				22
	
	RGBW_I2C_R_1_REG =				23
	RGBW_I2C_G_1_REG =				24
	RGBW_I2C_B_1_REG =				25
	
	RGBW_I2C_R_2_REG =				26
	RGBW_I2C_G_2_REG =				27
	RGBW_I2C_B_2_REG =				28
	
	RGBW_I2C_R_3_REG =				29
	RGBW_I2C_G_3_REG =				30
	RGBW_I2C_B_3_REG =				31
	
	RGBW_I2C_R_4_REG =				32
	RGBW_I2C_G_4_REG =				33
	RGBW_I2C_B_4_REG =				34

	RGBW_I2C_R_5_REG =				35
	RGBW_I2C_G_5_REG =				36
	RGBW_I2C_B_5_REG =				37
	
	RGBW_I2C_R_6_REG =				38
	RGBW_I2C_G_6_REG =				39
	RGBW_I2C_B_6_REG =				40
	
	RGBW_I2C_R_7_REG =				41
	RGBW_I2C_G_7_REG =				42
	RGBW_I2C_B_7_REG =				43
	
	RGBW_SAVE_REG = 				44
	
	
	# Pre-defined patterns
	RGBW_CYCLE_USER =                   0
	RGBW_CYCLE_FAST_RGB_COLOUR_CYCLE =  1
	RGBW_CYCLE_MED_RGB_COLOUR_CYCLE =   2
	RGBW_CYCLE_SLOW_RGB_COLOUR_CYCLE =  3
	RGBW_CYCLE_FAST_RG_CYCLE =          4
	RGBW_CYCLE_ALARM_INTER_PULSE =      5
	RGBW_CYCLE_ALARM_CONT_PULSE =       6
	RGBW_CYCLE_RGB_CONT_PULSE =         7
	RGBW_CYCLE_FLAME =                  8
	
	# Sets the red brightness level where level = 0 is off and level = 
	# 255 is maximum brightness
	def RGBW_Red_Level(self, add, level):
		self.write(add, self.RGBW_R_REG, level)
	
	# Sets the green brightness level where level = 0 is off and level = 
	# 255 is maximum brightness
	def RGBW_Green_Level(self, add, level):
		self.write(add, self.RGBW_G_REG, level)
	
	# Sets the blue brightness level where level = 0 is off and level = 
	# 255 is maximum brightness
	def RGBW_Blue_Level(self, add, level):
		self.write(add, self.RGBW_B_REG, level)
	
	# Sets the white/aux brightness level where level = 0 is off and 
	# level = 255 is maximum brightness
	def RGBW_White_Level(self, add, level):
		self.write(add, self.RGBW_W_REG, level)
	
	# Sets the master brightness for all colour channels where level = 0
	# is all colours off and level = 255 is maximum
	def RGBW_Brightness(self, add, level):
		self.write(add, self.RGBW_BRIGHT_REG, level)
	
	# Plays one of the pre-defined colour patterns
	def RGBW_Pattern(self, add, pattern):
		self.write(add, self.RGBW_LOAD_CYCLE_REG, pattern)

	# Writes a user defined pattern to the module. This must be passed
	# as a list of R,G,B levels. E.g. 
	# [[R1, G1, B1], [R2, G2, B2], [Rn, Gn, Bn]]
	def RGBW_User_Pattern(self, add, pattern):
		for row in pattern:
			for col in row:
				self.write(add, self.RGBW_I2C_R_0_REG, col)
		
		self.write(add, self.RGBW_PAT_COLOURS_REG, len(pattern))


	# Sets the amount of colour steps to insert between each RGB level 
	# of the user defined pattern.
	# If there is currently a pattern playing then this value will 
	# update after the current pattern has finished
	def RGBW_Cycle_Steps(self, add, steps):
		self.write(add, self.RGBW_PAT_STEPS_REG, steps)
	
	# Sets the amount of time to wait in ms between each colour step.
	# If there is currently a pattern playing then this value will 
	# update after the current pattern has finished
	def RGBW_Cycle_Speed(self, add, speed):
		self.writeInt(add, self.RGBW_PAT_STEP_SPEED_L_REG, speed)

	####################################################################
	
	
	####################################################################
	# 				MLINK NTC TEMP SENSOR (HCMODU0186)
	####################################################################
	
	# Modules registers
	NTC_TEMPL_REG = 				11
	NTC_TEMPH_REG = 				12
	
	# Reads the curent temperature from the module and returns it as an
	# integer to 1 dp
	def NTC_Temp(self, add):
		i = 0
		
		data = self.readInt(add, self.NTC_TEMPL_REG)
		if (data & 0x8000):
			data = (data ^ 0xFFFF) * - 1 
	
		return data / 10
	
	####################################################################
	
	
	####################################################################
	# 				MLINK 4x4 Matrix Keypad (HCMODU00188)
	####################################################################

	# Modules registers
	KEYPAD_4X4_KEY_REG =			11
	KEYPAD_4X4_KEY_STATE_REG =		12
	KEYPAD_4X4_KEY_DEBOUNCE_REG =	13

	KEYPAD_4X4_KEY_STATE_BIT =		1 << 0

	# Returns True if a key is currently pressed, False if no key is
	# pressed.
	def Keypad_4x4_Key_Down(self, add):
		if self.read(add, self.KEYPAD_4X4_KEY_STATE_REG) & self.KEYPAD_4X4_KEY_STATE_BIT:
			return True
		else:
			return False

	# Returns the ASCII value of the last key pressed, or '' if no new
	# key has been pressed.
	def Keypad_4X4_Read(self, add):
		key = self.read(add, self.KEYPAD_4X4_KEY_REG)
		if key != 0:
			return chr(key)
		else:
			return ''

	####################################################################
	
	
	####################################################################
	# 				MLINK Character LCD (HCMODU00190)
	####################################################################
	
	# Modules registers
	CLCD_PRINT_CHAR_REG = 			11
	CLCD_CURS_COL_REG = 			12
	CLCD_CURS_ROW_REG = 			13
	CLCD_CR1 = 						14
	CLCD_CR2 = 						15
	CLCD_SET_BL_REG = 				16
	CLCD_SET_CONT_REG = 			17
	CLCD_PRINT_CUST_REG = 			18
	CLCD_CUST0_REG = 				19
	CLCD_CUST1_REG = 				20
	CLCD_CUST2_REG = 				21
	CLCD_CUST3_REG = 				22
	CLCD_CUST4_REG = 				23
	CLCD_CUST5_REG = 				24
	CLCD_CUST6_REG = 				25
	CLCD_CUST7_REG = 				26
	
	CLCD_CLEAR_BIT =				0
	CLCD_DISP_ON_BIT =				1
	CLCD_CURS_DIR_BIT =				0
	CLCD_DISP_TYPE_BIT =			1

	CLCD_CURS_LTOR =				0
	CLCD_CURS_RTOL =				1

	CLCD_TYPE_1602 =				0
	CLCD_TYPE_2004 =				1
	
	# Moves the cursor to the specified col & row
	def cLCD_Cursor(self, add, col, row):
		data = (row << 8) | col
		self.writeInt(add, self.CLCD_CURS_COL_REG, data)
	
	# Prints a string to the display starting at the current cursor
	# position
	def cLCD_Print(self, add, text):
		for c in text:
			data = ord(c)
			self.write(add, self.CLCD_PRINT_CHAR_REG, data)

	# Clears the display
	def cLCD_Clear(self, add):
		self.writeBit(add, self.CLCD_CR1, self.CLCD_CLEAR_BIT, 1)
		while self.busy(add):
			pass
	
	# Turns the display on or off where state = 0 is off and state = 1
	# is on
	def cLCD_on(self, add, state):
		self.writeBit(add, self.CLCD_CR1, self.CLCD_DISP_ON_BIT, state)
	
	# Sets the direction the cursor will move after printing a character
	# where direction = 0 is keft to right and direction = 1 is right to
	# left
	def cLCD_cursDir(self, add, direction):
		self.writeBit(add, self.CLCD_CR2, self.CLCD_CURS_DIR_BIT, direction)
	
	# Sets the display size where display = 0 is a 16 x 2 line display
	# and display = 1 is a 20 x 4 line display
	def cLCD_dispType(self, add, display):
		self.writeBit(add, self.CLCD_CR2, self.CLCD_DISP_TYPE_BIT, display)
	
	# Sets a backlight level where level = 0 is off and level = 10 is 
	# maximum brightness
	def cLCD_Backlight(self, add, level):
		if level > 10:
			level = 10
		self.write(add, self.CLCD_SET_BL_REG, level)
	
	# Sets the contrast level where level = 0 minimum and level = 255 is
	# maximum
	def cLCD_Contrast(self, add, level):
		self.write(add, self.CLCD_SET_CONT_REG, level)
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 0. See documentation for how to define a bitmap
	def cLCD_setCust0(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST0_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 1. See documentation for how to define a bitmap
	def cLCD_setCust1(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST1_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 2. See documentation for how to define a bitmap
	def cLCD_setCust2(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST2_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 3. See documentation for how to define a bitmap
	def cLCD_setCust3(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST3_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 4. See documentation for how to define a bitmap
	def cLCD_setCust4(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST4_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 5. See documentation for how to define a bitmap
	def cLCD_setCust5(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST5_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 6. See documentation for how to define a bitmap
	def cLCD_setCust6(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST6_REG, bitmap[i])
	
	# Writes a list of 8 x byte values containing a bitmap to custom
	# character 7. See documentation for how to define a bitmap
	def cLCD_setCust7(self, add, bitmap):
		for i in range(0, 8):
			self.write(add, self.CLCD_CUST7_REG, bitmap[i])
	
	# Prints one of the custom characters (0 to 7) to the display at the
	# current cursor position
	def cLCD_printCust(self, add, i):
		if i < 8:
			self.write(add, self.CLCD_PRINT_CUST_REG, i)


	####################################################################

	####################################################################
	# 				MLINK 6 Button Pad (HCMODU00193)
	####################################################################
	
	# Modules registers
	BPAD_BUFF_STATUS_REG = 			10
	BPAD_BUFFER_REG = 				11
	BPAD_KEY_STATE_REG = 			12
	BPAD_DEBOUNCE_REG = 			13

	BPAD_UP_BIT =					1 << 0
	BPAD_LEFT_BIT =					1 << 1
	BPAD_DOWN_BIT =					1 << 2
	BPAD_RIGHT_BIT =				1 << 3
	BPAD_SELECT_BIT =				1 << 4
	BPAD_BACK_BIT =					1 << 5

	# Returns True if buffer is empty, False if not
	def bPad_Empty(self, add):
		if self.read(add, self.PAD_BUFF_STATUS_REG) == 1:
			return True
		else:
			return False

	# Returns True if there is one or more keys present in the buffer
	# False if not
	def bPad_New_Key(self, add):
		if self.read(add, self.BPAD_BUFF_STATUS_REG) == 0:
			return True
		else:
			return False
	
	# Returns the index number of the next key
	def bPad_Read_Key_Index(self, add):
		return self.read(add, self.BPAD_BUFFER_REG)
	
	# Returns the name of the next key
	def bPad_Read_Key(self, add):
		i = self.read(add, self.BPAD_BUFFER_REG)
		if i == 0:
			return "UP"
		elif i == 1:
			return "LEFT"
		elif i == 2:
			return "DOWN"
		elif i == 3:
			return "RIGHT"
		elif i == 4:
			return "SELECT"
		elif i == 5:
			return "BACK"
		else:
			return ""

	# Returns True if the UP button is currently pressed, False if not
	def bPad_Up_State(self, add):
		if self.read(add, self.BPAD_KEY_STATE_REG) & self.BPAD_UP_BIT:
			return True
		else:
			return False

	# Returns True if the LEFT button is currently pressed, False if not
	def bPad_Left_State(self, add):
		if self.read(add, self.BPAD_KEY_STATE_REG) & self.BPAD_LEFT_BIT:
			return True
		else:
			return False

	# Returns True if the DOWN button is currently pressed, False if not
	def bPad_Down_State(self, add):
		if self.read(add, self.BPAD_KEY_STATE_REG) & self.BPAD_DOWN_BIT:
			return True
		else:
			return False

	# Returns True if the RIGHT button is currently pressed, False if not
	def bPad_Right_State(self, add):
		if self.read(add, self.BPAD_KEY_STATE_REG) & self.BPAD_RIGHT_BIT:
			return True
		else:
			return False

	# Returns True if the SELECT button is currently pressed, False if not
	def bPad_Select_State(self, add):
		if self.read(add, self.BPAD_KEY_STATE_REG) & self.BPAD_SELECT_BIT:
			return True
		else:
			return False

	# Returns True if the BACK button is currently pressed, False if not
	def bPad_Back_State(self, add):
		if self.read(add, self.BPAD_KEY_STATE_REG) & self.BPAD_BACK_BIT:
			return True
		else:
			return False

	# Sets the amout of debouncing applied to each button from 0 (none)
	# to max (254). Default is 200.
	def bPad_Debounce(self, add, debounce):
		self.write(add, self.BPAD_DEBOUNCE_REG, debounce)

	####################################################################
	
	
	####################################################################
	# 				MLINK Home Sensor (HCMODU0198)
	####################################################################
	
	# Modules registers
	HSENS_DHTREAD_REG = 			10
	HSENS_TEMPL_REG =				11
	HSENS_TEMPH_REG =				12
	HSENS_HUML_REG =				13
	HSENS_HUMH_REG =                14
	HSENS_PIR_REG =					15
	HSENS_LDR_REG =					16
	HSENS_PIR_TRIGS_L_REG =			17
	HSENS_PIR_TRIGS_H_REG =			18
	
	HSENS_DHT22_MEAS_ERROR_BIT =	3
	
	# Triggers the start of a temp/hum measurement. The busy bit must
	# then be polled via the busy() function to check when the 
	# measurement is complete. When complete the new temp & humidity can
	# be read using the HSens_Temp() & HSens_Hum() functions
	def HSENS_Start(self, add):
		self.write(add, self.HSENS_DHTREAD_REG, 1)
	
	# Returns the current temperature. Note, to get the latest
	# temperature you must first run the HSENS_Start() function
	def HSens_Temp(self, add):
		data = self.readInt(add, self.HSENS_TEMPL_REG)
		if (data & 0x8000):
			data = (data ^ 0xFFFF) * - 1 
		return data / 10
	
	# Returns the current humidity. Note, to get the latest
	# temperature you must first run the HSENS_Start() function
	def HSens_Hum(self, add):
		data = self.readInt(add, self.HSENS_HUML_REG)
		return data / 10
	
	# Returns true if the current measurement was read from the DHT22 was
	# valid, false if there was an error
	def HSens_DHT22_Error(self, add):
		return self.readBit(add, self.STATUS_REG, self.HSENS_DHT22_MEAS_ERROR_BIT)
	
	# Returns a light level sensed by the LDR sensor where 0 = dark and
	# 255 = maximum brightness
	def HSens_LDR(self, add):
		return self.read(add, self.HSENS_LDR_REG)
	
	# Returns the current state of the LDR sensor where True = currently
	# triggered and False = idle. Note that when the PIR sensor is 
	# triggered it will remain triggered for about 4 seconds.
	def HSens_PIR(self, add):
		if self.read(add, self.HSENS_PIR_REG):
			return True
		else:
			return False

	# Returns the amount of times the PIR sensor has been triggered 
	# since the counter was last reset
	def HSens_Trigs(self, add):			
		return self.readInt(add, self.HSENS_PIR_TRIGS_L_REG)
	
	# Clears/resets the PIR trigger counter
	def HSens_Clear_Trigs(self, add):
		self.write(add, self.HSENS_PIR_TRIGS_L_REG, 0)
		
	####################################################################
