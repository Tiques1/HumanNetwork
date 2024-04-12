import tkinter as tk

root = tk.Tk()
root.title("Неравномерная сетка")

# Задаем различные веса для строк и столбцов
root.grid_columnconfigure(0, weight=1)  # 1й столбец
root.grid_columnconfigure(1, weight=2)  # 2й столбец
root.grid_columnconfigure(2, weight=1)  # 3й столбец

root.grid_rowconfigure(0, weight=1)  # 1я строка
root.grid_rowconfigure(1, weight=3)  # 2я строка
root.grid_rowconfigure(2, weight=2)  # 3я строка

# Создаем и размещаем виджеты
label1 = tk.Label(root, text="Я в 1й строке и 1м столбце", bg="lightblue")
label1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

label2 = tk.Label(root, text="Я в 1й строке и 2м столбце", bg="lightgreen")
label2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

label3 = tk.Label(root, text="Я в 1й строке и 3м столбце", bg="lightpink")
label3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

label4 = tk.Label(root, text="Я в 2й строке и 1м столбце", bg="lightyellow")
label4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

label5 = tk.Label(root, text="Я в 2й строке и 2м столбце", bg="lightcoral")
label5.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

label6 = tk.Label(root, text="Я в 3й строке и 1м столбце", bg="lightsalmon")
label6.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

label7 = tk.Label(root, text="Я в 3й строке и 2м столбце", bg="lightgrey")
label7.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

# Размещаем виджет в одной ячейке, которая занимает несколько строк и столбцов
big_label = tk.Label(root, text="Я занимаю 2 строки и 2 столбца", bg="lightblue")
big_label.grid(row=1, column=2, rowspan=2, columnspan=2, sticky="nsew", padx=5, pady=5)

root.mainloop()
