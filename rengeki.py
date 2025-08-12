import pyautogui
import matplotlib.pyplot as plt
import time
import numpy as np
import os
from typing import *
import sys
import cv2
FOLDER_PATH = r'C:/Users/Max/Desktop/tourabu_ai'
COLOR_DEEP_RED=np.array([175,24,24])
SHADOW_GREEN=np.array([130,170,21])
KOHAN_GREEN=np.array([54,160,99])
ALERT_RED=np.array([250,40,41])
TOUKEN_BLUE=np.array([27,106,255])
KATANA_NAVY=np.array([62,90,125])
class decide:
    def __init__(self,img_path:str):
        self.img=(plt.imread(img_path)*255).astype(np.uint8)
        self.img_path=img_path
        #close the computer
        self.close=True
    def image_catch(self):
        screenshot = pyautogui.screenshot()
        screenshot.save(self.img_path)
        self.img=(plt.imread(self.img_path)*255).astype(np.uint8)
    def position_color_check(self,position:Tuple[List],
                             color:np.ndarray,
                             isClick:bool=False)->int:
        """get and check button position
        Args:
            position (Tuple[List]): three position of the button([x1,y1],[x2,y2],[x3,y3])
            color (np.ndarray): np.array([r,g,b,a])
            isClick (bool, optional): whether to click the button. Defaults to False.
        Returns:
            int: count the number 
        """
        count=0
        for p in position:
            if np.all(color-20<=self.img[p[1],p[0]])\
                and np.all(color+20>=self.img[p[1],p[0]]):
                count+=1
            if count==3 and isClick:
                pyautogui.click(p[0],p[1])    
        return count
    def normal_click(self,x:int=946,y:int=773):
        #click
        print(f"normal click ({x},{y})")
        pyautogui.doubleClick(x,y,interval=0.1)
        return
    def start(self):
        #select butai
        position1=([1500,900],[1544,900],[1514,972])
        time.sleep(0.5)
        self.image_catch()
        self.position_color_check(position1,COLOR_DEEP_RED,isClick=True)
        #iza syutsujin
        position2=([1614,812],[1682,814],[1770,816])
        time.sleep(0.5)
        self.image_catch()
        self.position_color_check(position2,SHADOW_GREEN,isClick=True)
        #green position
        time.sleep(0.5)
        self.image_catch()
        self.green_click()
    def green_click(self):
        time.sleep(0.5)
        self.image_catch()
        red_position=([703,667],[687,666])
        #detect the katana is tired
        if self.position_color_check(red_position,ALERT_RED,isClick=False)>1:
            print("alert detected!!!")
            if self.close:
                #close chrome
                os.system("taskkill /im chrome.exe /f")
                time.sleep(5)
                #computer will close
                os.system("shutdown /s /t 200")
            sys.exit()
        mask=np.all(np.abs(self.img[..., :3]-SHADOW_GREEN) <= 20, axis=-1)
        is_green_color=np.any(mask)
        if is_green_color:
            coordinate=np.column_stack(np.where(mask))
            #filter the green block where is not the decision button
            filtered= coordinate[coordinate[:, 0]>600]
            if filtered.shape[0]==0:
                print("no green click")
                return
            #remove the light green location where is not the button
            x_ys=filtered[:,::-1]
            x_means=x_ys.mean(axis=0).astype(int)
            pyautogui.doubleClick(x_means[0],x_means[1],interval=0.25)
            print("green click")
            #cv2.circle(self.img,x_means,5,(0,0,255),5)
            #plt.imshow(self.img)
            #plt.show()
            return self.green_click()
        else:
            return    
    def continue_run(self): 
        time.sleep(0.5)
        self.image_catch()
        image=self.img
        position=([1567,280],[1570,340],[1539,314])
        if self.position_color_check(position,TOUKEN_BLUE)==3:
            print("contined run detected")
            gray=cv2.GaussianBlur(image,(3,3), 0)
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            gray=cv2.threshold(gray,150,255,cv2.THRESH_TRUNC)[1]
            edges=cv2.Canny(gray,40,200)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            contours,_=cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #store rectangle coordinates
            rects=[]
            for c in contours:
                #filter small contours
                if cv2.contourArea(c)>20000 and cv2.contourArea(c)<45000:
                    epsilon=0.05*cv2.arcLength(c, True)
                    approx=cv2.approxPolyDP(c, epsilon, True)
                    if len(approx)==6:
                        cv2.drawContours(image,[approx],0,(255,0,0),10)
                        rects.append(approx)
            #calculate centroid
            if len(rects)>0:
                for rect in rects:
                    centroid=rect.mean(axis=0)
                    centroid=tuple(centroid.flatten().astype(int))
                    if 1349<centroid[0]<1515:
                        pyautogui.doubleClick(centroid[0],centroid[1])
                        print(f"click {centroid}")
            #cv2.circle(image,centroid,5,(0,0,255),5)
    def find_new_katana(self):
        position=([[1492,793],[1531,791],[1542,813]])
        if self.position_color_check(position,KATANA_NAVY)==3:
            print("find new katana trigger")
            time.sleep(1)
            self.normal_click(949,694)
if __name__=="__main__":
    while True:
        d=decide(os.path.join(FOLDER_PATH,"1.png"))
        d.start()
        d.continue_run()
        d.find_new_katana()
        d.normal_click(1490,900) #please clear the number when change event  
        time.sleep(5)