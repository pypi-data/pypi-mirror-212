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

def main():
  curPath = os.path.abspath('.')
  im1Path = os.path.join(curPath, '1.jpg')
  im2Path = os.path.join(curPath, '2.jpg')
  image1 = cv2.imread(im1Path)
  image2 = cv2.imread(im2Path)

  getHorizen(image1, image2)
  getSubstract(image1, image2)
  getOverlapping(image1, image2)
  getDiffImages(image1, image2)
  getHistResult(image1, image2)


if __name__ == '__main__':
  main()
