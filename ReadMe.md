# ESTS
&nbsp;&nbsp;&nbsp;&nbsp;This is a demo developed using an emotion detector from [Pyimagesearch](www.pyimagesearch.com), and [Watson Studio](www.ibm.com/Watson/Studio) speech to text, translation, and sentiment analysis. This repository contains the project skeleton with the emotion detector, and the watson keys removed. The read me file will explain how to set up watson, and where to learn about the emotion detector. 

[Video of the Demo](https://youtu.be/VGxX9EylJA8)

*NOTE: This demo was run on Mac and Ubuntu, with python 3.6.5 or later. You may have different requirements*

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

Time to set up Watson Studio. Go to https://dataplatform.cloud.ibm.com/ and sign up for the free trial. This will give you access to the service for 1 month free. 

![Sign up page for Watson Studio](/images/Picture1.png)

