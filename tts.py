import tkinter as tk
from gtts import gTTS # type: ignore
import os
import tkinter.messagebox
window = tk.Tk()
window.geometry("500x200")
mytext="Hello! What would you like to say to the stretch robot?"
greeting = tk.Label("enter message")
language='en'
myobj=gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")
os.system("start welcom.mp3")

def go_clicked():
    msg="thank you for your input"
    tkinter.messagebox.showinfo(msg)
    language='en'
    myobj=gTTS(text=msg, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("start welcom.mp3")

greeting.pack()
usertext = tk.StringVar()
textbox = tk.Entry(window, textvariable=usertext)
textbox.pack()
mytext=textbox.get()
go_button = tk.Button(window, text="GO!", command=go_clicked)
go_button.pack(fill='x', expand=True, pady=10)
window.mainloop()
