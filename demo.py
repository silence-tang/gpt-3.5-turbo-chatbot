from tkinter import *
from aip import AipSpeech
from playsound import playsound
from tqdm import tqdm
import openai
import logging as log
import wave, pyaudio
import pyttsx3
import sys


log.basicConfig(filename='openai-history.log', encoding='utf-8', level=log.DEBUG)
openai.api_key = "sk-"
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

messages=[]

# 设定采样率、16位深度、声道、数据包大小、录制长度
RATE = 16000
FORMAT = pyaudio.paInt16
CHANNELS = 2
CHUNK = 1024
RECODE_SECONDS = 8  # 实际录制长度(秒) = 设置长度-1

# 初始化语音引擎
engine = pyttsx3.init()                       
engine.setProperty('rate', 180)               # 设置语速
voices = engine.getProperty('voices') 
engine.setProperty('voice',voices[0].id)      # 设置第一个语音合成器


def get_audio():
    p = pyaudio.PyAudio()
    #打开流
    stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
    frames = []

    #音频写入列表
    for _ in tqdm(range(int(RATE / CHUNK * RECODE_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
	#读取列表写入文件
    wf = wave.open("user_audio.wav", "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    #防止出现空数据
    wf.writeframes(b"".join(frames))
    wf.close()


def chatbot_response(msg):
    item =  {"role": "user", "content": msg}
    messages.append(item)
    # ChatGPT is powered by gpt-3.5-turbo, OpenAI’s most advanced language model.
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return str(response['choices'][0]['message']['content'])


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)
    if msg != '':
        ChatWindow.config(state=NORMAL)
        ChatWindow.insert(END, "You: " + '\n\n' + msg + '\n\n')   # show msg in the chat window
        ChatWindow.config(foreground="black", font=("Verdana", 12))
        ans = chatbot_response(msg)
        ChatWindow.insert(END, "Bot: " + ans + '\n\n')
        ChatWindow.config(state=DISABLED)
        ChatWindow.yview(END)
    if talk_var.get():
        if any(map(lambda c:'\u4e00' <= c <= '\u9fa5', ans)):
            lang = 'zh'
        else:
            lang = 'en'
        result  = client.synthesis(ans, lang, 1, {
            'vol': 5,   # 音量，取值0-15，默认为5中音量
            'per': 4,   # 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
            'spd': 6,	# 语速，取值0-9，默认为5中语速
            # pit	String	音调，取值0-9，默认为5中语调
        })
        if not isinstance(result, dict):
            with open('res_audio.mp3','wb') as f:
                f.write(result)
            f.close()
        playsound('res_audio.mp3')


def send_audio():
    get_audio()
    msg = openai.Audio.transcribe("whisper-1", open("user_audio.wav", "rb"))["text"]
    EntryBox.delete("0.0", END)
    if msg != '':
        ChatWindow.config(state=NORMAL)
        ChatWindow.insert(END, "You: " + '\n\n' + msg + '\n\n')
        ChatWindow.config(foreground="black", font=("Verdana", 12))
        ans = chatbot_response(msg)
        ChatWindow.insert(END, "Bot: " + ans + '\n\n')
        ChatWindow.config(state=DISABLED)
        ChatWindow.yview(END)
    if talk_var.get():
        if any(map(lambda c:'\u4e00' <= c <= '\u9fa5', ans)):
            lang = 'zh'
        else:
            lang = 'en'
        result  = client.synthesis(ans, lang, 1, {
            'vol': 5,   # 音量，取值0-15，默认为5中音量
            'per': 4,   # 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
            'spd': 6,	# 语速，取值0-9，默认为5中语速
            # pit	String	音调，取值0-9，默认为5中语调
        })
        if not isinstance(result, dict):
            with open('res_audio.mp3','wb') as f:
                f.write(result)
            f.close()
        playsound('res_audio.mp3')


def delete():
    ChatWindow.config(state=NORMAL)
    ChatWindow.yview("0.0")
    ChatWindow.delete("0.0", END)

def exit():
    sys.exit(0)
    #销毁root窗口
    base.destroy()


if __name__ == "__main__":
    
    base = Tk()
    base.title("ChatBot V1.0")
    base.geometry("600x500")
    base.resizable(width=FALSE, height=FALSE)
    
    # Create Chat window
    ChatWindow = Text(base, bd=0, fg='black', bg="white", font="Arial")
    ChatWindow.config(state=DISABLED)

    # Bind scrollbar to Chat window
    scrollbar = Scrollbar(base, command=ChatWindow.yview)
    ChatWindow['yscrollcommand'] = scrollbar.set

    # Create Button to send message
    SendButton = Button(base, width=10, font=("Verdana", 12, 'bold'), text="Send", bg="#54BBF7", activebackground="#1495DF", fg='#ffffff', command=send)
    AudioButton = Button(base, width=10, font=("Verdana", 12, 'bold'), text="Record", bg="#54BBF7", activebackground="#1495DF", fg='#ffffff', command=send_audio)
    talk_var = IntVar()
    talk_var.set(0)
    IsTalkButton = Checkbutton(base, width=13, text="is_talk", variable=talk_var, onvalue=1, offvalue=0)

    # Create the box to enter message
    EntryBox = Text(base, bd=0, bg="white", font="Arial")

    # Create the clear button to clear all the msg in the chat window
    ClearButton = Button(base, width=10, font=("Verdana", 12, 'bold'), text="Clear", bg="#54BBF7", activebackground="#1495DF", fg='#ffffff', command=delete)
    
    # Place all components on the screen
    scrollbar.place(x=586, y=6, height=350, width=15)
    ChatWindow.place(x=5, y=6, height=350, width=585)
    EntryBox.place(x=5, y=360, height=200, width=470)
    SendButton.place(x=478, y=360, height=35)
    AudioButton.place(x=478, y=360+35, height=35)
    IsTalkButton.place(x=478, y=360+70, height=35)
    ClearButton.place(x=478, y=360+105, height=35)

    # Exit
    base.protocol("WM_DELETE_WINDOW", exit)
    base.mainloop()

