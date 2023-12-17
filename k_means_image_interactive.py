import cv2
import numpy as np
import argparse
from pathlib import Path

window_name = 'Apply k means algorithm'

def main(img_path):

    # k mean parameters
    k_means_pars = {
        "k": 3,
        "attempts_count": 3
    }
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    
    img_orig_bgr = cv2.imread(img_path)
    img_orig_flat = np.float32(img_orig_bgr.reshape((-1,3)))
    height, width, _ = img_orig_bgr.shape

    def redraw():
        retval, labels, centers = cv2.kmeans(
            img_orig_flat,
            k_means_pars["k"],
            None,
            criteria,
            k_means_pars["attempts_count"],
            cv2.KMEANS_RANDOM_CENTERS)

        centers = np.uint8(centers)
        segmented_data = centers[labels.flatten()]
        
        # reshape data into the original image dimensions
        segmented_image = segmented_data.reshape((img_orig_bgr.shape))
        
        grid = np.zeros((height, 2 * width, 3), dtype=np.uint8)
        
        # Place each image in the corresponding grid position
        grid[0:height, 0:width] = img_orig_bgr
        grid[0:height, width:2*width] = segmented_image
        cv2.imshow(window_name, grid)
    
    def on_k_value_change(val):
        k_means_pars["k"] = val
        redraw()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.createTrackbar('k_value', window_name, 2, 10, on_k_value_change)
    cv2.setTrackbarMin('k_value_min', window_name, 2)
    cv2.setTrackbarMax('k_value_max', window_name, 10)

    redraw()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command line tool to test K means algorithm on an image")

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
