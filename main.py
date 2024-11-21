import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


# Root window class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")
        self.geometry("1280x720")

        # Create main content frame
        self.mainframe = Mainframe(self)
        self.mainframe.grid(column=0, row=0, sticky="nsew")

        # Enable main frame auto-resizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



# Main content frame class
class Mainframe(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Enable content auto-resizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0, pad=5)
        # todo There's extra space below the buttons for some reason

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Create menu bar
        self.open_img_btn = ttk.Button(self, text="Open Image", command=self.open_base_image)
        self.open_img_btn.grid(column=0, row=0, sticky="e")

        self.select_watermark_btn = ttk.Button(self, text="Select Watermark", command= self.open_watermark_image)
        self.select_watermark_btn.grid(column=1, row=0, sticky="w")

        # Create canvas
        self.canvas = tk.Canvas(self, width=500, height=500, background="gray75")
        self.canvas.grid(column=0, row=1, columnspan=2, sticky="nsew")

        # Initialize image variables
        self.base_image_filepath = None
        self.base_image = None

        self.watermark_filepath = None
        self.watermark = None

        self.watermarked_image = None

        self._resize_after_id = None

        # Open an image at initialization
        self.open_base_image()

        # Bind canvas resize event to dynamically resize the image
        self.canvas.bind('<Configure>', self.resize_image)


    # Sets the value of base_image and it's associated filepath, then calls resize_image()
    def open_base_image(self):
        self.base_image_filepath = filedialog.askopenfilename()
        self.base_image = Image.open(self.base_image_filepath)

        # For transparency to work properly with the watermark, the base image must be of type RGB
        self.base_image = self.base_image.convert("RGB")

        self.resize_image()


    # Sets the value of watermark and is associated filepath, then calls save_watermarked_image()
    def open_watermark_image(self):
        self.watermark_filepath = filedialog.askopenfilename()
        self.watermark = Image.open(self.watermark_filepath)
        self.save_watermarked_image()


    # Saves a new image and sets it as the value of self.watermarked image, then calls resize_image()
    def save_watermarked_image(self):
        # todo Avoid hardcoded numbers
        self.base_image.paste(self.watermark, (20, self.base_image.size[1] - 200), mask=self.watermark)
        self.base_image.save("pics/final_image.png")
        self.resize_image()


    def resize_image(self, *args, **kwargs):
        if self._resize_after_id:
            self.after_cancel(self._resize_after_id)

        self._resize_after_id = self.after(100, self._perform_resize)


    def _perform_resize(self):
        # Use a copy to prevent altering the original image
        resized_image = self.base_image.copy()

        # Get the current canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Resize the image (downsize only) to fit within the canvas, preserving aspect ratio
        resized_image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)

        # Create a PhotoImage object and set as canvas background
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")


if __name__ == '__main__':
    app = App()
    app.mainloop()

