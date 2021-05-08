import cv2
import numpy as np
import lab_multis as lm

from utils.datasets import datasets as dt
from utils.general import general as gn
#import general as gn
#import datasets as dt
import os

#C:\Users\carit\PycharmProjects\tutorial\data_2
path_imagenes = '/content/prueba_data/' #'C:/Users/carit/PycharmProjects/tutorial/data_2/'#'C:/Users/carit/Documents/L377506/L377506/oblique/'#
path_save_images = '/content/train/images/'#'C:/Users/carit/PycharmProjects/tutorial/carpetadata/'#
path_save_labels = '/content/train/labels/'
new_center = 0
def crear_texto(img,objeto,w_real,h_real,name,cx,cy,boxes):
    h_label =h_real/img.shape[0]
    w_label = w_real / img.shape[1]
    texto_label = '{} {} {} {} {}'.format(objeto, cx, cy, w_label, h_label)
    doc = open(path_save_labels+name+str(boxes)+'.txt', 'w')
    doc.write(texto_label)

#C:\Users\carit\PycharmProjects\tutorial\datasets.py
for imgs in os.listdir(path_imagenes):
    if imgs.endswith('.jpg'):
        name,flnme = os.path.splitext(imgs)
        if os.path.exists(path_imagenes+name+'.txt'):
            # Leer las imagenes
            img = cv2.imread(path_imagenes+name+'.jpg')
            ancho1 = img.shape[1]
            alto1 = img.shape[0]
            img = cv2.resize(img, (int(ancho1*0.6), int(alto1*0.6)))  # width and height
            img_t = img
            # CARGAR LAS DIMENSIONES
            #print(img.shape)
            ancho = img.shape[1]
            alto = img.shape[0]
            #print(f'ancho:{ancho}, alto:{alto}')
            ##--CARGAR LABELS
            f = open(path_imagenes+name + '.txt')
            labels = np.array([x.split() for x in f.read().strip().splitlines()], dtype=np.float32)
            for boxes in range(labels.shape[0]):
                img_t = img

                if labels.shape[1] == 5:

                    cx_real = int(labels[boxes][1] * ancho)
                    cy_real = int(labels[boxes][2] * alto)
                    w_real = int(labels[boxes][3] * ancho)
                    h_real = int(labels[boxes][4] * alto)
                    #print(name)
                    #print(boxes)
                    #print(f'hreal{h_real}={labels[boxes][4]}*{alto}')
                    objeto = int(labels[boxes][0])
                    h_mod = h_real *1.1
                    w_mod = w_real*1.1
                    #print(f'cx: {cx_real},cy:{cy_real},w_real:{w_real}, h_real:{h_real}')
                    px, py, sx, sy = lm.xywhtoxyxy(cx_real,cy_real,w_mod,h_mod)
                    #print(f'px:{px},py:{py},sx:{sx},sy:{sy}')
                    #print(labels)
                    #print(f'hreal:{h_real}')
                    #print(f'hmod:{h_mod}')
                    h_realn = gn.check_img_size(int(h_mod),32)
                    #print(f'imagen shape inicial:{img.shape}')
                    #print(h_realn)
                    dt.letterbox(img,32)
                    img_t = dt.letterbox(img_t, (h_realn,h_realn), stride=32)[0]
                    #print('nueva shape imagen:')
                    #print(img_t.shape)
                    limy2 = cy_real + int(img_t.shape[0]/2)
                    #print(f'limy1{limy2} = {cy_real} + {int(img_t.shape[0] / 2)}')
                    limy1 = cy_real - int(img_t.shape[0]/2)
                    #print(f'limy1{limy1} = {cy_real} - {int(img_t.shape[0]/2)}')
                    limx2 = cx_real + int(img_t.shape[1] / 2)
                    #print(f'limx2 {limx2}= {cx_real} + {int(img_t.shape[1] / 2)}')
                    limx1 = cx_real - int(img_t.shape[1] / 2)
                    #print(f'limx1 {limx1}= {cx_real} - {int(img_t.shape[1] / 2)}')
                    cx_txt = 0.5
                    cy_txt = 0.5
                    if limx1 < 0:
                        #print('entre0')
                        new_center = int(limx1)
                        new_center /= img_t.shape[1]
                        cx_txt = 0.5+new_center
                        w_real*=0.95
                        limx1 = 0


                    if limx2 > ancho:
                        #print('entre1')

                        new_center = int(limx2-ancho)
                        new_center /= img_t.shape[0]
                        cx_txt = 0.5+ new_center
                        w_real*=0.95
                        limx2 = ancho
                    if limy1 < 0:
                        #print('entre2')
                        new_center = limy1
                        new_center /= img_t.shape[1]
                        cy_txt = 0.5+ new_center
                        h_real *=0.95
                        limy1 = 0

                    if limy2 > alto:
                        #print('entre3')
                        new_center = int(limy2 - alto)
                        new_center /= img_t.shape[0]
                        cy_txt = 0.5 + new_center
                        h_real*=0.95
                        limy2 = alto


                    #print(f'los limites nuevos son: en y:{limy1,limy2}, x:{limx1,limx2}')
                    #cv2.rectangle(img,(px,py),(sx,sy),(255,0,0),5)
                    imgcrop = img[limy1:limy2,limx1:limx2]
                    #print(f'altura:{limy2 - limy1}, ancho:{limx2 - limx1}')
                    #print(f'para crear docs: altura: {h_realn}, w_real:{w_real}')
                    crear_texto(img_t,objeto,w_real,h_real,name,cx_txt,cy_txt,boxes)

                    cv2.imwrite(path_save_images+name+str(boxes)+'.jpg',imgcrop)
                    #print('-----------------')

