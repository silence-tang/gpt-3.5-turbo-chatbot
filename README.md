# GPT-ChatBot


This is a simple chatbot based on gpt-3.5-turbo, whisper-1 and tkinter.

## Results
![FT01C.png](https://i.328888.xyz/2023/03/03/FT01C.png)


## Requirements
1. tkinter
2. tqdm
3. openai
4. wave
5. pyaudio


You can install them simply by running `pip install xxx`.

## Run

- You can run the app locally by running `python chatbot.py`.

- It is worth noting that you should paste your own openai api_key to `openai.api_key = "sk-***"`.

- If you want to send a message by typing, feel free to type any questions in the text area then press the "Send" button.

- If you want to send a message by talking, feel free to press the "Audio" button and ask your question.

- You can set the time(second) for recording your audio by `RECODE_SECONDS`, which is set to 5 by default.

Enjoy your chat with gpt, have a good time!


### Note

Maybe you will encounter problems like "openai.error.APIConnectionError: Error communicating with OpenAI".

This is mainly caused by your local firewalls or Internet settings. If you have VPN on your machine, try to close/start it to avoid the problem.
