import tkinter as tk
import emotion
import response_generator
from robot_movements import happy, sad, angry, surprise

window = tk.Tk()
window.title("Stretch Robot ChatBox")
window.geometry("500x400")
mytext = "Hello! What would you like to say to the stretch robot?"
greeting = tk.Label(window, text="enter message here:", font=("Helvetica", 20))
language = 'en'

greeting.pack()
usertext = tk.StringVar()
textbox = tk.Text(window, height=5, width=50)
textbox.pack()

def get_user_input():
    user_text = textbox.get("1.0", "end-1c")
    return f"User input: {user_text}"

def go_clicked():
    user_input = get_user_input()
    response_msg = response_generator.get_response(user_input)
    display_response(response_msg)
    response_emotion = emotion.classify_emotion(response_msg)
    if (response_emotion == "Joy"):
        happy()
    elif (response_emotion == "Sad"):
        sad()
    elif (response_emotion == "Anger"):
        angry()
    else:
        surprise()

def display_response(response_msg:str):
    reply = tk.Label(window, text=response_msg, font=("Helvetica", 14), width=150)
    reply.place(x=5, y=10)
    reply.pack()

go_button = tk.Button(window, text="GO!", command=go_clicked, height=2, width=5)
go_button.place(x=100, y=150)
window.mainloop()