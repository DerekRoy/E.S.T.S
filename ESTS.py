import tensorflow as tf
from SpeechToText import *
from multiprocessing import Process, Queue, Value
import threading, time
import cv2
import numpy as np
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, SentimentOptions
from watson_developer_cloud import LanguageTranslatorV3
import imutils
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import re
from PIL import ImageFont, ImageDraw, Image
import arabic_reshaper
from bidi.algorithm import get_display
import os
import argparse
import sys

#Supress Tensorflow warnings
tf.logging.set_verbosity(tf.logging.ERROR)

class SpeechTranslationSentiment:
    def __init__(self, w, l):
        #API credentials and information [Edit this for your specific account]
        self.language_translator = LanguageTranslatorV3(
            version='2018-05-01',
            iam_apikey='',#Enter API Key HERE!
            url='https://gateway.watsonplatform.net/language-translator/api')

        self.natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey='',#Enter API Key HERE!
            url='https://gateway.watsonplatform.net/natural-language-understanding/api')

        self.w = w
        self.textIn = "Speech text here"
        self.speech = self.textImage(self.textIn, False)
        self.sTranslation = self.textImage(self.textIn, False)
        self.sentiment = ""
        self.getTone()
        self.target = l
        self.dict = {'ar':'arabic.ttf', 'hi':'hindi.ttf','ko':'korean.otf','ru':'NotoSans-Bold.ttf'}

    #Set the text value and image
    def setText(self,t):
        self.text = t
        self.speech = self.textImage(t,False)

    def getText(self):
        return self.text

    def setTranslation(self,t):
        self.sTranslation = self.textImage(t, False)

    #Get the speech to text image
    def getSpeech(self):
        return self.speech

    #Convert strings to an image
    def textImage(self,text,special):
        #Default characters that fit on screen
        imageChars = 31

        #Characters that fit on screen per language and font
        diffFonts = {'ar':33, 'hi': 35, 'ko': 22, 'ru': 27}
        otherLangs = {'ja':16, 'zh':15, 'zh-TW':15}

        #Create text
        canvas = np.full((150,535,3),255,dtype = "uint8")

        #Choose fonts based off language and the method call
        if special and (self.target in ['ar', 'hi', 'ko', 'ru']):
            fontpath = "fonts/" + self.dict[self.target]
            imageChars = diffFonts[self.target]

        elif special and (self.target in ['ja', 'zh', 'zh-TW']):
            imageChars = otherLangs[self.target]
            fontpath = "fonts/simsun.ttc"

        else:
            fontpath = "fonts/simsun.ttc"

        #Edit string based on length to see in frame
        if len(text) > imageChars:
            text =text[len(text)-imageChars:]

        if special and self.target == 'ar':
            reshaped_text = arabic_reshaper.reshape(text)
            text = get_display(reshaped_text)

        #Write font into image
        font = ImageFont.truetype(fontpath, 32)
        img_pil = Image.fromarray(canvas)
        draw = ImageDraw.Draw(img_pil)
        draw.text((17, 58),  text, font = font, fill = (0, 0, 0))
        canvas = np.array(img_pil)
        return canvas

    #Translate from english to specified target language
    def translate(self):
        try:
            translation = self.language_translator.translate(text=self.text, model_id='en-'+self.target).get_result()
            self.sTranslation = self.textImage(translation["translations"][0]["translation"], True)
            # print(translation["translations"][0]["translation"])
        except:
            self.sTranslation = self.textImage("Translation", False)

    #Define the tone of a string provided, and output a graph of it
    def getTone(self):
        #Handle Errors from inconsistent length or other api issues
        try:
            response = self.natural_language_understanding.analyze(text = self.text,features=Features(sentiment=SentimentOptions())).get_result()
            response = response["sentiment"]["document"]
            score = response["score"]
            label = response["label"]
        except:
            score = 0
            label = "no sentiment detected"

        #Create canvas to draw on
        canvas = np.full((300, 400, 3),255,dtype="uint8")

        #Values for watson image
        x = int(round(982/10))
        y = int(round(952/10))
        spacing = 10

        #Draw Watson image on Sentiment graph
        watsonImage = cv2.imread("watson.png")
        watsonImage = cv2.resize(watsonImage, (x, y))
        canvas [300-y-spacing:300-spacing,spacing:x+spacing,:] = watsonImage

        # Construct the percentage text
        t = "{:.2f}%".format(score * 100)

        if label == "no sentiment detected":
            t = ""

        # draw the probability bar on the canvas
        w = int(score * 195)

        #Color Options dictionary (B,G,R)
        colors = {"positive":(86,127,113),"negative":(7,24,90),"neutral":(93,90,90),"no sentiment detected":(0,0,0)}

        #Draw Rectangle
        cv2.rectangle(canvas, (205, (127) + 5),
                (200+w, (127) + 35), colors[label], -1)

        #Draw Title text
        cv2.putText(canvas, "Sentiment of Speech", (55, 50),
        cv2.FONT_HERSHEY_COMPLEX, 0.80,(5, 5, 5), 2)

        #Draw Sentiment text
        cv2.putText(canvas, label, (10, (100) + 23),
        cv2.FONT_HERSHEY_COMPLEX, 0.60,(colors[label]), 2)

        #Draw Percentage Text
        cv2.putText(canvas, t, (163, (100) + 23),
        cv2.FONT_HERSHEY_COMPLEX, 0.6,(colors[label]), 2)

        self.sentiment = canvas

    #Update the images containing sentiment and translation every half a second
    def update(self, u_stop):
        if not u_stop.is_set():
            if self.w.value:
                self.translate()
                self.getTone()
            threading.Timer(.5, self.update, [u_stop]).start()

    def getScreen(self):
        textout = np.concatenate((self.speech,self.sTranslation), axis=0)
        screen = np.concatenate((self.sentiment,textout), axis=1)
        return screen

