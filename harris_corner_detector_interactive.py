import cv2
import numpy as np
import argparse
from pathlib import Path

window_name = 'Apply harris corner detector algorithm'

def main(img_path):
    # harris parameters:
    harris_pars = {
        "blockSize": 2,
        "ksize": 3,
        "k": 0.04,
        "thresh": 0.01
    }

    
    img_orig_bgr = cv2.imread(img_path)
    img_orig_gray = cv2.cvtColor(img_orig_bgr, cv2.COLOR_BGR2GRAY)
    height, width, _ = img_orig_bgr.shape

    def redraw():
        img_gray = np.copy(img_orig_gray)
        img_bgr = np.copy(img_orig_bgr)
        img_gray = np.float32(img_gray)

        # Detect corners 
        img_harris = cv2.cornerHarris(
            img_gray,
            harris_pars['blockSize'],
            harris_pars['ksize'],
            harris_pars['k'])

        # Dilate corner image to enhance corner points
        img_harris = cv2.dilate(img_harris, None)
        # show on the orig img with 
        img_bgr[img_harris > harris_pars['thresh'] * img_harris.max()] = [0, 0, 255]
        
        grid = np.zeros((height, 3 * width, 3), dtype=np.uint8)
    
        # Place each image in the corresponding grid position
        grid[0:height, 0:width] = np.copy(img_orig_bgr)
        grid[0:height, width:2*width] = cv2.cvtColor(img_harris, cv2.COLOR_GRAY2BGR)
        grid[0:height, 2*width:3*width] = img_bgr
        cv2.imshow(window_name, grid)
    
    def on_harris_block_size_change(val):
        harris_pars['blockSize'] = val
        redraw()
    
    def on_harris_ksize_change(val):
        harris_pars['ksize'] = val
        redraw()

    def on_harris_k_change(val):
        harris_pars['k'] = val / 100.0
        redraw()

    def on_harris_thresh_change(val):
        harris_pars['thresh'] = val / 100.0
        redraw()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.createTrackbar('harris_block_size', window_name, 2, 5, on_harris_block_size_change)
    cv2.setTrackbarMin('harris_block_size_min', window_name, 1)
    cv2.setTrackbarMax('harris_block_size_max', window_name, 5)
    
    cv2.createTrackbar('harris_ksize', window_name, 3, 9, on_harris_ksize_change)
    cv2.setTrackbarMin('harris_ksize_max', window_name, 1)
    cv2.setTrackbarMax('harris_ksize_max', window_name, 9)

    cv2.createTrackbar('harris_k', window_name, 4, 15, on_harris_k_change)
    cv2.setTrackbarMin('harris_k', window_name, 1)
    cv2.setTrackbarMax('harris_k', window_name, 15)

    cv2.createTrackbar('harris_thresh', window_name, 1, 100, on_harris_thresh_change)
    cv2.setTrackbarMin('harris_thresh', window_name, 1)
    cv2.setTrackbarMax('harris_thresh', window_name, 100)

    redraw()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command line tool to test Harris corner detector algorithm")

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
