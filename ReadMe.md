# ESTS
&nbsp;&nbsp;&nbsp;&nbsp;This is a demo developed using an emotion detector from [Watson Studio](www.ibm.com/Watson/Studio), and [Watson Studio](www.ibm.com/Watson/Studio) speech to text, translation, and sentiment analysis. This repository contains the project skeleton with the emotion detector, and the watson keys removed. The read me file will explain how to set up watson, and where to learn about the emotion detector. 

[Video of the Demo](https://youtu.be/VGxX9EylJA8)

*NOTE: This demo was run on Mac and Ubuntu, with python 3.6.5 or later. You may have different requirements.*

## Setting up your workspace 

**Set up your audio drivers:**

Mac `brew install portaudio` Further instructions [here](http://macappstore.org/portaudio/).

Ubuntu `sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools`

**Upgrade/Get Pip:**

&nbsp;&nbsp;&nbsp;&nbsp;`sudo pip --upgrade pip`

&nbsp;&nbsp;&nbsp;&nbsp;Instructions for installing pip are [here](https://pip.pypa.io/en/stable/installing/)

**Install dependencies:**

&nbsp;&nbsp;&nbsp;&nbsp;`sudo pip install -r requirements.txt`

## Getting Watson Studio Services 

Time to set up Watson Studio. Go to https://www.ibm.com/cloud/ and sign up for an account.

![IBM Cloud home page](/images/Picture1.png)

Sign up by clicking *"Sign up or log in"* and follow further prompts.

After you have signed up make sure you are signed in. Go to the top of the page and click on the search bar. Type in *Speech to Text* and click on the first catalogue result. 

![IBM Cloud Speech to text search](/images/Picture2.png)

Click on *Create* at the bottom right side of the screen. 

![Speech to text instance in IBM catalogue](/images/Picture3.png)

After creating the instance you will be redirected to the services getting started page. From here go to the top left of the screen and click on *Manage* 

![Picture of the Managment page for IBM cloud speech to text](/images/Picture4.png)

This page is important to keep open as we will be using the API Key later.

Next click on the search bar at the top of the window, and type in natural language translation. Right click the service to open in a new tab. Now create the resource and navigate to the manage page.

![Picture of searching Language Understanding](/images/Picture5.png)

Repeat the above steps by typing in Natural Language Understanding in the search bar. 

![Picture of looking for natural language understanding](/images/Picture6.png)

After creating the above resources open up ESTS.py and SpeechToText.py. We are now going to add your credentials to the program. Start by navigating to the Speech To Text service and clicking on the copy to clipboard button. 

![Apikey copy button](/images/Picture6.png)

Now open SpeechToText.py and go to line 98 and paste your apikey into the userpass variable value. 

![Placing apikey in SpeechToText.py](/images/Picture7.png)

Next open up the ESTS.py file and copy the apikey from the Language Translator and paste it into the iam_apikey variable value online 29. Repeat the same process for Natural Language Understanding on line 34. 

![ESTS.py credentials](/images/Picture8.png)

Now you are ready to run the code. Here are some problems to look out for:
- Bluetooth mic/headphones: If you are using bluetooth headphones with a mic, it may interrupt the speech to text feature. 
- Webcam connection: If a web cam is not attached to your workstation, the code will not run. 

## How to run the Code:  

In the terminal navigate to the directory where ESTS.py is located, and enter to command: `python ESTS.py -l french -w False`.

Supported languages are: Arabic, Czech, Danish, Dutch, Finnish, French, German, Hindi, Hungarian, Italian, Japanese, Korean, Norwegian, Polish, Portuguese, Russian', Simplified Chinese, Spanish, Swedish, Traditional Chinese, Turkish. 

That concludes the tutorial, and read me if you would like to contribute to the code in anyway please do. 



