import cv2
import tkinter as tk
from PIL import Image, ImageTk

class ImageGridApp:
    def __init__(self, master, images):
        self.master = master
        self.images = images
        self.current_image_index = 0

        self.canvas = tk.Canvas(master)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.load_image()

        # Bind arrow keys to image navigation
        master.bind("<Left>", self.prev_image)
        master.bind("<Right>", self.next_image)

    def load_image(self):
        # Convert the image from BGR to RGB
        image = cv2.cvtColor(self.images[self.current_image_index], cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def next_image(self, event):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.load_image()

    def prev_image(self, event):
        self.current_image_index = (self.current_image_index - 1) % len(self.images)
        self.load_image()

if __name__ == "__main__":
    # Read your images
    image1 = cv2.imread('pizza_bluescreen.jpg')
    image2 = cv2.imread('pizza_bluescreen.jpg')
    image3 = cv2.imread('pizza_bluescreen.jpg')
    image4 = cv2.imread('pizza_bluescreen.jpg')

    # Create Tkinter window
    root = tk.Tk()
    root.title("Image Grid Viewer")

    # Create an instance of the ImageGridApp class
    app = ImageGridApp(root, [image1, image2, image3, image4])

    # Start the Tkinter main loop
    root.mainloop()
