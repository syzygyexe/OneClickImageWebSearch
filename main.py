from tkinter import Tk, Button, Frame, Label, BOTTOM, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import requests
import webbrowser
import json
from fileinput import filename


def showimage():
    global filename
    filename = filedialog.askopenfilename(title="Select Image File", filetypes=(
        ("JPG file", "*.jpg"), ("PNG file", "*.png"), ("Other files", "*.*")))
    img = Image.open(filename)
    img.thumbnail((580, 450))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img


def browseimagegoogle():
    # Google
    filepath = filename
    searchurl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (filepath, open(
        filepath, 'rb')), 'image_content': ''}
    response = requests.post(searchurl, files=multipart, allow_redirects=False)
    fetchurl = response.headers['Location']
    webbrowser.open(fetchurl)


def browseimageyandex():
    # Yandex
    filepath = filename
    searchurl = 'https://yandex.ru/images/search'
    files = {'upfile': ('blob', open(filepath, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    print(params)
    response = requests.post(searchurl, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = searchurl + '?' + query_string
    webbrowser.open(img_search_url)


def browseboth():
    browseimagegoogle()
    browseimageyandex()


root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, pady=15)

lbl = Label(root)
lbl.pack()

btn = Button(frm, text="Open Image", command=showimage)
btn.pack(side=tk.LEFT, padx=3)

btn2 = Button(frm, text="Browse Image in Google", command=browseimagegoogle)
btn2.pack(side=tk.LEFT, padx=3)

btn3 = Button(frm, text="Browse Image in Yandex", command=browseimageyandex)
btn3.pack(side=tk.LEFT, padx=3)

btn4 = Button(frm, text="Browse Both", command=browseboth)
btn4.pack(side=tk.LEFT, padx=3)

btn5 = Button(frm, text="Exit", command=lambda: exit())
btn5.pack(side=tk.LEFT, padx=3)

root.title("Birdy")
root.wm_iconbitmap('./birdy.ico')
root.geometry("640x480")

root.mainloop()
