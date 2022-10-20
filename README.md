# Text to Speech

## Introduction

Optical character recognition (OCR) is the electronic or mechanical conversion of images of typed, handwritten or printed text into machine-encoded text.

Text to speech (TTS) is the use of software to create an audio output in the form of a spoken voice. 

This project built an end-to-end translation from text-image to speech. 

## Quick Start

1. Git clone or download this repository, and navigate to  `TextToSpeech`  folder.

  - go to [**Text to Speech**](https://github.com/tp6fu6m3/TextToSpeech)
  - [**Git clone**](https://github.com/tp6fu6m3/TextToSpeech.git) or [**download**](https://github.com/tp6fu6m3/TextToSpeech/archive/refs/heads/main.zip)
  - change directory to TextToSpeech
  - Install a few required pip packages (including OpenCV).

```
pip install -r requirements.txt
```

2. Download the text-image recognition data on Tesseract.
  - go to [**Tesseract**](https://github.com/UB-Mannheim/tesseract/wiki)
  - download [**tesseract-ocr**](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.2.0.20220712.exe)
  - tick  `Chinese`  in `Additional language data(download)` during installation



![Alt text](/img/1.png?raw=true "Optional Title")

![Alt text](/img/2.png?raw=true "Optional Title")

- add  `C:\your location\Tesseract-OCR`  into `Path` 

3. Download  `IP攝影機` on your mobile devices.

- go to setting->video overlay->text color, and change the Opacity from 100% to 0%
- Revise the  `LOCAL_URL` in  `main.py` 

![Alt text](/img/3.jpg?raw=true "Optional Title")

4. Demonstrate real time recognition.

```
python main.py
python main.py --camera        // Process this program on web-camera
python main.py --no_camera     // Process this program on local video
```

-   press `q` to quit the program
