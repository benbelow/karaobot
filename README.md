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

## Local Setup / Zero to Hero

1) Install [pre-reqs](#pre-requisites)
2) Set up [database](#database)
3) Set up [initial words](#initial-data)
4) Run [parody server](#as-a-rest-api)
5) Run [similarity server](#as-a-rest-api)
6) [Configure proxy settings and run proxy server](#karafun-integration-wip)

### Pre-requisites

#### Python 3

C tooling is required for some dependencies. 

On Mac I've had to add: `export C_INCLUDE_PATH="/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/include/python3.9"` 
to my bash profile, and after that pip install worked in a venv in PyCharm

This can be a real pain! 
Recommend: 
* use brew to install python
* stick to python 3.9
  * This is pretty vital, I've seen it break a lot with later versions and haven't spent time seeing if it's fixable - but some migration work is needed if so. 
* use a venv


* `python -m spacy download en_core_web_sm` to download spacy data
  * will need to first `pip install spacy`

#### Windows specific setup

* VSCode sometimes seems to not update PATH for new terminals spawned, need to reset the whole editor


### Setup

#### Database

* Install dependencies
  * `pip install -r requirements.txt`
* Set environment variable `DB_URI` pointing to local postgres instance
* run `schema.py` to create initial schema
* Required config:
  * `DB_URI=postgresql+psycopg2://postgres:password@localhost:5438/karaobot`

You might need to install some dependencies manually at some point in this process: 
e.g: 
* sqlalchemy
* psycopg2
  * this may fail to install, you can just install a pre-compiled version:
  * `pip install psycopg2-binary`

* [Coming soon] Download nltk corpus
  * [See docs](https://www.nltk.org/data.html)
  * `python -m nltk.downloader all`
__________________

#### Initial Data

Before running, you must first run the `setup.py` script to seed the database with processed words 

Required config: 

* `DB_URI=postgresql+psycopg2://postgres:<mypassword>@localhost:5438/karaobot`


## Running

To generate a parody:

#### As a REST API

* Run `parody/server.py` using flask
  * Required config:
    * environment variable of `DB_URI=postgresql+psycopg2://postgres:password@localhost:5438/karaobot`
  * Command line: 
    `export FLASK_APP=parody/server.py;export DB_URI=postgresql+psycopg2://postgres:password@localhost:5438/karaobot;flask run`

* Run `similarity/server.py` using flask
  * Run on port 5001 via `-p 5001`
  * Required: 
    * data/source_data/GoogleNews-vectors-negative300.bin (https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/)
    * This is git ignored as it's very very large, please set it up manually for now on servers running the similarity app
  * Command line:
    `export FLASK_APP=similarity/server.py;flask run -p 5001`

__________________

## Karafun integration (WIP)

To enjoy singing some auto-generated parodies live in front of your bewildered friends, simply:

* Install [mitmproxy](https://mitmproxy.org/)
* Run mitmproxy and navigate to [mitm.it/](mitm.it/)
* Install your certificate of choice (we are using Firefox)
* Set up your proxy
  * For Firefox, this is Settings > Proxy > Manual > localhost:8080 for http and https
* The mitmproxy addon is in the `proxy` directory. To use it, run `mitmproxy -s proxy/karafun.py`
  * Or if you prefer in web mode: `mitmweb -s proxy/karafun.py`
* Finally, open https://www.karafun.com/web/

### On Dependencies

I swear I've run this successfully before without doing this, but on my most recent attempt (May 2024), I'm getting issues
relating to a lack of xml.etree.ElementTree when mitmproxy was installed via brew

It looks like this is because the compiled version has minimal python deps, and so I've followed the instructions here: https://docs.mitmproxy.org/stable/overview-installation/#fn:1

This means: 
* install via pipx, not brew
* inject all modules required via `pipx inject mitmproxy <dep>`