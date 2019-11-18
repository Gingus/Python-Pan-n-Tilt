# encoding: utf8
from __future__ import unicode_literals
import sys
import os

try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import pygubu
#Ucomment on pi
from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
#This uses Adafruit motor library, note: good for continuous rotation servos
from adafruit_motor import servo

i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)
pca.frequency = 50

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
servo1 = servo.Servo(pca.channels[0], min_pulse=580, max_pulse=2480)
servo2 = servo.Servo(pca.channels[1], min_pulse=580, max_pulse=2480)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
#servo1 = servo.Servo(pca.channels[1], min_pulse=600, max_pulse=2400)

# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2600)

# The pulse range is 1000 - 2000 by default.
servo1 = servo.Servo(pca.channels[0])
servo2 = servo.Servo(pca.channels[1])
servo1.angle = 50
servo2.angle = 50
##for i in range(180):
##    servo1.angle = i
##for i in range(180):
##    servo1.angle = 180 - i
##pca.deinit()#I think this stops the signal after the move to save power
#Adapt the bit above

##servo1.angle = i
##pca.deinit()

class Myapp:
    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder()
        #call from the current file path then "filename.ui"
        fpath = os.path.join(os.path.dirname(__file__),"test3.ui")
        builder.add_from_file(fpath)
        
        #mainwindow is the name/ID in pygubu of the main ttk.Frame
        #that contains all the other widgets
        mainwindow = builder.get_object('mainwindow', master)

        builder.connect_callbacks(self)
##        self.set_scrollbars()

    def on_Button_Update_Tilt_clicked(self):
        Enter_Tilt_High = (self.builder.tkvariables['TiltHighEntryVar'].get())
        Add_High = print(Enter_Tilt_High)
        
        Enter_Tilt_Low = (self.builder.tkvariables['TiltLowEntryVar'].get())
        Add_Tilt_Low = print(Enter_Tilt_Low)

        scale = self.builder.get_object('Scale_Tilt')
        scale.configure({'from':int(Enter_Tilt_High)});
        
        scale = self.builder.get_object('Scale_Tilt')
        scale.configure({'to':int(Enter_Tilt_Low)});

    def on_Button_Update_Pan_clicked(self):
        Enter_High = (self.builder.tkvariables['PanHighEntryVar'].get())
        Add_High = print(Enter_High)
        
        Enter_Low = (self.builder.tkvariables['PanLowEntryVar'].get())
        Add_Low = print(Enter_Low)

        scale = self.builder.get_object('Scale_Pan')
        scale.configure({'from':int(Enter_High)});
        
        scale = self.builder.get_object('Scale_Pan')
        scale.configure({'to':int(Enter_Low)});

    def entry_invalid(self):
        messagebox.showinfo('Title', 'Invalid entry input')

##
##    def checkbutton_command(self):
##        messagebox.showinfo('Title', 'Checkbutton command')

    def on_scale1_changed(self, event):#This matches the command for        scale1
        #in gubu. Gets the scale's command
        label = self.builder.get_object('Label_Tilt_Scale')
        #Gets and builds the label by name
        scale1 = self.builder.get_object('Scale_Tilt')#'scale1' = the ID in      gubu
        #of the scale in the UI file. Gets and builds the scale
        label.configure(text=scale1.get())
        #Uses the variable from the scale  and outputs it to the label
        print(scale1.get()) #New Test Worked
        #uses the variable from scale to update the servo position
        servo1.angle = scale1.get()
        #pca.deinit()#New Bit! Removed this as it stops the servo updating/moving
    
    def on_scale2_changed(self, event):#This matches the command for        scale1
        #in gubu. Gets the scale's command
        label = self.builder.get_object('Label_Pan_Scale')
        #Gets and builds the label by name
        scale2 = self.builder.get_object('Scale_Pan')#'scale1' = the ID in       gubu
        #of the scale in the UI file. Gets and builds the scale
        label.configure(text=scale2.get())
        #Uses the variable from the scale  and outputs it to the label
        print(scale2.get()) #New Test Worked
        #uses the variable from scale to update the servo position
        servo2.angle = scale2.get()
        #pca.deinit()#New Bit! Removed this as it stops the servo updating/moving
    
    
    
        

if __name__ == '__main__':
    root = tk.Tk()
    app = Myapp(root)
    root.mainloop()

##Note: To set the slider variables try self.slider.set(100) OR
    ##self.slider.From_.set(100)/self.slider.To:.set(100) maybe