import numpy as np
import cv2 as cv

VIDEO_PATH = r"/home/moaz/Desktop/AUR-Training-26/Phase 3/Task 1/video.mp4"

class object_detection():
     def __init__(self, video_path):
          self.video_path = video_path

     def preprocess(self, frame):
          frame_blur = cv.GaussianBlur(frame, (5, 5), 0)
          return cv.cvtColor(frame_blur, cv.COLOR_BGR2HSV)

     def color_mask(self, frame):
          lower_red = np.array([0, 100, 100])
          upper_red = np.array([10, 255, 255])
          mask_red = cv.inRange(frame, lower_red, upper_red)

          lower_blue = np.array([100, 150, 50])
          upper_blue = np.array([140, 255, 255])
          mask_blue = cv.inRange(frame, lower_blue, upper_blue)

          return mask_red, mask_blue

     def detect_shapes(self, mask, target_shape, color_label):
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        detections = []

        for c in contours:
            area = cv.contourArea(c)
            if area < 400:  
                continue

            param =  cv.arcLength(c, True)
            if param == 0:
                continue

            approx = cv.approxPolyDP(c, 0.04 * param, True)
            is_valid_shape = False

            if target_shape == "circle":
                    is_valid_shape = True if len(approx) > 4 else False

            elif target_shape == "square":
                if len(approx) == 4:
                    x, y, w, h = cv.boundingRect(approx)
                    ratio = w / h
                    if 0.8 <= ratio <= 1.2:  
                        is_valid_shape = True

            if is_valid_shape:
               M = cv.moments(c)
               cx = int(M["m10"] / M["m00"])
               cy = int(M["m01"] / M["m00"])
               label = f"{color_label} {target_shape}"
               detections.append({'contour': c, 'centroid': (cx, cy), 'label': label})

        return detections

     def video_process(self):
         cap = cv.VideoCapture(self.video_path)

         while cap.isOpened():
             nxt, frame = cap.read()

             if not nxt:
                 break
             
             hsv = self.preprocess(frame)
             mask_red, mask_blue = self.color_mask(hsv)

             red_circles = self.detect_shapes(mask_red, "circle", "red")
             blue_squares = self.detect_shapes(mask_blue, "square", "blue")

             for det in red_circles + blue_squares:
                    contour = det['contour']
                    cx, cy = det['centroid']
                    label = det['label']

                    draw_color = (255, 255, 255)

                    cv.drawContours(frame, [contour], -1, draw_color, 1)

                    cv.putText(frame, label, (cx - 40, cy - 10),
                              cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

             cv.imshow("Shape Detection", frame)
             if cv.waitKey(30) & 0xFF == 27:
                    break
         cap.release()
         cv.destroyAllWindows()

if __name__ == "__main__":
    detector = object_detection(VIDEO_PATH)
    detector.video_process()