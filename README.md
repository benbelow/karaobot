# Karaobot

## Local Setup

### Pre-requisites

* Python 3

### Setup

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

* Run `server.py` using flask
  * Required config:
    * environment variable of `DB_URI=postgresql+psycopg2://postgres:<mypassword>@localhost:5432/karaobot` 

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
