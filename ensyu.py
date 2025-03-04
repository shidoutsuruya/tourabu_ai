import pyautogui
import matplotlib.pyplot as plt
import time
import numpy as np
import os
from typing import *
import sys 
import cv2
FOLDER_PATH = r'C:/Users/Max/Desktop/tourabu_ai'
KATANA_NAVY=np.array([62,90,125])
CONTINUE_PURPLE=np.array([140,22,183])
ALERT_RED=np.array([250,40,41])
class decide:
    def __init__(self,img_path:str):
        self.img=(plt.imread(img_path)*255).astype(np.uint8)
        self.img_path=img_path
        self.close=False
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
    def normal_click(self,x:int=946,y:int=733):
        print(f"normal click ({x},{y})")
        pyautogui.doubleClick(x,y,interval=0.1)
        return
    def continue_run(self):
        time.sleep(0.5)
        self.image_catch()
        image=self.img
        position=([1530,288],[1555,310],[1583,311])
        if self.position_color_check(position,CONTINUE_PURPLE)==3:
            print("continue run is detected")
            gray=cv2.GaussianBlur(image,(3,3),0)
            gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
            _,thresh=cv2.threshold(gray,150,255,cv2.THRESH_TRUNC)
            edges=cv2.Canny(thresh,40,200)
            kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
            closed=cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)
            contours,_=cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            rects=[]
            for c in contours:
                if cv2.contourArea(c)>10000 and cv2.contourArea(c)<20000:
                    epsilon=0.05*cv2.arcLength(c,True)
                    approx=cv2.approxPolyDP(c,epsilon,True)
                    if len(approx)==6:
                        cv2.drawContours(image,[approx],0,(255,0,0),10)
                        rects.append(approx)
            rects=np.array(rects)
            centroid=rects.mean(axis=1)
            centroid=centroid.mean(axis=0).astype(int).flatten()
            pyautogui.doubleClick(centroid[0],centroid[1]+100)
            cv2.circle(image,centroid,5,(0,0,255),5)
            #sys.exit()
    def find_new_katana(self):
        position=([[1492,793],[1531,791],[1542,813]])
        if self.position_color_check(position,KATANA_NAVY)==3:
            print("find new katana trigger")
            self.normal_click(949,694)
    def tired_check(self):
        self.image_catch()
        red_position=([703,667],[687,666])
        if self.position_color_check(red_position,ALERT_RED)==2:
            print("tired detected")
            if self.close:
                #close chrome
                os.system("taskkill /im chrome.exe /f")
                time.sleep(5)
                #computer will close
                os.system("shutdown /s /t 200")
            sys.exit()
    def alert_check(self):
        self.image_catch()
        red_position=([714,658],[733,658])
        if self.position_color_check(red_position,ALERT_RED)==2:
            print("alert detected")
            if self.close:
                #close chrome
                os.system("taskkill /im chrome.exe /f")
                time.sleep(5)
                #computer will close
                os.system("shutdown /s /t 200")
            sys.exit()
if __name__=="__main__":
    while True:
        d=decide(FOLDER_PATH+"/screenshot.png")
        d.continue_run()
        d.find_new_katana()
        d.tired_check()
        d.alert_check()
        d.normal_click()
        time.sleep(1)