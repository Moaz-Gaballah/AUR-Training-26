import numpy as np
import cv2 as cv

img = cv.imread("img.jpg")

img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

lower_orange = np.array([5, 100, 100])
upper_orange = np.array([25,255,255])

lower_red = np.array([0, 100, 100])
upper_red = np.array([10,255,255])

lower_green = np.array([35, 80, 80])
upper_green = np.array([90,255,255])

orange_mask = cv.inRange(img_hsv, lower_orange, upper_orange)
red_mask = cv.inRange(img_hsv, lower_red, upper_red)
green_mask = cv.inRange(img_hsv, lower_green, upper_green)

img[orange_mask > 0] = [0, 0, 255]
img[red_mask > 0] = [0, 255, 0]
img[green_mask > 0] = [0, 165, 255]

cv.imshow("orange_mask", orange_mask)
cv.imshow("red_mask", red_mask)
cv.imshow("green_mask", green_mask)
cv.imshow("Result", img)

cv.waitKey(0)
cv.destroyAllWindows()
