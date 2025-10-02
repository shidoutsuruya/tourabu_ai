
import pyautogui
import time
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from typing import *
position=(1473,899)
ALERT_RED=np.array([250,40,41])
FORMATION_BLUE=np.array([27,106,255])
class decide:
    def __init__(self,img_path:str):
        self.close=True
        self.img_path=img_path
    def image_catch(self):
        screenshot=pyautogui.screenshot()
        screenshot.save(self.img_path)
        self.img=(plt.imread(self.img_path)*255).astype(np.uint8)
    def position_color_check(self,position:Tuple[List],
                             color:np.ndarray,
                             isClick:bool=False)->int:
        count=0
        for p in position:
            if np.all(color-20<=self.img[p[1],p[0]])\
                and np.all(color+20>=self.img[p[1],p[0]]):
                count+=1
            if count==3 and isClick:
                pyautogui.click(p[0],p[1])
        return count
    def tired_check(self):
        self.image_catch()
        red_position=([688,665],[706,671],[834,658])
        if self.position_color_check(red_position,ALERT_RED)>=2:
            print("tired detected")
            if self.close:
                #close chrome
                os.system("taskkill /im chrome.exe /f")
                time.sleep(5)
                #computer will close
                os.system("shutdown /s /t 200")
            sys.exit()
    def team_formation_selection(self):
        self.image_catch()
        team_blue_position=([519,422],[955,484],[1395,424],[517,697],[943,634],[1387,635])
        click_position=(465,705)
        if self.position_color_check(team_blue_position,FORMATION_BLUE)>=3:
            print("select formation")
            pyautogui.click(click_position[0],click_position[1])
        
        
while True:
    pyautogui.click(position)
    d=decide(r"C:\Users\Max\Desktop\tourabu_ai\1.png")
    d.image_catch()
    d.team_formation_selection()
    d.tired_check()
    time.sleep(2)
