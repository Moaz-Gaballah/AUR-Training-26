import cv2 as cv
from collections import defaultdict

img = cv.imread("image.png")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

img_blur = cv.GaussianBlur(img_gray, (5, 5), 0)
edges = cv.Canny(img_blur, 50, 150)

cv.imshow("Edges", edges)
cv.imshow("gray", img_gray)

contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
count = defaultdict(int)
for contour in contours:

     if cv.contourArea(contour) < 200:
          continue

     epsilon = 0.02 * cv.arcLength(contour, True)
     approx = cv.approxPolyDP(contour, epsilon, True)
     vertices = len(approx)

     if vertices == 3:
          shape = "Triangle"
     elif vertices == 4:
          x, y, w, h = cv.boundingRect(approx)
          ratio = w / h
          shape = "Square" if 0.95 <= ratio <= 1.05 else "Rectangle"
     else:
          shape = "Circle"

     count[shape] += 1

     M = cv.moments(contour)

     cx = int(M["m10"] / M["m00"])
     cy = int(M["m01"] / M["m00"])

     if shape == "Circle" or shape == "Triangle":
          cv.putText(img, shape, (cx-30, cy), cv.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 2)
     else:
          cv.putText(img, shape, (cx-40, cy), cv.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 2)
     
for name, n in count.items():
     print(f"{name}: {n}")

cv.imshow("result", img)
cv.waitKey(0)
cv.destroyAllWindows()