#Acceptable language inputs for Wtson
LANGUAGES = ['arabic','czech', 'danish', 'dutch', 'finnish', 'french', 'german', 'hindi', 'hungarian', 'italian', 'japanese', 'korean', 'norwegian', 'polish', 'portuguese', 'russian', 'simplifiedchinese', 'spanish', 'swedish', 'traditionalchinese', 'turkish']
LANGS = ['ar', 'cs', 'da', 'nl', 'fi', 'fr', 'de', 'hi', 'hu', 'it', 'ja', 'ko', 'nb', 'pl', 'pt', 'ru', 'zh', 'es', 'sv', 'zh-TW', 'tr']

#Process string input with regular expression
def processLanguage(lang):
    regex = re.compile('[^a-zA-Z]')
    l = lang.lower()
    l = regex.sub('',lang).strip()
    if l in LANGUAGES:
        l = LANGS[LANGUAGES.index(l)]
    return l

#Check if the language input is acceptable for Watson
def validLanguage(lang):
    if lang in LANGUAGES or lang in LANGS:
        return True

    else:
        return False

#Get a new language input
def changeLanguage(lang):
    decision = input("Would you like to change the language to translate to?(y/n): ")

    if 'y' in decision.lower():
        decision = True
        lang = input("Enter the language or language code: ")
        needLang = True

        while needLang:
            if validLanguage(processLanguage(lang)):
                needLang = False
            else:
                lang = input("Bad Input, Enter the language or language code: ")

    return  lang

def toBool(x):
    if x in ['True', 'true', 'Yes','yes','1']:
        return True
    return False

#Collect arguements from command line for languages and wether user wants to connect to Watson
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--language", required=True,
    help="language used for translation")
ap.add_argument("-w", "--watson", required=True,
    help="wether to enable watson")
args = vars(ap.parse_args())

#Set up Watson and languages
lang = processLanguage(args['language'])
watson = Value('d', int(toBool(args['watson'])))
s = False
sts = SpeechTranslationSentiment(watson, lang)

#Function to set and start graph and mouse on click
def mouse_drawing(event, x, y, flags, params):
    global s, watson, sts
    if event == cv2.EVENT_LBUTTONDOWN:
        if 0 < x < 110 and 490 < y < 600:
            if watson.value:
                watson.value = False
            else:
                watson.value = True
                sts.setText("Connecting to Watson ...")
        elif 70<x<310 and 0<y<60:
            if s:
                s = False
            else:
                s = True

#Validate entered language and exit if it is not acceptable for Watson
if not validLanguage(lang):
    print("\nIncorrect language input, you can input:\n{}\nor\n{}\nNot {}\n".format(LANGUAGES,LANGS,lang))
    exit()

#Let user know what the entered choice is
print("You have chosen to translate to {}, and set using Watson to {}".format(args["language"], watson.value))

#Set up Display windows and functions, as well as an update thread
u_stop = threading.Event()

#Define running values and multiprocessing for speech to text if watson is true
q = Queue()
p = Process(target=speechToText, args=(q,watson,))
p.start()
sts.update(u_stop)

#Get the camera
camera = cv2.VideoCapture(0)

# load the face detector cascade, emotion detection CNN, then define
# the list of emotion labels
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

EMOTIONS = ["angry", "scared", "happy", "sad", "surprised","neutral"]

colors = {"happy":(82,240,247),"surprised":(90,153,219),"scared":(86,127,113),"angry":(7,24,90),"neutral":(93,90,90), "sad":(91,80,62)}

#API reference to trained model
pai_api = 'api/dlapis/26a7f490-077c-482b-9b87-b255b69fae72'
powerai_baseurl='https://p10a159.pbm.ihost.com/powerai-vision/'
endpoint = powerai_baseurl + pai_api

#Load Model
model = load_model("checkpoints/epoch_75.hdf5")

