# ESTS
<a href="http://example.com/" target="_blank">Hello, world!</a>
&nbsp;&nbsp;&nbsp;&nbsp;This is a demo developed using an emotion detector from <a href="www.pyimagesearch.com" target="blank">Pyimagesearch</a>, and [Watson Studio](www.ibm.com/Watson/Studio) speech to text, translation, and sentiment analysis. This repository contains the project skeleton with the emotion detector, and the watson keys removed. The read me file will explain how to set up watson, and where to learn about the emotion detector. 

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

**TO BE CONTINUED Skeleton:** 
right click open search in new tab for language translation, and natural language understanding 
create the resource and go to manage tab for these resources 
add the proper credentials to line 29 and 34 in ESTS.py
add the proper credential to line 98 in SpeechToText.py

Gotchas for the code:
- bluetooth mic/headphones
- not having web cam
- websocket client 
- improper sizing of numpy dimensions 

How to run the code  
Encourage editing and updating of code 



