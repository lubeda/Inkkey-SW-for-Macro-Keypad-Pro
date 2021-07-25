#In here, the logic of the different modes are defined.
#Each mode has to implement four functions (use "pass" if not needed):
#
#- activate
#Called when the mode becomes active. Usually used to set up static key assignment and icons
#- poll
#Called periodically and typically used to poll a state which you need to monitor. At the end you have to return an interval in seconds before the function is to be called again - otherwise it is not called a second time
#- animate
#Called up to 30 times per second, used for LED animation
#- deactivate
#Called when the mode becomes inactive. Used to clean up callback functions and images on the screen that are outside commonly overwritten areas.

#To avoid multiple screen refreshs, the modules usually do not clean-up the display when being deactivvated. Instead, each module is supposed to set at least the area corresponding to each button (even if it needs to be set to white if unused).

from inkkeys import *
import time
from threading import Timer
from math import ceil, floor
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb

DEBUG = False
        ############# Simple example. For Blender we just set up a few key assignments with corresponding images.
        ## Blender ## To be honest: Blender is just the minimalistic example here. Blender is very keyboard centric
        ############# and you should get used to the real shortcuts as it is much more efficient to stay on the keyboard all the time.

class ModeBlender:

    def activate(self, device):
        device.sendTextFor(0, "Blender") #Title

        #Button1 (Jog dial press)
        device.sendTextFor(1, "Play/Pause")
        device.setKeyLedfor(1,"FFCC00")
        device.assignKey(KeyCode.SW1_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.RELEASE)])

        #Jog dial rotation
        device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)]) #CW = Clock-wise, one frame forward
        device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)]) #CCW = Counter clock-wise, one frame back

        #Button2 (top left)
        device.sendTextFor(2,"cameras")
        device.setKeyLedfor(2,"FFCCFF")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.PRESS)]) #Set view to camera
        device.assignKey(KeyCode.SW2_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_0, ActionCode.RELEASE)])

        #Button3 (left, second from top)
        device.sendTextFor(3,"bounding-box")
        device.setKeyLedfor(3,"CC00FF")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.PRESS)]) #Isolation view
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DIVIDE, ActionCode.RELEASE)])

        #Button4 (left, third from top)
        device.sendTextFor(4,"====")
        device.assignKey(KeyCode.SW4_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left)
        device.sendTextFor(5,"====")
        device.assignKey(KeyCode.SW5_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right)
        device.sendTextFor(6, "ratio")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.PRESS)]) #Center on selection
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEYPAD_DOT, ActionCode.RELEASE)])
        
    def poll(self, device):
        return False    # No polling in this example

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        pass            # Nothing to clean up in this example

        ##########
        ## Gimp ## The Gimp example is similar to Blender, but we add a callback to pressing the jog dial to switch functions
        ##########

