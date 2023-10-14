# Karaobot

## Architecture Overview

There are a few components here: 

* SQL Database
  * Stores pre-analysed words and rhymes. When new words are encountered, they are added to this database once processed.
* Parody Server
  * Generates parodies of provided text via HTTP API
  * Requires: 
    * SQL Database
    * Similarity Server
* Similarity Server
  * HTTP API to wrap around Word2Vec (via gensim library)
  * This is a separate component as importing even a pre-trained corpus for Word2Vec increases the cold start time by at least 10 seconds or so,
  which isn't really suitable for quick changes / hotfixes to the main parody generation, where change (and bugs) are more likely
* MITM Proxy
  * Proxy which knows how to intercept calls to karafun, including: 
    * Replacing words of karaoke tracks with some parodied by the parody server
    * Pre-fetching tracks as they're queued, and pre-generating parody data
    * VERY rudimentary queuing of pre-fetched tracks

## Local Setup

### Pre-requisites

* Python 3

C tooling is required for some dependencies. 

On Mac I've had to add: `export C_INCLUDE_PATH="/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/include/python3.9"` 
to my bash profile, and after that pip install worked in a venv in PyCharm

### Setup

`python -m spacy download en_core_web_sm` to download spacy data

#### Database

* Install dependencies
  * `pip install -r requirements.txt`
* Set environment variable `DB_URI` pointing to local postgres instance


* Install dependencies
  * `pip install -r requirements.txt`
* [Coming soon] Download nltk corpus
  * [See docs](https://www.nltk.org/data.html)
  * `python -m nltk.downloader all`

__________________

## Running

Currently this is just a python script with hardcoded values.

Before running, you must first run the `setup.py` script to seed the database with processed words 

Required config: 

* `DB_URI=postgresql+psycopg2://postgres:<mypassword>@localhost:5432/karaobot`


To generate a parody:

#### As a REST API

* Run `parody/server.py` using flask
  * Required config:
    * environment variable of `DB_URI=postgresql+psycopg2://postgres:<mypassword>@localhost:5432/karaobot` 

* Run `similarity/server.py` using flask
  * Required: 
    * data/source_data/GoogleNews-vectors-negative300.bin (https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/)
    * This is git ignored as it's very very large, please set it up manually for now on servers running the similarity app

__________________

## Karafun integration (WIP)

To enjoy singing some auto-generated parodies live in front of your bewildered friends, simply:

* Install [mitmproxy](https://mitmproxy.org/)
* Run mitmproxy and navigate to [mitm.it/](mitm.it/)
* Install your certificate of choice (we are using Firefox)
* Set up your proxy
  * For Firefox, this is Settings > Proxy > Manual > localhost:8080 for http and https
* The mitmproxy addon is in the `mitmproxy-addons` directory. To use it, run `mitmproxy -s mitmproxy-addons/karafun.py`
  * Or if you prefer in web mode: `mitmweb -s mitmproxy-addons/karafun.py`
* Finally, open https://www.karafun.com/web/
