import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread("img.png")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

avg_blur = cv.blur(img, (9, 9))
med_blur = cv.medianBlur(img, 9)
gauss_blur = cv.GaussianBlur(img, (9,9), 0)

avg_canny = cv.Canny(avg_blur, 70, 90)
med_canny = cv.Canny(med_blur, 80, 200)
gauss_canny = cv.Canny(gauss_blur, 60, 160)

# cv.imshow("Canny_avg", avg_canny)
# cv.imshow("Canny_med", med_canny)
# cv.imshow("Canny_gauss", gauss_canny)

# cv.imshow("original", img)
# cv.imshow("avg_blur", avg_blur)
# cv.imshow("med_blur", med_blur)
# cv.imshow("gauss_blur", gauss_blur)
# cv.waitKey(0)
# cv.destroyAllWindows()

fig, axes = plt.subplots(2, 4, figsize=(18, 9))
 
axes[0, 0].imshow(img, cmap="gray")
axes[0, 0].set_title("Original")
 
axes[0, 1].imshow(avg_blur, cmap="gray")
axes[0, 1].set_title("Average Blur")
 
axes[0, 2].imshow(med_blur, cmap="gray")
axes[0, 2].set_title("Median Blur")
 
axes[0, 3].imshow(gauss_blur, cmap="gray")
axes[0, 3].set_title("Gaussian Blur")
 
axes[1, 0].imshow(img, cmap="gray")
axes[1, 0].set_title("Original")
 
axes[1, 1].imshow(avg_canny, cmap="gray")
axes[1, 1].set_title("Canny Average")
 
axes[1, 2].imshow(med_canny, cmap="gray")
axes[1, 2].set_title("Canny Median")
 
axes[1, 3].imshow(gauss_canny, cmap="gray")
axes[1, 3].set_title("Canny Gaussian")
 
for ax_row in axes:
    for ax in ax_row:
        ax.axis("off")
 
plt.tight_layout()
plt.show()

