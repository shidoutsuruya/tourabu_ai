import PIL.Image
import cv2
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from typing import *
import sys
FOLDER_PATH = r'C:/Users/Max/Desktop/tourabu_ai'
COLOR_DEEP_RED=np.array([175,24,24])
SHADOW_GREEN=np.array([130,170,21])
COLOR_BLACK=np.array([35,6,2])
KOHAN_GREEN=np.array([54,160,99])
TEGATA_GRAY=np.array([190,190,186])
KOIKOI_GREEN=np.array([3,117,44])
KOIKOI_BLUE=np.array([96,131,182])
KOIKOI_RED=np.array([206,65,63])
TOUKEN_BLUE=np.array([27,106,255])
CONTINUE_ORANGE=np.array([222,108,15])
SHINAN_GREEN=np.array([132,170,22])
ALERT_RED=np.array([250,40,41])
KATANA_NAVY=np.array([62,90,125])
FORMATION_BLUE=np.array([27,106,255])
class decide:
    #when playing, 80% of the website in google chrome
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
        pyautogui.doubleClick(x,y,interval=0.25)
        return
    def start(self):
        #select butai
        position1=([1500,882],[1592,881],[1520,949])
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
        mask=np.all(np.abs(self.img[..., :3]-SHADOW_GREEN)==0, axis=-1)
        is_green_color=np.any(mask)
        if is_green_color:
            coordinate=np.column_stack(np.where(mask))  # rows (y), cols (x)
            #filter row and column
            region = (coordinate[:, 0]>800) & (coordinate[:, 1]<1100)
            filtered = coordinate[region]
            if filtered.shape[0]==0:
                print("no green click")
                return
            xys = filtered[:, ::-1]  # to (x, y)
            xy_mean = xys.mean(axis=0).astype(int)
            pyautogui.doubleClick(xy_mean[0], xy_mean[1], interval=0.25)
            print("green click")
            #cv2.circle(self.img,x_means,5,(0,0,255),5)
            #plt.imshow(self.img)
            #plt.show()
            return self.green_click()
        else:
            return
    def satsu_select(self):
        time.sleep(0.5)
        self.image_catch()
        image=self.img
        #check whether is the selection part sinan green
        position=([1517,849],[1517,870],[1517,882])
        if self.position_color_check(position,SHINAN_GREEN)==3:
        #check koikoi satsu
            is_target_color=np.any(np.all(image==KOIKOI_GREEN,axis=-1))
            if is_target_color:
                self.koikoi_agari()
            else:
                self.random_select(765,1137,427,590) 
        return
    def random_select(self,x_min,x_max,y_min,y_max):
        x=np.random.randint(x_min,x_max)
        y=np.random.randint(y_min,y_max)
        print(f"random click ({x},{y})")
        pyautogui.doubleClick(x,y,interval=0.25)
    def black_satsu_click(self):
        time.sleep(0.5)
        self.image_catch()
        #trigger by black satsu
        position=([348,336],[408,335],[505,329])
        is_trigger=0
        for p in position:
            if np.all(COLOR_BLACK-50<=self.img[p[1],p[0]])\
                and np.all(COLOR_BLACK+50>=self.img[p[1],p[0]]):
                    is_trigger+=1
        if int(is_trigger)==3:
            print("black satsu detected")
            #preprocess
            gray=cv2.GaussianBlur(self.img,(5,5), 0)
            gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
            gray=cv2.threshold(gray, 100, 255,cv2.THRESH_BINARY)[1]
            #detect edges
            edges=cv2.Canny(gray,30,200)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            contours,_=cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #store rectangle coordinates
            rects=[]
            for c in contours:
                #filter small contours
                if cv2.contourArea(c)>10000:
                    epsilon=0.03*cv2.arcLength(c, True)
                    approx=cv2.approxPolyDP(c, epsilon, True)
                    if len(approx)==4:
                        cv2.drawContours(self.img,[approx],0,(0,255,0),2)
                        rects.append(approx)
            #click card
            new_rects=[rect for i, rect in enumerate(rects) if i % 2 != 0]
            print(len(new_rects))
            if len(new_rects)>0:
                for r in new_rects:
                    x,y,w,h=cv2.boundingRect(r)
                    center=(x+w//2,y+h//2)
                    #for real click
                    pyautogui.click(center[0],center[1])
                    cv2.circle(self.img,center,5,(0,0,255),2)
                    time.sleep(0.5) 
        return 
    def koikoi_agari(self):
        time.sleep(0.5)
        self.image_catch()
        print("koikoi detected")
        image=self.img
        #check koikoi exist
        mask=np.all(image==KOIKOI_BLUE,axis=-1)
        is_blue_color=np.any(mask)
        if is_blue_color:
            coordinate=np.column_stack(np.where(mask))
            x_ys=coordinate[:,::-1]
            x_ys3=x_ys[:3]
            for c in x_ys3:
                #click koikoi
                pyautogui.doubleClick(c[0],c[1])
                #cv2.circle(image,tuple(c),5,(0,0,255),5)
        #check agari
        mask=np.all(image==KOIKOI_RED,axis=-1)
        is_red_color=np.any(mask)
        if is_red_color:
            coordinate=np.column_stack(np.where(mask))
            x_ys=coordinate[:,::-1]
            x_ys3=x_ys[:3]
            for c in x_ys3:
                #click agari
                pyautogui.doubleClick(c[0],c[1])
                #cv2.circle(image,tuple(c),5,(0,0,255),5)
        #plt.imshow(image)
        #plt.show()
    def continue_run(self): 
        time.sleep(0.5)
        self.image_catch()
        image=self.img
        position=([1572,254],[1540,288],[1591,291])
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
            #print(rects)
            centroid=rects[0].mean(axis=0)
            centroid=tuple(centroid.flatten().astype(int))
            #CLICK
            pyautogui.doubleClick(centroid[0],centroid[1])
            cv2.circle(image,centroid,5,(0,0,255),5)
    def continue_check(self):
        time.sleep(0.5)
        self.image_catch()
        position=([1411,833],[1481,828],[1467,880])
        self.position_color_check(position,CONTINUE_ORANGE,isClick=True)
    def find_new_katana(self):
        position=([[1492,793],[1531,791],[1542,813]])
        if self.position_color_check(position,KATANA_NAVY)==3:
            print("find new katana trigger")
            self.normal_click(949,694)
    def team_formation_selection(self):
        self.image_catch()
        team_blue_position=([515,395],[949,395],[1390,395],[515,606],[949,606],[1390,606])
        click_position=(490,680)
        if self.position_color_check(team_blue_position,FORMATION_BLUE)>=3:
            print("select formation")
            pyautogui.click(click_position[0],click_position[1])
if __name__=="__main__":
    while True:
        test=decide(os.path.join(FOLDER_PATH,"1.png"))
        test.start()
        test.satsu_select()
        test.team_formation_selection()
        test.continue_run()
        test.black_satsu_click()
        test.continue_check()
        test.find_new_katana()
        test.normal_click()
