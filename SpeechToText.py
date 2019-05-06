import argparse
import base64
import json
import threading
import time
import pyaudio
import websocket
from websocket._abnf import ABNF

#Set up audio stream 16 bit, 44.1k sample rate, chunk size to send watson,and mono ch
FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 1024*4
CHANNELS = 1

#Place holder variable to hold Queue
f = ""
w = ""

def read_audio(ws):
    #Get global sample rate, set to audio device rate, and then send the stream from audio device to the websocket port
    global RATE, w
    p = pyaudio.PyAudio()
    RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            try:
                ws.send(data, ABNF.OPCODE_BINARY) #Indicates binary is sent through stream
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

        if not w.value:
            break

    # Disconnect the audio stream
    stream.stop_stream()
    stream.close()
    print("* done recording")

    #Stop to get final response
    data = {"action": "stop"}
    ws.send(json.dumps(data).encode('utf8'))

    #Wait then shut down websocket and stream
    time.sleep(1)
    ws.close()
    p.terminate()

# Print and save the text from Watson
def on_message(self, msg):
    data = json.loads(msg)
    if "results" in data:
        c = data['results'][0]['alternatives'][0]['transcript']

        #Check if Queue is full
        if not f.full():
            f.put(c)
        else:
            f.get()
            f.put(c)

#Begins as soon as an active connection exsists
def on_open(ws):
    data = {
        "action": "start",
        "content-type": "audio/l16;rate=%d" % RATE,
        "continuous": True,
        "interim_results": True,
        "word_confidence": True,
        "timestamps": True,
        "max_alternatives": 3
    }

    #Initial control message
    ws.send(json.dumps(data).encode('utf8'))

    #New thread to process audio
    threading.Thread(target=read_audio, args=(ws,)).start()

def speechToText(q,watson):
    global f, w
    f = q
    w = watson

    # Connect to websocket interfaces
    headers = {}
    userpass = "" #Enter API Kkey HERE!
    headers["Authorization"] = "Basic " + base64.b64encode(userpass.encode()).decode()
    url = "wss://stream.watsonplatform.net/speech-to-text/api/v1/recognize?model=en-US_BroadbandModel"

    #Initial connection to watson if its true
    if w.value:
        print("Initializing WebSocket...")
        ws = websocket.WebSocketApp(url, header=headers,on_message=on_message)
        ws.on_open = on_open

        print("Starting Websocket...")
        #Websocket takes control until it is closed
        ws.run_forever()

    #Check wether to connect to watson on loop
    while True:
        if w.value == True:
            print("Initializing WebSocket...")
            ws = websocket.WebSocketApp(url, header=headers,on_message=on_message)
            ws.on_open = on_open

            print("Starting Websocket...")
            #Websocket takes control until it is closed
            ws.run_forever()
