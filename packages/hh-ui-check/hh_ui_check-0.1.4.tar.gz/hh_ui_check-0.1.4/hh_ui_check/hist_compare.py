#!/usr/bin/env python3

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


def create_rgb_hist(image):
  """"创建 RGB 三通道直方图（直方图矩阵）"""
  h, w, c = image.shape
  # 创建一个（16*16*16,1）的初始矩阵，作为直方图矩阵 
  # 16*16*16的意思为三通道每通道有16个bins
  rgbhist = np.zeros([16 * 16 * 16, 1], np.float32)
  bsize = 256 / 16
  for row in range(h):
    for col in range(w):
      b = image[row, col, 0]
      g = image[row, col, 1]
      r = image[row, col, 2]
      # 人为构建直方图矩阵的索引，该索引是通过每一个像素点的三通道值进行构建
      index = int(b / bsize) * 16 * 16 + int(g / bsize) * 16 + int(r / bsize)
      # 该处形成的矩阵即为直方图矩阵
      rgbhist[int(index), 0] += 1
  # plt.ylim([0, 10000])
  # plt.grid(color='r', linestyle='--', linewidth=0.5, alpha=0.3)
  return rgbhist

def hist_compare(image1, image2):
  """直方图比较函数"""
  # 创建第一幅图的rgb三通道直方图（直方图矩阵）
  hist1 = create_rgb_hist(image1)
  # 创建第二幅图的rgb三通道直方图（直方图矩阵）
  hist2 = create_rgb_hist(image2)
  # 进行三种方式的直方图比较
  match1 = cv.compareHist(hist1, hist2, cv.HISTCMP_BHATTACHARYYA)
  match2 = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
  match3 = cv.compareHist(hist1, hist2, cv.HISTCMP_CHISQR)
  # print("巴氏距离：%s, 相关性：%s, 卡方：%s" %(match1, match2, match3))
  print("相关性评分：%s分" %(int(match2 * 100)))


def getHistResult(image1, image2) :
  # cv.imwrite('compare-1',create_rgb_hist(src1) )
  # cv.imwrite('compare-2',create_rgb_hist(src2) )
  # plt.subplot(1,2,1)
  # plt.title("diff1")
  # plt.plot(create_rgb_hist(src1))
  # plt.subplot(1,2,2)
  # plt.title("diff2")
  # plt.plot(create_rgb_hist(src2))
  hist_compare(image1, image2)
  # plt.show()
  # cv.waitKey(0)
  # while True: 
  #   #do your thing 
  #   if cv.waitKey(0) & 0xFF == ord('q'): 
  #     break #this loop will break if you press 'q', else it'll wait 
  # cv.destroyAllWindows()
