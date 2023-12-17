import cv2
import numpy as np
import argparse
from pathlib import Path

window_name = 'Apply Canny edge detector'

def main(img_path):
    thresh = [0, 255]
    img_orig = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    height, width, _ = img_orig.shape

    def redraw():
        img = np.copy(img_gray)
        canny_img = cv2.Canny(img, *thresh)
        grid = np.zeros((height, 2 * width, 3), dtype=np.uint8)

        # Place each image in the corresponding grid position
        grid[0:height, 0:width] = img_orig
        grid[0:height, width:2*width] = cv2.cvtColor(canny_img, cv2.COLOR_GRAY2BGR)

        cv2.imshow(window_name, grid)
    
    def on_min_thresh_change(val):
        thresh[0] = val
        redraw()
    
    def on_max_thresh_change(val):
        thresh[1] = val
        redraw()
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.createTrackbar('thresh_min', window_name, 0, 255, on_min_thresh_change)
    cv2.createTrackbar('thresh_max', window_name, 0, 255, on_max_thresh_change)
    redraw()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command line tool to test Canny Edge algorithm thresholds")

    parser.add_argument(
        "-i",
        "--input_image",
        type=str,
        required=True,
        help="The path to the input image file")
    args = parser.parse_args()

    if not Path(args.input_image).is_file():
        raise ValueError(f"Error! File: {args.input_image} doesn't exist on disk!")
    
    main(args.input_image)
