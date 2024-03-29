import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

current_image = None

def open_image():
    global photo
    global file
    global image
    global current_image
    file = filedialog.askopenfilename()
    if file :
        image = Image.open(file)
        image.thumbnail((600, 400)) 
        photo = ImageTk.PhotoImage(image) 
        current_image = image
        canvas.create_image(300, 200, image=photo, anchor='center')  

def adjust_brightness(image, num, dialog):
    global photo
    global current_image
    num = int(num)
    if num > 0:
        add = True
    else:
        add = False
        num = -num
    a = max(0, min(255, num))
    pixels = image.load()
    if add:
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                r = min(r + a, 255)
                g = min(g + a, 255)
                b = min(b + a, 255)
                image.putpixel((i, j), (r, g, b))
    else:
        for i in range(image.width):
            for j in range(image.height):
                r, g, b = pixels[i, j]
                r = max(0, r - a)
                g = max(0, g - a)
                b = max(0, b - a)
                image.putpixel((i, j), (r, g, b))
    image.thumbnail((600, 400))     
    photo = ImageTk.PhotoImage(image)  
    current_image = image
    canvas.create_image(300, 200, image=photo, anchor='center')  
    dialog.destroy()  

def adjust_brightness_interface():
    global current_image
    if file: 
        dialog = tk.Toplevel(root)
        dialog.title("Enter the adjust number")
        dialog.geometry("300x100")

        label = tk.Label(dialog, text="adjust number: +/-(0 - 255)")
        label.pack()
        entry = tk.Entry(dialog)
        entry.pack()

        confirm_button = tk.Button(dialog, text="adjust Image", command= lambda: adjust_brightness(current_image, entry.get(), dialog))
        confirm_button.pack()

def crop_image(image, x1, y1, x2, y2, dialog):
    global photo
    global current_image
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    cropped_image = image.crop((max(0, x1), max(0, y1), min(600, x2), min(400, y2)))
    cropped_image.thumbnail((600, 400)) 
    photo = ImageTk.PhotoImage(cropped_image)  
    current_image = cropped_image
    canvas.create_image(300, 200, image=photo, anchor='center')  
    dialog.destroy()  


def crop_image_interface():
    if file: 
        dialog = tk.Toplevel(root)
        dialog.title("Enter Coordinates")
        dialog.geometry("300x200")

        x1_label = tk.Label(dialog, text="Upper Left X Coordinate:")
        x1_label.pack()
        x1_entry = tk.Entry(dialog)
        x1_entry.pack()

        y1_label = tk.Label(dialog, text="Upper Left Y Coordinate:")
        y1_label.pack()
        y1_entry = tk.Entry(dialog)
        y1_entry.pack()

        x2_label = tk.Label(dialog, text="Lower Right X Coordinate:")
        x2_label.pack()
        x2_entry = tk.Entry(dialog)
        x2_entry.pack()

        y2_label = tk.Label(dialog, text="Lower Right Y Coordinate:")
        y2_label.pack()
        y2_entry = tk.Entry(dialog)
        y2_entry.pack()

        confirm_button = tk.Button(dialog, text="Crop Image", command= lambda: crop_image(current_image, x1_entry.get(), y1_entry.get(), x2_entry.get(), y2_entry.get(), dialog))
        confirm_button.pack()

def ave(img, x, y, f):
    rt = gt= bt = 0
    for x2 in range(x-f, x+1+f):
        for y2 in range(y-f, y+1+f):
            r, g, b = img.getpixel((x2,y2))
            rt += r
            gt += g
            bt += b
    bt = bt// ((f*2+1)**2)
    rt = rt// ((f*2+1)**2)
    gt = gt// ((f*2+1)**2)
    return (rt, gt, bt)

def blur_image(img, f, dialog):
    global photo
    global current_image
    f = int(f)
    if f < 0:
        f = 0
    if f > 5:
        f = 5
    w = img.size[0]
    h = img.size[1]
    for x in range(f, w-f):
        for y in range(f, h-f):
            r,g,b = ave(img, x, y, f)
            img.putpixel((x,y), (r,g,b))
    img.thumbnail((600, 400)) 
    photo = ImageTk.PhotoImage(img)  
    current_image = img
    canvas.create_image(300, 200, image=photo, anchor='center')  
    dialog.destroy()  

def blur_image_interface():
    if file: 
        dialog = tk.Toplevel(root)
        dialog.title("Enter blur factor")
        dialog.geometry("300x100")

        label = tk.Label(dialog, text="blur factor(better not >= 5)")
        label.pack()
        entry = tk.Entry(dialog)
        entry.pack()

        confirm_button = tk.Button(dialog, text="Blur Image", command= lambda: blur_image(current_image, entry.get(), dialog))
        confirm_button.pack()

def save_image():
     current_image.save("Saved image.jpg")

root = tk.Tk()
root.title("Simple Python Photo Editor")

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()

brightness_button = tk.Button(root, text="Adjust Brightness", command=adjust_brightness_interface)
brightness_button.pack(side=tk.LEFT,padx=(50, 0), pady=(0, 20))

crop_button = tk.Button(root, text="Crop Image", command=crop_image_interface)  
crop_button.pack(side=tk.LEFT,padx=(50, 0), pady=(0, 20))

blur_button = tk.Button(root, text="Blur Image", command=blur_image_interface)
blur_button.pack(side=tk.LEFT,padx=(50, 0), pady=(0, 20))

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(side=tk.LEFT,padx=(50, 0), pady=(0, 20))

#start
root.mainloop()