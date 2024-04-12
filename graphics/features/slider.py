import tkinter as tk

def on_scale_change(value):
    label_value.config(text=f"Выбранное значение: {value}")

root = tk.Tk()
root.title("Слайдер (Scale)")

# Создаем слайдер
scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=on_scale_change)
scale.pack(pady=20)

# Метка для отображения выбранного значения
label_value = tk.Label(root, text="Выбранное значение: 0")
label_value.pack()

root.mainloop()
