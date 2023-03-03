# GPT-ChatBot


This is a simple chatbot based on gpt-3.5-turbo and tkinter.

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

You can run the app locally by running `python chatbot.py`.

It is worth noting that you should paste your own openai api_key to `openai.api_key = "sk-***"`.

Enjoy your chat with gpt, have a good time!


### Note

Maybe you will encounter problems like "openai.error.APIConnectionError: Error communicating with OpenAI".

This is mainly caused by your local firewalls or Internet settings. If you have VPN on your machine, try to close/start it to avoid the problem.
