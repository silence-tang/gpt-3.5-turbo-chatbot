import tkinter
from tkinter import *

from tqdm import tqdm
import openai
import logging as log
import wave, pyaudio
import pyttsx3
import sys


log.basicConfig(filename='openai-history.log', encoding='utf-8', level=log.DEBUG)
openai.api_key = "sk-******" # paste your openai api_key here
messages=[]
# 设定采样率、16位深度、声道、数据包大小、录制长度
RATE = 16000
FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024
RECODE_SECONDS = 5  # 实际录制长度(秒) = 设置长度-1


def get_audio():
    p = pyaudio.PyAudio()
    #打开流
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames = []

    #音频写入列表
    for _ in range(int(RATE / CHUNK * RECODE_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
	#读取列表写入文件
    wf=wave.open("user_audio.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    #防止出现空数据
    wf.writeframes(b"".join(frames))
    wf.close()
    return


def chatbot_response(msg):
    item =  {"role": "user", "content": msg}
    messages.append(item)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return str(response['choices'][0]['message']['content'])


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)
    if msg != '':
        ChatWindow.config(state=NORMAL)
        ChatWindow.insert(END, "You: " + '\n\n' + msg + '\n\n')
        ChatWindow.config(foreground="white", font=("Verdana", 12))
        res = chatbot_response(msg)
        ChatWindow.insert(END, "Bot: " + res + '\n\n')
        ChatWindow.config(state=DISABLED)
        ChatWindow.yview(END)


def exit():
    sys.exit(0)
    #销毁root窗口
    base.destroy()


def send_audio():
    get_audio()
    msg = openai.Audio.transcribe("whisper-1", open("user_audio.wav", "rb"))["text"]
    EntryBox.delete("0.0", END)
    if msg != '':
        ChatWindow.config(state=NORMAL)
        ChatWindow.insert(END, "You: " + '\n' + msg + '\n\n')
        ChatWindow.config(foreground="white", font=("Verdana", 12))
        res = chatbot_response(msg)
        ChatWindow.insert(END, "Bot: " + '\n' + res + '\n\n')
        ChatWindow.config(state=DISABLED)
        ChatWindow.yview(END)



if __name__ == "__main__":
    
    # engine = pyttsx3.init()                       #初始化语音引擎
    # engine.setProperty('rate', 100)               #设置语速
    # engine.setProperty('volume', 0.6)             #设置音量
    # voices = engine.getProperty('voices') 
    # engine.setProperty('voice',voices[0].id)      #设置第一个语音合成器

    base = Tk()
    base.title("ChatBot V1.0")
    base.geometry("600x500")
    base.resizable(width=FALSE, height=FALSE)
    
    # Create Chat window
    ChatWindow = Text(base, bd=0, fg='white', bg="black", font="Arial")
    ChatWindow.config(state=DISABLED)
    
    # Bind scrollbar to Chat window
    scrollbar = Scrollbar(base, command=ChatWindow.yview)
    ChatWindow['yscrollcommand'] = scrollbar.set
    
    # Create Button to send message
    SendButton = Button(base, width=10, font=("Verdana", 12, 'bold'), text="发送", bg="#54BBF7", activebackground="#1495DF", fg='#ffffff', command=send)
    AudioButton = Button(base, width=10, font=("Verdana", 12, 'bold'), text="录音", bg="#54BBF7", activebackground="#1495DF", fg='#ffffff', command=send_audio)
    
    # Create the box to enter message
    EntryBox = Text(base, bd=0, bg="white", width=52, height=8, font="Arial")
    
    # Place all components on the screen
    scrollbar.place(x=595, y=6, height=350)
    ChatWindow.place(x=5, y=6, height=350, width=600)
    EntryBox.place(x=5, y=360)
    SendButton.place(x=478, y=360, height=70)
    AudioButton.place(x=478, y=360+70, height=70)
    
    # Exit
    base.protocol("WM_DELETE_WINDOW", exit)
    base.mainloop()

