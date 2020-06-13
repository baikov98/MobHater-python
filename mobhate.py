import cv2
from PIL import ImageGrab
import numpy as np
import pyautogui as pg
import time
time.sleep(2)
template = cv2.imread('111.png', 0)#Mob's health bar template
w, h = template.shape[::-1] #template width and height
def findmob():
    try:
        base_screen = ImageGrab.grab(bbox=(0, 0, 1035, 752))
        #grab image from 0,0 to end of your game window
        base_screen.save('base_screen.png')
        img_rgb = cv2.imread('base_screen.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        #Compares a template against overlapped image regions.
        #The function slides through image, compares the overlapped
        #patches of size w*h against template using the specified method and
        #stores the comparison results in result
        loc = np.where(res >= 0.8)
        #Return indices(i.e x, y) of the elements satisfying the condition is returned
        for pt in zip(*loc[::-1]):
            #Return last x,y from x and y arrays that contains in loc
            x = int(pt[0])
            y = int(pt[1])
        print('Mob x,y=%2s,%3s' % (x,y))
        time.sleep(0.3)
        x,y = ((x+(w/2)), y) #Mob's hp bar's center
        pg.moveTo(x,y)
        time.sleep(0.1)
        pg.mouseDown(button='right')
        time.sleep(0.4)
        pg.mouseUp(button='right')
        time.sleep(0.1)
    except:
        '''Mob not found'''
        pg.keyDown('right')
        time.sleep(0.35)
        pg.keyUp('right')
        time.sleep(1)

def notcombat():
    if pg.pixelMatchesColor(269, 262, (39, 36, 24)):
        #coords from combat status in game
        return True
    else:
        return False

def isfullhp():
    if pg.pixelMatchesColor(395, 242, (0, 212, 0)):
        #Coords from 90% point of hp bar in game
        return True
    else:
        return False

def relax():
    pg.moveTo(10,10)#Move cursor out for not interrupt matchTemplate
    pg.press('5') #Buff button
    time.sleep(0.5)
    pg.press('6') # /Sit macros button
    while not isfullhp():
        time.sleep(2)

def startcombat():
    pg.press('2') #Warrior's 'Charge' that skip random barriers
    while not notcombat():
        pg.press('3') #Attack button
        time.sleep(0.2)
        pg.press('2')
    relax()
