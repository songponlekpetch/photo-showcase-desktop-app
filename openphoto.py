import os
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

class PhotoRenderer:
    
    INITIAL_ORDER = 4
    
    def __init__(self, master, folder):
        self.last_image = 1
        self.master = master
        self.folder = folder
        self.files = os.listdir(folder)
        self.files.sort(reverse=True)
        
        self.images = [
            ImageTk.PhotoImage(
                ImageOps.contain(Image.open(f"{folder}/{image}"), (int(master.winfo_screenwidth() / 4), 500))) 
            for image in self.files if image.endswith(".jpg")]
        
    def render_images(self):
        for index in range(len(self.images)):
            image_label = tk.Label(self.master, image=self.images[index])
            image_label.grid(row=(index + self.INITIAL_ORDER) //4, column=(index + self.INITIAL_ORDER) % 4)
            self.last_image = index + 1
            print(f"Rendering {self.last_image}.jpg row={(index + self.INITIAL_ORDER) //4} column={(index + self.INITIAL_ORDER) % 4}")
            
    def next_image(self):
        try:
            self.images.insert(0, ImageTk.PhotoImage(ImageOps.contain(Image.open(f"{self.folder}/{self.last_image + 1}.jpg"), (int(root.winfo_screenwidth() / 4), 500))))
            self.last_image += 1
        except:
            print(f"No {self.last_image + 1}.jpg images in {self.folder}")
            
        self.render_images()


root = tk.Tk()
app = FullScreenApp(root)
photo_renderer = PhotoRenderer(master=root, folder="photos")
photo_renderer.render_images()

button = tk.Button(root, text="Next", command=photo_renderer.next_image)
button.grid(row=0, column=0)

root.mainloop()
