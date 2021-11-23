import cv2
import math
import numpy as np
from PIL import Image
import os
from datetime import datetime
import werkzeug

class Processing():
    def mask_img(path,img_file):
        cascade_file = "static/xml/haarcascade_mcs_mouth.xml"
        cascade_file02 = "static/xml/haarcascade_mcs_nose.xml"
        cascade_file03 = "static/xml/haarcascade_eye.xml"

        #カスケードファイルを利用した検出器を定義
        cascade = cv2.CascadeClassifier(cascade_file)
        
        cascade02 = cv2.CascadeClassifier(cascade_file02)
        
        
        cascade03 = cv2.CascadeClassifier(cascade_file03)
        #画像ファイルを読み込み
        image_file = cv2.imread(os.path.join(path,img_file))
        if image_file is None:
            return False

        #GrayScaleに変換
        img_gray = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)

        #detectMultiScaleで検出
        face_list = cascade.detectMultiScale(img_gray,1.1,50)
        
        face_list02 = cascade02.detectMultiScale(img_gray,1.1,50)
        
        face_list03 = cascade03.detectMultiScale(img_gray,1.1,50)
        
        if(len(face_list) > 0 and len(face_list02) > 0 and len(face_list03) > 1):
            x01 = face_list[0][0]
            y01 = face_list[0][1]
            w01 = face_list[0][2]
            h01 = face_list[0][3]
            
            
            eye_x01 = face_list03[0][0]
            eye_y01 = face_list03[0][1]
            eye_w01 = face_list03[0][2]
            eye_h01 = face_list03[0][3]
            
            
            eye_x02 = face_list03[1][0]
            eye_y02 = face_list03[1][1]
            eye_w02 = face_list03[1][2]
            eye_h02 = face_list03[1][3]
            

            
            nose_x01 = face_list02[0][0]
            nose_y01 = face_list02[0][1]
            nose_w01 = face_list02[0][2]
            nose_h01 = face_list02[0][3]
            
            
            #位置調整
            eye_x03 = eye_x01 - eye_x02
            eye_y03 = eye_y01 - eye_y02
            tan = eye_y03 / eye_x03
            atan = np.arctan(tan) *180/math.pi
            
            
            im1 = Image.open(os.path.join(path,img_file))
            im2 = Image.open('static/img/mask.png').rotate(-atan,expand=1)
            
            

            
            im22 = im2.resize((math.floor(w01 * 2.0), h01 + nose_h01))
            resize_name = datetime.now().strftime("%Y%m%d_%H%M%S_")+ werkzeug.utils.secure_filename("mask_resize.png")
            
            im22.save(os.path.join(path,resize_name))
            back_im = im1.copy()
            back_im.paste(im22, (math.floor(x01 - (w01 / 2)), nose_y01), im22.split()[0])
            back_im.save(os.path.join(path,"change_" + img_file))
            os.remove(os.path.join(path,resize_name))
            
            return os.path.join("change_" + img_file)
        else:
            return False