class ModeGimp:
    jogFunction = ""    #Keeps track of the currently selected function of the jog dial

    def activate(self, device):
        device.sendTextFor("title", "Gimp", inverted=True)  #Title

        #Button2 (top left)
        device.sendIconFor(2, "icons/fullscreen.png")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_Z)]) #Cut to selection (this shortcut appears to be language dependent, so you will probably need to change it)
        device.assignKey(KeyCode.SW2_RELEASE, [])

        #Button3 (left, second from top)
        device.sendIconFor(3, "icons/upc-scan.png")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_I)]) #Cut to content (this shortcut appears to be language dependent, so you will probably need to change it)
        device.assignKey(KeyCode.SW3_RELEASE, [])

        #Button4 (left, third from top)
        device.sendIconFor(4, "icons/crop.png")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L)]) #Canvas size (this shortcut appears to be language
        device.assignKey(KeyCode.SW4_RELEASE, [])

        #Button5 (bottom left)
        device.sendIconFor(5, "icons/arrows-angle-expand.png")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_ALT, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_S)]) #Resize (this shortcut appears to be language
        device.assignKey(KeyCode.SW5_RELEASE, [])

        #Button6 (top right)
        device.sendIconFor(6, "icons/clipboard-plus.png")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_V), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #Paste as new image
        device.assignKey(KeyCode.SW6_RELEASE, [])

        #Button7 (right, second from top)
        device.sendIconFor(7, "icons/layers-half.png")
        device.assignKey(KeyCode.SW7_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_N), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #New layer
        device.assignKey(KeyCode.SW7_RELEASE, [])

        #Button8 (right, third from top)
        device.sendIconFor(8, "icons/arrows-fullscreen.png")
        device.assignKey(KeyCode.SW8_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)]) #Zom to fill screen
        device.assignKey(KeyCode.SW8_RELEASE, [])

        #Button9 (bottom right)
        device.sendIconFor(9, "icons/dot.png")
        device.assignKey(KeyCode.SW9_PRESS, []) #Not used, set to nothing.
        device.assignKey(KeyCode.SW9_RELEASE, [])


        self.jogFunction = ""

        #This toggles the jog function and sets up key assignments and the label for the jog dial. It calls "updateDiplay()" if update is not explicitly set to False (for example if you need to update more parts of the display before updating it.)
        def toggleJogFunction(update=True):
            if self.jogFunction == "size":  #Tool opacity in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Tool opacity")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_COMMA), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_PERIOD), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_SHIFT, ActionCode.RELEASE)])
                self.jogFunction = "opacity"
                if update:
                    device.updateDisplay()
            else:                            #Tool size in GIMP
                device.clearCallback(KeyCode.JOG)
                device.sendTextFor(1, "Tool size")
                device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_BRACE)])
                device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT_BRACE)])
                self.jogFunction = "size"
                if update:
                    device.updateDisplay()


        #Button 1 / jog dial press
        device.registerCallback(toggleJogFunction, KeyCode.JOG_PRESS) #Call "toggleJogFunction" if the dial is pressed
        device.assignKey(KeyCode.SW1_PRESS, [])                       #We do not send a key stroke when the dial is pressed, instead we use the callback.
        device.assignKey(KeyCode.SW1_RELEASE, [])                     #We still need to overwrite the assignment to clear previously set assignments.
        toggleJogFunction(False)    #We call toggleJogFunction to initially set the label and assignment
        device.updateDisplay()      #Everything has been sent to the display. Time to refresh it.

    def poll(self, device):
        return False #Nothing to poll

    def animate(self, device):
        device.fadeLeds() #No LED animation is used in this mode, but we call "fadeLeds" anyway to fade colors that have been set in another mode before switching

    def deactivate(self, device):
        device.clearCallbacks() #Remove our callbacks if we switch to a different mode




        ############## This mode is used as a fallback and a much more complex example than Gimp. It also uses a switchable Jog dial,
        ## Fallback ## but most of its functions give a feedback via LED. Also, we use MQTT (via a separately defined class) to get
        ############## data from a CO2 sensor and control a light (both including feedback)

