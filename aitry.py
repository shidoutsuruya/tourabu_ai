import PIL.Image
import cv2
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from typing import *
FOLDER_PATH = r'C:/Users/Max/Desktop/hihou_test'
COLOR_DEEP_RED=np.array([157,24,25,255])
SHADOW_GREEN=np.array([118,155,19,255])
COLOR_BLACK=np.array([5,5,5,255])
KOHAN_GREEN=np.array([54,161,102,255])
TEGATA_GRAY=np.array([190,190,186,255])
KOIKOI_GREEN=np.array([11,135,45,255])
KOIKOI_BLUE=np.array([99,127,178,255])
KOIKOI_RED=np.array([195,56,69,255])
TOUKEN_BLUE=np.array([20,90,190,255])
CONTINUE_ORANGE=np.array([255,165,0,255])
SHINAN_GREEN=np.array([0,255,0,255])

class decide:
    def __init__(self,img_path:str):
        self.img=(plt.imread(img_path)*255).astype(np.uint8)
        self.img_path=img_path
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
                print(f"click ({p[0]},{p[1]})")
                #pyautogui.click(p[0],p[1])    
        return count
    def normal_click(self):
        #click
        x=np.random.randint(0,1920)
        y=np.random.randint(0,1080)
        print(f"click ({x},{y})")
        #pyautogui.click((x,y))
        return
    def buy(self):
        #detect lack of money
        time.sleep(2)
        self.image_catch()
        position_tegata_gray=([1614,812],[1682,814],[1770,816])
        #buy kohan
        if self.position_color_check(position_tegata_gray,TEGATA_GRAY)==3:
            position1=([1614,812],[1682,814],[1770,816])
            self.position_color_check(position1,KOHAN_GREEN,isClick=True)
            time.sleep(2)
            self.image_catch()
            position2=([1614,812],[1682,814],[1770,816])
            self.position_color_check(position2,SHADOW_GREEN,isClick=True)
            return self.buy()    
        else:
            return  
    def start(self):
        #select butai
        position1=([1360,711],[1460,722],[1357,789])
        time.sleep(2)
        self.image_catch()
        self.position_color_check(position1,COLOR_DEEP_RED,isClick=True)
        #iza syutsujin
        position2=([1614,812],[1682,814],[1770,816])
        time.sleep(2)
        self.image_catch()
        self.position_color_check(position2,SHADOW_GREEN,isClick=True)
        #green position
        position3=([656,675],[750,672],[841,679])
        time.sleep(2)
        self.image_catch()
        self.position_color_check(position3,SHADOW_GREEN,isClick=True)
        self.green_click()
    def green_click(self):
        time.sleep(2)
        self.image_catch()
        mask=np.all(self.img==SHADOW_GREEN,axis=-1)
        is_green_color=np.any(mask)
        if is_green_color:
            coordinate=np.column_stack(np.where(mask))
            x_ys=coordinate[:,::-1]
            x_means=x_ys.mean(axis=0).astype(int)
            print("xmeans",x_means)
            cv2.circle(self.img,x_means,5,(0,0,255),5)
            #plt.imshow(self.img)
            #plt.show()
            return self.green_click()
        else:
            return
    def satsu_select(self):
        time.sleep(2)
        self.image_catch()
        image=self.img
        #check whether is the selection part sinan green
        position=([0,0],[1,1],[2,2])
        if self.position_color_check(position,SHINAN_GREEN)==3:
        #check koikoi satsu
            is_target_color=np.any(np.all(image==KOIKOI_GREEN,axis=-1))
            if is_target_color:
                self.koikoi_agari()
            else:
                self.random_select(0,1920,0,1080) 
        return
    def random_select(self,x_min,x_max,y_min,y_max):
        x=np.random.randint(x_min,x_max)
        y=np.random.randint(y_min,y_max)
        print(f"click ({x},{y})")
        #pyautogui.click((x,y))
    def select_method1(self,image):
        print("satsu select detected")
        gray = cv2.GaussianBlur(image,(3,3), 0)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        gray=cv2.threshold(gray,15,255,cv2.THRESH_BINARY)[1]
        #detect edges
        edges=cv2.Canny(gray,30,200)
        """
        plt.imshow(edges)
        plt.show()
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours,_=cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #store rectangle coordinates
        rects=[]
        for c in contours:
            #filter small contours
            if cv2.contourArea(c) <25000:
                continue
            epsilon=0.03*cv2.arcLength(c, True)
            approx=cv2.approxPolyDP(c, epsilon, True)
            if len(approx)==4:
                cv2.drawContours(image,[approx],0,(255,0,0),2)
                rects.append(approx)
        if len(rects)>0:
        #click card
            for r in rects:
                x,y,w,h=cv2.boundingRect(r)
                center=(x+w//2,y+h//2)
                #for real click
                cv2.circle(image,center,5,(0,0,255),2)
        else:
            self.normal_click()
        #plt.imshow(image)
        #plt.show()
    def black_satsu_click(self):
        time.sleep(2)
        self.image_catch()
        position=([226,571],[1226,265],[205,241])
        is_trigger=0
        for p in position:
            if np.all(COLOR_BLACK<=self.img[p[1],p[0]])\
                and np.all(COLOR_BLACK+50>=self.img[p[1],p[0]]):
                    is_trigger+=1
        if int(is_trigger)==3:
            print("black satsu detected")
            #preprocess
            gray = cv2.GaussianBlur(self.img,(5,5), 0)
            gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
            gray= cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            #detect edges
            edges=cv2.Canny(gray,30,200)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            contours,_=cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #store rectangle coordinates
            rects=[]
            for c in contours:
                #filter small contours
                if cv2.contourArea(c) < 6000:
                    continue
                epsilon=0.03*cv2.arcLength(c, True)
                approx=cv2.approxPolyDP(c, epsilon, True)
                if len(approx)==4:
                    cv2.drawContours(self.img,[approx],0,(0,255,0),2)
                    rects.append(approx)
            #click card
            if len(rects)>0:
                for r in rects:
                    x,y,w,h=cv2.boundingRect(r)
                    center=(x+w//2,y+h//2)
                    #for real click
                    cv2.circle(self.img,center,5,(0,0,255),2)
                    time.sleep(1)
            """
            plt.imshow(self.img)
            plt.show()
            """
        return 
    def koikoi_agari(self):
        time.sleep(2)
        self.image_catch()
        print("koikoi detected")
        image=self.img
        #check koikoi exist
        mask=np.all(image==KOIKOI_BLUE,axis=-1)
        is_blue_color=np.any(mask)
        if is_blue_color:
            coordinate=np.column_stack(np.where(mask))
            x_ys=coordinate[:,::-1]
            for c in x_ys:
                #click koikoi
                cv2.circle(image,tuple(c),5,(0,0,255),5)
        #check agari
        mask=np.all(image==KOIKOI_RED,axis=-1)
        is_red_color=np.any(mask)
        if is_red_color:
            coordinate=np.column_stack(np.where(mask))
            x_ys=coordinate[:,::-1]
            for c in x_ys:
                #click agari
                cv2.circle(image,tuple(c),5,(0,0,255),5)
        #plt.imshow(image)
        #plt.show()
    def continue_run(self): 
        time.sleep(2)
        self.image_catch()
        image=self.img
        position=([1435,28],[1450,61],[1452,80])
        if self.position_color_check(position,TOUKEN_BLUE)==3:
            print("comtined run detected")
            gray=cv2.GaussianBlur(image,(3,3), 0)
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            gray=cv2.threshold(gray,150,255,cv2.THRESH_TRUNC)[1]
            edges=cv2.Canny(gray,40,200)
            #plt.imshow(edges)
            #plt.show()
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            contours,_=cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #store rectangle coordinates
            rects=[]
            for c in contours:
                #filter small contours
                if cv2.contourArea(c)>30000 and cv2.contourArea(c)<45000:
                    epsilon=0.04*cv2.arcLength(c, True)
                    approx=cv2.approxPolyDP(c, epsilon, True)
                    if len(approx)==6:
                        cv2.drawContours(image,[approx],0,(255,255,0),10)
                        rects.append(approx)
            centroid=rects[0].mean(axis=0)
            centroid=tuple(centroid.flatten().astype(int))
            #CLICK
            cv2.circle(image,centroid,5,(0,0,255),5)
            #plt.imshow(image)
            #plt.show()
    def continue_check(self):
        time.sleep(2)
        self.image_catch()
        position=([1000,1000],[1000,1000],[1000,1000])
        self.position_color_check(position,CONTINUE_ORANGE,isClick=True)
if __name__=="__main__":
    #test=decide(os.path.join(FOLDER_PATH,"kohan1.png"))
    #test.start()
    """
    while True:
        image_catch()
        test=decide(os.path.join(FOLDER_PATH,"screenshot.png"))
        test.buy()
        test.start()
        test.satsu_select()
        test.continue_run()
        test.black_satsu_click()
        test.continue_check()
        test.normal_click()
        image_delete()
        time.sleep(3)
    """