import tkinter as tk
from PIL import Image, ImageTk


class MapViewer:
    def __init__(self, root, image_path):
        self.root = root
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.image = Image.open(image_path)
        self.image_width, self.image_height = self.image.size
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<ButtonPress-1>", self.on_start_scroll)
        self.canvas.bind("<B1-Motion>", self.on_scroll)
        self.canvas.bind("<MouseWheel>", self.on_zoom)

        self.start_x = None
        self.start_y = None
        self.start_scroll_x = None
        self.start_scroll_y = None

        self.scale = 1.0

    def on_canvas_resize(self, event):
        new_width = event.width
        new_height = event.height
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))

    def on_start_scroll(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.start_scroll_x = self.canvas.xview()[0]
        self.start_scroll_y = self.canvas.yview()[0]

    def on_scroll(self, event):
        if self.start_x is not None and self.start_y is not None:
            dx = self.start_x - event.x
            dy = self.start_y - event.y
            self.canvas.xview_moveto(self.start_scroll_x + dx / self.image_width)
            self.canvas.yview_moveto(self.start_scroll_y + dy / self.image_height)

    def on_zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= scale_factor
        new_width = int(self.image_width * self.scale)
        new_height = int(self.image_height * self.scale)
        resized_image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))
        self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)
        self.canvas.scale("all", 0, 0, scale_factor, scale_factor)

# Создаем основное окно
root = tk.Tk()
root.title("Map Viewer")

# Путь к изображению карты
image_path = "../UI.png"

# Создаем объект MapViewer
map_viewer = MapViewer(root, image_path)

# Запускаем основной цикл обработки событий
root.mainloop()
