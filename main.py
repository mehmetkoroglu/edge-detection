from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd

from PIL import ImageTk, Image

tk = Tk()
tk.geometry("850x625")
tk.resizable(False, False)
tk.title("Edge Detection with Image Processing - Mehmet Nazım KÖROĞLU")

file_path = ""
file = Image
file_X = Image
file_Y = Image
file_G = Image
file_grey_scale = Image


def select_file():
    global file_path, file, file_Y, file_X, file_G, file_grey_scale

    try:
        filetypes = (('Image Files', '*.png *.jpg *.jpeg'), ('All files', '*.*'))
        file_path = fd.askopenfilename(initialdir='./Desktop', filetypes=filetypes)
        file_grey_scale = Image.open(file_path).convert('L').resize((250, 250))

        file = Image.open(file_path).resize((250, 250))
        file_X = Image.open(r'x.png').resize((250, 250))
        file_Y = Image.open(r'y.png').resize((250, 250))
        file_G = Image.open(r'xy.png').resize((250, 250))

        image = ImageTk.PhotoImage(file)
        img = Label(image=image)
        img.image = image
        img.place(x=50, y=50)
    except:
        pass


def process():
    global file_path, file, file_Y, file_X, file_G, file_grey_scale

    try:
        edge_detection(select_box.get())

        image2 = ImageTk.PhotoImage(file_X)
        img2 = Label(image=image2)
        img2.image = image2
        img2.place(x=350, y=50)

        image3 = ImageTk.PhotoImage(file_Y)
        img3 = Label(image=image3)
        img3.image = image3
        img3.place(x=50, y=350)

        image4 = ImageTk.PhotoImage(file_G)
        img4 = Label(image=image4)
        img4.image = image4
        img4.place(x=350, y=350)
    except:
        messagebox.showerror(title='Error', message='Image Not Selected! or Invalid Threshold Value')


def edge_detection(mask_type):
    global file_path, file, file_Y, file_X, file_G, file_grey_scale
    mask_y = mask_x = [[], [], []]
    if mask_type == 'Sobel':
        mask_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        mask_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    elif mask_type == 'Prewitt':
        mask_y = [[-1, -1, -1], [0, 0, 0], [1, 1, 1]]
        mask_x = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    else:
        messagebox.showerror(title='Error', message='Method Error!')

    for i in range(1, file.width - 1):
        for j in range(1, file.height - 1):
            a = 0
            a += file_grey_scale.getpixel((i - 1, j - 1)) * mask_y[0][0]
            a += file_grey_scale.getpixel((i - 1, j)) * mask_y[0][1]
            a += file_grey_scale.getpixel((i - 1, j + 1)) * mask_y[0][2]

            a += file_grey_scale.getpixel((i, j - 1)) * mask_y[1][0]
            a += file_grey_scale.getpixel((i, j)) * mask_y[1][1]
            a += file_grey_scale.getpixel((i, j + 1)) * mask_y[1][2]

            a += file_grey_scale.getpixel((i + 1, j - 1)) * mask_y[2][0]
            a += file_grey_scale.getpixel((i + 1, j)) * mask_y[2][1]
            a += file_grey_scale.getpixel((i + 1, j + 1)) * mask_y[2][2]

            if round(a) < int(threshold.get()):
                file_X.putpixel((i, j), (0, 0, 0, 255))
            if round(a) >= int(threshold.get()):
                file_X.putpixel((i, j), (255, 255, 255, 255))

    for i in range(1, file.width - 1):
        for j in range(1, file.height - 1):
            a = 0
            a += file_grey_scale.getpixel((i - 1, j - 1)) * mask_x[0][0]
            a += file_grey_scale.getpixel((i - 1, j)) * mask_x[0][1]
            a += file_grey_scale.getpixel((i - 1, j + 1)) * mask_x[0][2]

            a += file_grey_scale.getpixel((i, j - 1)) * mask_x[1][0]
            a += file_grey_scale.getpixel((i, j)) * mask_x[1][1]
            a += file_grey_scale.getpixel((i, j + 1)) * mask_x[1][2]

            a += file_grey_scale.getpixel((i + 1, j - 1)) * mask_x[2][0]
            a += file_grey_scale.getpixel((i + 1, j)) * mask_x[2][1]
            a += file_grey_scale.getpixel((i + 1, j + 1)) * mask_x[2][2]

            if round(a) < int(threshold.get()):
                file_Y.putpixel((i, j), (0, 0, 0, 255))
            if round(a) >= int(threshold.get()):
                file_Y.putpixel((i, j), (255, 255, 255, 255))

    for i in range(file.width):
        for j in range(file.height):
            if file_X.getpixel((i, j))[0] > 0 or file_Y.getpixel((i, j))[0] > 0:
                file_G.putpixel((i, j), (255, 255, 255, 255))
            else:
                file_G.putpixel((i, j), (0, 0, 0, 128))


open_file = ttk.Button(text='Load Image', width=15, command=select_file)
open_file.place(x=625, y=175)

process = ttk.Button(text='Start Process', width=15, command=process)
process.place(x=730, y=175)

label_mask = ttk.Label(text='Select Mask Type')
label_mask.place(x=625, y=50)

select_box = ttk.Combobox(master=tk, width=30)
select_box['values'] = ('Sobel', 'Prewitt')
select_box.current(0)
select_box.place(x=625, y=75)

label_threshold = ttk.Label(text='Threshold')
label_threshold.place(x=625, y=125)

threshold = ttk.Entry(width=15, validate='key')
threshold.insert(0, str(30))
threshold.place(x=730, y=125)

label_original = ttk.Label(text='Original')
label_original.place(x=150, y=30)

label_x = ttk.Label(text='Gradiant X')
label_x.place(x=450, y=30)

label_y = ttk.Label(text='Gradiant Y')
label_y.place(x=150, y=325)

label_sum = ttk.Label(text='Gradiant Sum')
label_sum.place(x=450, y=325)

tk.mainloop()
