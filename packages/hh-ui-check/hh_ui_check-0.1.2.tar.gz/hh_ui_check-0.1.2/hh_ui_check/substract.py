# 两图相减法
import cv2
import numpy as np


def getSubstract(image1, image2):
  hh, ww = image1.shape[:2]
  
  hh1, ww1 = image2.shape[:2]

  h=max(hh,hh1)
  w=max(ww,ww1)
  org_image=np.ones((h,w,3),dtype=np.uint8)*255
  trans_image=np.ones((h,w,3),dtype=np.uint8)*255

  org_image[:hh,:ww,:]=image1[:,:,:]
  trans_image[:hh1,:ww1,:]=image2[:,:,:]

  substract_img = trans_image - org_image

  cv2.imwrite('substract.jpg', substract_img)


