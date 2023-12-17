import cv2
import numpy as np
import argparse
from pathlib import Path

window_name = 'Apply Hough detection algorithm'

def main(img_path):
    # canny par:
    canny_thresh = [0, 255]
    # hough parameters:
    hough_pars = {
        "rho": 1,
        "theta": 1,
        "threshold_intersections": 1,
        "min_line_length": 1,
        "max_line_gap": 1
    }

    
    img_orig = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    height, width, _ = img_orig.shape

    def redraw():
        img = np.copy(img_gray)
        canny_img = cv2.Canny(img, *canny_thresh)
        lines = cv2.HoughLinesP(
            canny_img,
            hough_pars["rho"], hough_pars["theta"] * np.pi / 180,
            hough_pars["threshold_intersections"], np.array([]),
            hough_pars["min_line_length"], hough_pars["max_line_gap"])
        
        grid = np.zeros((height, 3 * width, 3), dtype=np.uint8)
    
        
        # Place each image in the corresponding grid position
        grid[0:height, 0:width] = img_orig
        grid[0:height, width:2*width] = cv2.cvtColor(canny_img, cv2.COLOR_GRAY2BGR)
        
        hough_img = np.copy(img_orig)
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(hough_img, (x1, y1), (x2, y2), (255,0,0), 5)
        grid[0:height, 2*width:3*width] = hough_img
        cv2.imshow(window_name, grid)
    
    def on_min_canny_thresh_change(val):
        canny_thresh[0] = val
        redraw()
    
    def on_max_canny_thresh_change(val):
        canny_thresh[1] = val
        redraw()

    def on_hough_rho_change(val):
        print(f"New rho: {val}")
        hough_pars["rho"] = val
        redraw()

    def on_hough_theta_change(val):
        hough_pars["theta"] = val
        redraw()

    def on_hough_threshold_intersections_change(val):
        hough_pars["threshold_intersections"] = val
        redraw()

    def on_hough_min_line_length_change(val):
        hough_pars["min_line_length"] = val
        redraw()

    def on_hough_max_line_gap_change(val):
        hough_pars["max_line_gap"] = val
        redraw()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.createTrackbar('canny_thresh_min', window_name, 10, 255, on_min_canny_thresh_change)
    cv2.setTrackbarMin('canny_thresh_min', window_name, 1)

    cv2.createTrackbar('canny_thresh_max', window_name, 50, 255, on_max_canny_thresh_change)
    cv2.setTrackbarMin('canny_thresh_max', window_name, 1)

    cv2.createTrackbar('hough_rho', window_name, 1, 200, on_hough_rho_change)
    cv2.setTrackbarMin('hough_rho', window_name, 1)

    cv2.createTrackbar('hough_theta', window_name, 1, 180, on_hough_theta_change)
    cv2.setTrackbarMin('hough_theta', window_name, 1)

    cv2.createTrackbar('hough_threshold_intersections', window_name, 60, 200, on_hough_threshold_intersections_change)
    cv2.setTrackbarMin('hough_threshold_intersections', window_name, 1)

    cv2.createTrackbar('hough_min_line_length', window_name, 70, 200, on_hough_min_line_length_change)
    cv2.setTrackbarMin('hough_min_line_length', window_name, 1)

    cv2.createTrackbar('hough_max_line_gap', window_name, 5, 200, on_hough_max_line_gap_change)
    cv2.setTrackbarMin('hough_max_line_gap', window_name, 1)

    redraw()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command line tool to test Hough line detection algorithm")

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
