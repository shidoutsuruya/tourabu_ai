import PIL.Image
import cv2
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time
import os
FOLDER_PATH = r'C:/Users/Max/Desktop/hihou_test'
COLOR_DEEP_RED=np.array([0.686,0.0941,0.0941])
COLOR_SHADOW_GREEN=np.array([0.51,0.667,0.0824])
COLOR_BLACK=np.array([0.02,0.02,0.02,1])
KOHAN_GREEN=np.array([0.26,0.667,0.0824])
TEGATA_GRAY=np.array([0.74,0.74,0.725,1])
KOIKOI_GREEN=np.array([11,135,45,255])
KOIKOI_BLUE=np.array([99,127,178,255])
KOIKOI_RED=np.array([195,56,69,255])
def image_catch(image_path:str=os.path.join(FOLDER_PATH,"screenshot.png")):
    screenshot = pyautogui.screenshot()
    screenshot.save(image_path)
    return screenshot
def image_delete(image_path:str=os.path.join(FOLDER_PATH,"screenshot.png")):
    import os
    os.remove(image_path)
    print("Image deleted")
    return
class decide:
    def __init__(self,img):
        self.img=plt.imread(img)
    def buy(self):
        position=([280,242],[357,241])
        kohan_buy=0
        for p in position:
            if np.all(TEGATA_GRAY<=self.img[p[1],p[0]])\
                and np.all(TEGATA_GRAY+0.02>=self.img[p[1],p[0]]):
                    kohan_buy+=1
        if int(kohan_buy)==2:
            print("click buy")
            print("click yes")        
        return        
    def start(self):
        #select butao
        position1=([1614,812],[1682,814],[1770,816])
        for p in position1:
            if np.all(COLOR_DEEP_RED<self.img[p[1],p[0]])\
                and np.all(COLOR_DEEP_RED+0.001>self.img[p[1],p[0]]):
                print("Deep red detected")
                #pyautogui.click(p[0],p[1])
            else:
                print("Not deep red")
        #iza syutsujin
        position2=([1614,812],[1682,814],[1770,816])
        for p in position2:
            if np.all(COLOR_DEEP_RED<self.img[p[1],p[0]])\
                and np.all(COLOR_DEEP_RED+0.001>self.img[p[1],p[0]]):
                print("Deep red detected")
                #pyautogui.click(p[0],p[1])
            else:
                print("Not deep red")
        #green position
        position3=([1614,812],[1682,814],[1770,816])
        for p in position3:
            if np.all(COLOR_SHADOW_GREEN<=self.img[p[1],p[0]])\
                and np.all(COLOR_SHADOW_GREEN+0.001>=self.img[p[1],p[0]]):
                print("green detected")
                #pyautogui.click(p[0],p[1])
            else:
                print("not green")
    def satsu_select(self):
        image=self.img*255
        image=image.astype(np.uint8)
        #check koikoi satsu
        is_target_color=np.any(np.all(image==KOIKOI_GREEN,axis=-1))
        if is_target_color:
            self.koikoi_agari()
        else:
            gray = cv2.GaussianBlur(image,(3,3), 0)
            gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            gray=cv2.threshold(gray,15,255,cv2.THRESH_BINARY)[1]
            plt.imshow(gray)
            plt.show()
            #detect edges
            edges=cv2.Canny(gray,30,200)
            plt.imshow(edges)
            plt.show()
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
            print(len(rects))
            #click card
            for r in rects:
                x,y,w,h=cv2.boundingRect(r)
                center=(x+w//2,y+h//2)
                #for real click
                cv2.circle(image,center,5,(0,0,255),2)
            plt.imshow(image)
            plt.show()
    def black_satsu_click(self):
        position=([226,571],[1226,265],[205,241])
        is_trigger=0
        for p in position:
            if np.all(COLOR_BLACK<=self.img[p[1],p[0]])\
                and np.all(COLOR_BLACK+0.1>=self.img[p[1],p[0]]):
                    is_trigger+=1
        if int(is_trigger)==3:
            print("black satsu detected")
            image=self.img*255
            image=image.astype(np.uint8)
            #preprocess
            gray = cv2.GaussianBlur(image,(5,5), 0)
            gray=cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
            gray= cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            #detect edges
            edges=cv2.Canny(gray,30,200)
            plt.imshow(edges)
            plt.show()
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
                    cv2.drawContours(image,[approx],0,(0,255,0),2)
                    rects.append(approx)
            #click card
            for r in rects:
                x,y,w,h=cv2.boundingRect(r)
                center=(x+w//2,y+h//2)
                #for real click
                cv2.circle(image,center,5,(0,0,255),2)
        return 
    def koikoi_agari(self):
        image=self.img*255
        image=image.astype(np.uint8)
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
        plt.imshow(image)
        plt.show()
if __name__=="__main__":
    test1=decide(os.path.join(FOLDER_PATH,"test3.png"))
    #test1.koikoi_agari()
    test1.satsu_select()
    #test1.black_satsu_click()
    """
    while True:
        img=image_catch()
        time.sleep(3)
        decide.test(img)
        #image_delete()
        time.sleep(3)
    """
    #plt.imshow(plt.imread(IMAGE_PATH))
    #plt.show()