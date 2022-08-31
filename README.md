# Karaobot

## Local Setup

### Pre-requisites

* Python 3

### Setup

* Install dependencies
  * `pip install -r requirements.txt`
* [Coming soon] Download nltk corpus
  * [See docs](https://www.nltk.org/data.html)
  * `python -m nltk.downloader all`

__________________

## Running

Currently this is just a python script with hardcoded values.

To generate a parody:

#### Via Genius

* Replace the artist name and song name in the `fetch_lyrics` call of `main.py` with the target song details

#### From local input

* Remove the line fetching original lyrics from genius (`fetch_lyrics` in `main.py`)
* Modify `input.txt` with your desired input

* Output lyrics will be written to `output.txt`

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