#Mouse Interaction capabilitis set
cv2.namedWindow("Emotion Detection by PyImageSearch trained on Watson Machine Accelerator with IBM Watson Speech Services")
cv2.setMouseCallback("Emotion Detection by PyImageSearch trained on Watson Machine Accelerator with IBM Watson Speech Services", mouse_drawing)

print("\nIn the video window press:\n'q' to quit the program,\n'i' to initiate Watson,\n'k' to kill the connection to Watson\n's' to suppress Emotion Graph\n")

while True:

    #Display that Watson is Disconnected
    if not watson.value:
        sts.setText("Watson Disconnected")
        sts.setTranslation("Watson Disconnected")

    # grab the current frame
    (grabbed, frame) = camera.read()

    # resize the frame and convert it to grayscale
    frame = imutils.resize(frame, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Get the text
    if not q.empty():
    	sts.setText(q.get())

    # initialize the canvas for the visualization, then clone
    # the frame so we can draw on it
    canvas = np.full((300, 400, 3), 255, dtype="uint8")

    #Suppress of show emotion graph based on truth value of s
    if s:
        cv2.putText(canvas, "Graph Suppressed", (69, 150),cv2.FONT_HERSHEY_COMPLEX, 0.80,(0, 0, 0), 2)
    else:
        #Draw Title text
        cv2.putText(canvas, "Emotions Detected", (69, 85),cv2.FONT_HERSHEY_COMPLEX, 0.80,(0, 0, 0), 2)
        cv2.putText(canvas, "EMOTION", (10, 125),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(5, 5, 5), 2)
        cv2.putText(canvas, "LIKELINESS", (271, 125),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(5, 5, 5), 2)

    #Values for watson image
    x = int(round(700/2.8))
    y = int(round(161/2.8))
    spacing = 70

    #Draw Watson image on Sentiment graph
    pyimagesearch = cv2.imread("pyimagesearch.png")
    pyimagesearch = cv2.resize(pyimagesearch, (x, y))
    canvas [0:y,spacing:x+spacing,:] = pyimagesearch


    #Frame we will draw on for or face box
    frameClone = frame.copy()

    # detect faces in the input frame, then clone the frame so that
    # we can draw on it
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
    	minNeighbors=5, minSize=(30, 30),
    	flags=cv2.CASCADE_SCALE_IMAGE)

    if len(rects) > 0:
    	# determine the largest face area
    	rect = sorted(rects, reverse=True,key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
    	(fX, fY, fW, fH) = rect

        # extract the face ROI from the image, then pre-process
        # it for the network
    	roi = gray[fY:fY + fH, fX:fX + fW]
    	roi = cv2.resize(roi, (48, 48))
    	roi = roi.astype("float") / 255.0
    	roi = img_to_array(roi)
    	roi = np.expand_dims(roi, axis=0)

        #Get emot values and maximum likely emotion
    	preds = model.predict(roi)[0]
    	label = EMOTIONS[preds.argmax()]

        #Choose to suppress grph output or not
    	if not s:
            # loop over the labels + probabilities and draw them
    		for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
        		# construct the label text
    			text = emotion
    			text2 = "{:.0f}%".format(prob * 100)

        		# draw the label + probability bar on the canvas
    			w = int(prob * 220)

    			cv2.rectangle(canvas, (80, (i * 25) + 140),(80+w, (i * 25) + 160), (colors[emotion]), -1)
    			cv2.putText(canvas, text, (10, (i * 25) + 152),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(5, 5, 5), 2)
    			cv2.putText(canvas, text2, (305, (i * 25) + 152),cv2.FONT_HERSHEY_SIMPLEX, 0.45,(5, 5, 5), 2)

        # draw the label on the frame
    	cv2.putText(frameClone, label, (fX, fY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    	cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),(0, 0, 255), 2)

    #Sync all seperate components and show
    frameClone = imutils.resize(frameClone, height = 300)
    merge = np.concatenate((canvas, frameClone), axis=1)
    all = np.concatenate((merge, sts.getScreen()), axis=0)

    #Output the full output
    cv2.imshow("Emotion Detection by PyImageSearch trained on Watson Machine Accelerator with IBM Watson Speech Services",all)

    #Video window controls: q to quit (needs waitKey to be assigned to variable)
    wait = cv2.waitKey(1)
    if wait & 0xFF == ord("q"):
        print("Quitting...")
        p.terminate()
        u_stop.set()
        break

    #k to kill connection to Watson
    if wait & 0xFF == ord("k"):
        if watson.value:
            print("Disconnecting from Watson...")
            watson.value = False

    #i to innitiate a connection with Watson
    if wait & 0xFF == ord("i"):
        if not watson.value:
            print("Connecting to Watson...")
            watson.value = True


    # s to suppress Emotion graph
    if wait & 0xFF == ord("s"):
        if s:
            s = False
        else:
            s = True

camera.release()
cv2.destroyAllWindows()
