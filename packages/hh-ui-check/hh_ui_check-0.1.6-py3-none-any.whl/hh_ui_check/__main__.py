#!/usr/bin/env python3
import sys
import os
import cv2
import numpy as np
sys.path.append(os.getcwd())

from hh_ui_check.horizen import getHorizen
from hh_ui_check.substract import getSubstract
from hh_ui_check.overlapping import getOverlapping
from hh_ui_check.diff import getDiffImages
from hh_ui_check.hist_compare import getHistResult

def existFile(curPath, name):
  imPath = os.path.join(curPath, name + '.png')
  if not os.path.exists(imPath):
    imPath = os.path.join(curPath, name + '.jpg') 
  if not os.path.exists(imPath):
    return (False, '')
  else:
    return True, imPath


def main(dirPath):  
  result1 = existFile(dirPath, '1')
  result2 = existFile(dirPath, '2')

  if result1[0] and result2[0]:
    image1 = cv2.imread(result1[1])
    image2 = cv2.imread(result2[1])
    getHorizen(dirPath, image1, image2)
    getSubstract(dirPath, image1, image2)
    getOverlapping(dirPath, image1, image2)
    getDiffImages(dirPath, image1, image2)
    getHistResult(image1, image2)
  else: 
    print(curPath + '不存在1.png或2.png')

if __name__ == '__main__':
  curPath = os.path.abspath('.')
  print('当前文件夹：')
  main(curPath)
  # 文件夹
  dirs = os.listdir(r'./')
  for dir in dirs: 
    dirPath = os.path.join(curPath, dir)
    if os.path.isdir(dirPath):
      print(dir + '文件夹：')
      main(dirPath)
  
