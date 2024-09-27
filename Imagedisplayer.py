import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import json
from tkinter import messagebox

# Create a Tkinter window
root = tk.Tk()
root.title("Fox Gallery")
root.iconbitmap("foxicon.ico")
root.geometry("400x460")

# Function to load and display the image from url
def display_image_from_url(url):
    global count
    # fetch the image from the url
    response = requests.get(url)
    img_data = response.content


    # Open the image using pillow
    img = Image.open(BytesIO(img_data))

    # Resize the image to fit the window if necessary
    img = img.resize((400,400))

    # Convert the image to a PhotoImage object for Tkinter
    img_tk = ImageTk.PhotoImage(img)

    # Create a Label widget to display the image
    label = tk.Label(root, image=img_tk)
    label.image = img_tk
    label.grid(column=0, row=0, columnspan=2)

# Sets the count value to the length of the history list
with open("history.txt") as newfile:
    data = newfile.readlines()
    history = [x.strip("\n") for x in data]
    count = len(history)


def next():
    global count

    with open("history.txt") as file:
        data = file.readlines()
        history = [x.strip("\n") for x in data]
        if history.index(f"{history[count]}") == (len(history) - 1):
            img_url = requests.get("https://randomfox.ca/floof").json()["image"]
            with open("history.txt", mode="a") as file:
                file.write(f"{img_url}\n")
            display_image_from_url(img_url)
            count += 1
        else:
            count += 1
            display_image_from_url(f"{history[count]}")

def previous():
    global count

    with open("history.txt") as file:
        data = file.readlines()
        history = [x.strip("\n") for x in data]
        if history.index(history[count]) != 0:
            count -= 1
            display_image_from_url(f"{history[count]}")
        else:
            messagebox.showwarning("No More Pictures", "This is the last image")
            display_image_from_url(f"{history[count]}")



prev_button = tk.Button(root, text="Previous", font=("Georgia", 10), command=previous)
prev_button.grid(column=0, row=1, pady=20, padx=10)


img_url = requests.get("https://randomfox.ca/floof").json()["image"]

with open("history.txt", mode="a") as file:
    file.write(f"{img_url}\n")

# Url of the image to be displayed
image_url = img_url

next_button = tk.Button(root, text="Next", font=("Georgia", 10), command=next)
next_button.grid(column=1, row=1, pady=20, padx=10)

#Display the image in the Tkinter window
display_image_from_url(image_url)

#Start the Tkinter event loop
root.mainloop()
