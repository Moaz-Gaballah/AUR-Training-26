import numpy as np
import cv2 as cv 

HEIGHT = 800
WIDTH = 600

OFF_COLOR = (20, 20, 30)
ON_COLOR = (255, 220, 120)

img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

img[:] = (25, 25, 40)
img[int(0.85 * HEIGHT): , :] = (30, 50, 35)
img[int(HEIGHT * 0.1): int(HEIGHT*0.9), int(WIDTH * 0.2): int(WIDTH*0.8)] = (90, 90,100)

def draw_window(img, i, j, color):
     y0 = int(HEIGHT * 0.1) + i*100 + 20
     y1 = int(HEIGHT * 0.1) + i*100 + 70
     x0 = int(WIDTH * 0.2) + j*75 + 15
     x1 = int(WIDTH * 0.2) + j*75 + 45

     img[y0: y1, x0:x1] = color 

register = [(i, j) for i in range(6) for j in range(5)]

for (i, j) in register:
     draw_window(img, i, j, OFF_COLOR)


while True:
     for (i, j) in register:
          draw_window(img, i, j, OFF_COLOR)

     indices = np.random.choice(30, size=4, replace=False)    

     for index in indices:
          i, j = register[index]
          draw_window(img, i, j, ON_COLOR)

     cv.imshow("img", cv.cvtColor(img, cv.COLOR_RGB2BGR))

     if cv.waitKey(1000) == 27: 
          break


cv.destroyAllWindows()





