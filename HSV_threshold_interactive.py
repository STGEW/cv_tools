import cv2
import numpy as np


lower = np.array([0, 0, 0])
upper = np.array([0, 0, 0])

img_path = "water_balloons.jpg"
img_orig = cv2.imread(img_path)

window_name = 'Apply HSV thresholds'
height, width, _ = img_orig.shape

def redraw():
    img = np.copy(img_orig)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, lower, upper)
    img[mask != 0] = [0, 0, 0]

    # Create a blank canvas to arrange the images in a grid
    grid = np.zeros((height, 3 * width, 3), dtype=np.uint8)

    # Place each image in the corresponding grid position
    grid[0:height, 0:width] = img_orig
    grid[0:height, width:2*width] = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    grid[0:height, 2*width:3*width] = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

    cv2.imshow(window_name, grid)


def on_hue_min_change(val):
    lower[0] = val
    redraw()

def on_saturation_min_change(val):
    lower[1] = val
    redraw()

def on_value_min_change(val):
    lower[2] = val
    redraw()

def on_hue_max_change(val):
    upper[0] = val
    redraw()

def on_saturation_max_change(val):
    upper[1] = val
    redraw()

def on_value_max_change(val):
    upper[2] = val
    redraw()
    

 
redraw()
cv2.createTrackbar('hue_min', window_name, 0, 180, on_hue_min_change)
cv2.createTrackbar('saturation_min', window_name, 0, 255, on_saturation_min_change)
cv2.createTrackbar('value_min', window_name, 0, 255, on_value_min_change)
cv2.createTrackbar('hue_max', window_name, 0, 180, on_hue_max_change)
cv2.createTrackbar('saturation_max', window_name, 0, 255, on_saturation_max_change)
cv2.createTrackbar('value_max', window_name, 0, 255, on_value_max_change)
 
cv2.waitKey(0)
cv2.destroyAllWindows()