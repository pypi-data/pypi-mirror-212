#!/usr/bin/env python3

# 两图相减法
import cv2
import numpy as np


def getOverlapping(dirPath, image1, image2):
  hh, ww = image1.shape[:2]
  
  hh1, ww1 = image2.shape[:2]

  h=max(hh,hh1)
  w=max(ww,ww1)
  org_image=np.ones((h,w,3),dtype=np.uint8)*255
  trans_image=np.ones((h,w,3),dtype=np.uint8)*255

  org_image[:hh,:ww,:]=image1[:,:,:]
  trans_image[:hh1,:ww1,:]=image2[:,:,:]

  # substract_img = trans_image - org_image
  # 权重越大，透明度越低
  overlapping = cv2.addWeighted(org_image, 0.7, trans_image, 0.3, 0)
  # 保存叠加后的图片
  cv2.imwrite(dirPath + '/overlapping.jpg', overlapping)


