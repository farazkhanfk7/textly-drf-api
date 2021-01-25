  
  
 <img src="https://github.com/batcypher/bash/blob/main/IMG_20210125_092915.jpg">

![python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)   [![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)

# Textly-DRF-API
> An open-source API for text correction.

All-in-one API for the grammar correction, spell check, sentiment analysis,Text Summary,text Generation, Neural Machine Translation (German to  English).
Textly was build with [Django-Rest-Framework](https://www.django-rest-framework.org/) and is based on Natural Language Processing. It uses many Deep Learning models like GPT2, BERT for text analysis.

## Deep Learning Models
* **Bidirectional Encoder Representations from Transformers (BERT)**
* **Generative Pretrained Transformer 2 (GPT-2)**
* **Seq2Seq LSTM Model built using PyTorch**
* **Bart-Large-CNN**

## Get Started
> Use a virtual env
* Clone repo : ```$ git clone https://github.com/farazkhanfk7/textly-drf-api```
* ```$ cd django-rest-api```
* Create a virtualenv: ```$ mkvirtualenv env``` or ```$ python -m venv env```
* Activate env : ```$ workon env``` or ```$ source env/bin/activate```

**Download Models**
> Run this shell script to download models to their respective folders.
```
$ sh load_model.sh
```
**Install dependencies** 
```
$ pip install -r requirements.txt
```

**Run project locally**
```
$ python manage.py runserver
```

**Run project with Docker** 
* Build Docker Image
```
$ docker-compose build
```

* Run Container
```
$ docker-compose up
```

## API Endpoint

* http://127.0.0.1:8000/gcapi/check/
> Takes a sentence through POST request and performs Grammer-Check and sentiment analysis. 

* http://127.0.0.1:8000/gcapi/generate/
> Takes a sentence through POST request and runs text-generation model to predict next words. 

* http://127.0.0.1:8000/gcapi/spell/
> Takes a sentence through POST request and correct spellings. 

* http://127.0.0.1:8000/gcapi/summary/
> Returns the summary of a large text entered by user.

* http://127.0.0.1:8000/gcapi/translate-german/
> Translates German text to English
