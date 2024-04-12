import tkinter as tk
from tkinter import Canvas, Scrollbar, Label


class MapViewer(tk.Tk):
    def __init__(self, image_path):
        super().__init__()
        self.title("Map Viewer")
        self.geometry("800x600")

        # Создаем скроллбары
        self.scrollbar_x = Scrollbar(self, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar_y = Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Создаем холст (Canvas)
        self.canvas = Canvas(self, bg="white", xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Подключаем скроллбары к холсту
        self.scrollbar_x.config(command=self.canvas.xview)
        self.scrollbar_y.config(command=self.canvas.yview)

        # Создаем Label для хранения холста с изображением
        self.image_label = Label(self.canvas, bg="white")
        self.image_label.pack()

        # Загружаем изображение карты в Label
        self.image = tk.PhotoImage(file=image_path)
        self.image_label.config(image=self.image)

        # Устанавливаем область прокрутки холста
        self.canvas.create_window(0, 0, anchor=tk.NW, window=self.image_label)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))


if __name__ == "__main__":
    # Путь к изображению карты
    image_path = "../UI.png"

    app = MapViewer(image_path)
    app.mainloop()