class ModeFallback:

    def __init__(self):
        pass

    def activate(self, device):
        if DEBUG:
            print("Clearscreen")
        device.sendTextFor(0, "000000 333333 888888") #Title
        
        leds = []
        for x in range(15):
            leds.append(0x222222)
        device.setLeds( leds)
        

        device.sendTextFor(1, "I inpoint")
        device.setKeyLedFor(1,"FF0000")
        
        device.assignKey(KeyCode.SW1_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_I, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.SW1_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_I, ActionCode.RELEASE)])

        #Button2 (top left)
        
        device.sendTextFor(2, "^B cut")
        device.setKeyLedFor(2,"888822")
        device.assignKey(KeyCode.SW2_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.PRESS), event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B, ActionCode.PRESS),event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_B, ActionCode.RELEASE),event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT_CTRL, ActionCode.RELEASE)]) #Zoom to fill screen
        device.assignKey(KeyCode.SW2_RELEASE, [])

        #Button3 (left, second from top)

        device.sendTextFor(3, "O outpoint")
        device.setKeyLedFor(3,"FF0000")
        device.assignKey(KeyCode.SW3_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_O, ActionCode.PRESS)]) #Isolation view
        device.assignKey(KeyCode.SW3_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_O, ActionCode.RELEASE)])


        #Button4 (left, third from top)
        device.sendTextFor(4, "J pl. back")
        device.setKeyLedFor(4,"00FF00")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J, ActionCode.PRESS)]) #Isolation view
        device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J, ActionCode.RELEASE)])


        #Jog dial rotation
        device.sendTextFor(7, "left(right")
        device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)]) #CW = Clock-wise, one frame forward
        device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)]) #CCW = Counter clock-wise, one frame back   
        
        #Button5 (bottom left)
        device.sendTextFor(5, "K stop")
        device.setKeyLedFor(5,"00FF00")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_K, ActionCode.PRESS)]) #Isolation view
        device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_K, ActionCode.RELEASE)])

        #Button6 (top right)
        
        device.sendTextFor(6, "L Stop")
        device.setKeyLedFor(6,"00FF00")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L, ActionCode.PRESS)]) #Isolation view
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L, ActionCode.RELEASE)])

        device.assignKey(KeyCode.JOG_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.JOG_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_SPACE, ActionCode.RELEASE)])




    def poll(self, device):
        return False
    #Called to update the icon of button 4, showing the state of the office light (as if I couldn't see it in the real room, but it is a nice touch to update the display accordingly)

    def animate(self, device):
        pass

    def deactivate(self, device):
        pass

class ModeDaVinciCut:

    def __init__(self):
        pass

    def activate(self, device):
        device.sendTextFor(0, "AAAAAA 080808 000000") #Clearscreen

        device.setLeds ("")

        
        print("Activating Mode Davinci")

        #Button4 (left, third from top)
        device.sendTextFor(4,"J back <<")
        device.setKeyLedFor(4,"FF0000")
        device.assignKey(KeyCode.SW4_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_J, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.SW4_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_K, ActionCode.RELEASE)])

        device.sendTextFor(5,"K stop")
        device.setKeyLedFor(5,"00FF00")
        device.assignKey(KeyCode.SW5_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_K, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.SW5_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_K, ActionCode.RELEASE)])

        device.sendTextFor(6,"K stop")
        device.setKeyLedFor(6,"0000FF")
        device.assignKey(KeyCode.SW6_PRESS, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L, ActionCode.PRESS)]) #Play/pause
        device.assignKey(KeyCode.SW6_RELEASE, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_L, ActionCode.RELEASE)])

        #Jog dial rotation
        device.assignKey(KeyCode.JOG_CW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_RIGHT)]) #CW = Clock-wise, one frame forward
        device.assignKey(KeyCode.JOG_CCW, [event(DeviceCode.KEYBOARD, KeyboardKeycode.KEY_LEFT)]) #CCW = Counter clock-wise, one frame back

        #Button1
        device.assignKey(KeyCode.SW1_PRESS, []) #Set view to camera
        device.assignKey(KeyCode.SW1_RELEASE, [])

        #Button2
        device.assignKey(KeyCode.SW2_PRESS, []) #Set view to camera
        device.assignKey(KeyCode.SW2_RELEASE, [])

        #Button3
        device.assignKey(KeyCode.SW3_PRESS, []) #Set view to camera
        device.assignKey(KeyCode.SW3_RELEASE, [])
        
        leds = []
        for x in range(6):
            leds.append([0x222222]  )
        device.setLeds( leds)

    def poll(self, device):
        return False
    #Called to update the icon of button 4, showing the state of the office light (as if I couldn't see it in the real room, but it is a nice touch to update the display accordingly)

    def animate(self, device):
        pass

    def deactivate(self, device):
        pass






