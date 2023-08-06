#!/usr/bin/env python3

import cv2
import numpy as np

# 最大要素数量 默认500
MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15

def alignImages(im1, im2):

  # im2 is reference and im1 is to be warped to match im2
  # note: numbering is swapped in function
 
  # Convert images to grayscale
  im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
   
  # Detect ORB features and compute descriptors.
  # orb 算法
  orb = cv2.ORB_create(MAX_FEATURES)
  keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
  keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
   
  # Match features.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = matcher.match(descriptors1, descriptors2, None)
   
  # Sort matches by score
  # matches.sort(key=lambda x: x.distance, reverse=False)
  matches = sorted(matches, key=lambda x: x.distance, reverse=False)
  # Remove not so good matches
  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]
 
  # Draw top matches
  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
  cv2.imwrite("diff_matches.png", imMatches)
   
  # Extract location of good matches
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)
 
  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt
   
  # Find homography
  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
 
  # Use homography
  height, width, channels = im2.shape
  im1Reg = cv2.warpPerspective(im1, h, (width, height))
   
  return im1Reg, h
 
 
def getDiffImages(image1, image2):
  hh, ww = image1.shape[:2]
  
  # Aligned image will be stored in imReg. 
  # The estimated homography will be stored in h. 
  imReg, h = alignImages(image2, image1)
   
  # Print estimated homography
  # print("Estimated homography : \n",  h)
  
  # Convert images to HSV and get saturation channel
  refSat = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)[:,:,1]
  imSat = cv2.cvtColor(imReg, cv2.COLOR_BGR2HSV)[:,:,1]

  # Otsu threshold
  refThresh = cv2.threshold(refSat, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
  imThresh = cv2.threshold(imSat, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

  # apply morphology open and close
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
  refThresh = cv2.morphologyEx(refThresh, cv2.MORPH_OPEN, kernel, iterations=1)
  refThresh = cv2.morphologyEx(refThresh, cv2.MORPH_CLOSE, kernel, iterations=1).astype(np.float64)
  imThresh = cv2.morphologyEx(imThresh, cv2.MORPH_OPEN, kernel, iterations=1).astype(np.float64)
  imThresh = cv2.morphologyEx(imThresh, cv2.MORPH_CLOSE, kernel, iterations=1)
  
  # get absolute difference between the two thresholded images
  diff = np.abs(cv2.add(imThresh,-refThresh))
  
  # apply morphology open to remove small regions caused by slight misalignment of the two images
  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12,12))
  diff_cleaned = cv2.morphologyEx(diff, cv2.MORPH_OPEN, kernel, iterations=1).astype(np.uint8)

  # Filter using contour area and draw bounding boxes that do not touch the sides of the image
  cnts = cv2.findContours(diff_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  result = image1.copy()
  for c in cnts:
      x,y,w,h = cv2.boundingRect(c)
      if x>0 and y>0 and x+w<ww-1 and y+h<hh-1:
        cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)

  # save images
  cv2.imwrite('diff.png', diff_cleaned)
  cv2.imwrite('diff_result.png', result)


