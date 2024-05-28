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


# How to add custom words

(a) Add to the custom words and custom phrases files
* MAKE SURE THEY'RE ALL LOWER CASE AND FREE FROM PUNCTUATION FOR MAXIMAL EFFECTIVENESS

(b) Fix scansion

* Custom words in custom words/phrases files will be automatically added and analysed
* If any of them are not successfully analysed, they will be logged in `need_manual_db_tweaks`
* Go to the database (using e.g. DBeaver or Datagrip) and update the `stress` column
  * P = primary stress. Big stress
  * S = secondary stress. Not super stressed but a bit I guess.
  * U = unstressed. 
  * Look at some examples to make sure you match

Most common examples of stresses: 

(taken direct from a SQL query)
PU	10826	aaron	abbe	abbey
P	6978	1	2	aah
UPU	4183	abandon	abandoned	abandons
PUU	3765	abacus	abler	absalom
UP	2751	aback	abash	abashed
PS	2200	aardvark	abscess	access
UPUU	1954	abandonment	abdominal	abilities
PUS	1858	abattoir	abdicate	abdicates
SUPU	1337	abalone	abdication	aberration
PUSU	1035	abdicated	abdicating	abrogated
PSU	675	abstracted	accessing	airlifted
SUPUU	636	abnormalities	abnormality	abolitionist
SUP	436	absentee	absentees	acquiesce
UPUSU	408	abbreviated	abbreviating	accelerated
PUUU	376	accuracies	accuracy	accurately
UPUS	322	abbreviate	abbreviates	accelerate
UPUUU	235	abominable	accompanying	additionally
USUPU	225	abbreviation	abbreviations	abomination
SUUPU	157	academician	academicians	aerodynamic
PP	154	2d	ac	aimee
UUPU	130	absolutist	adriano	automation
SP	115	aha	aj	alright
SPU	112	alfalfa	angelic	archangel
U	87	a	a-	a.
UUP	83	achingly	appointee	appointees
USUPUU	82	accelerometer	accelerometers	acceptability
SUUPUU	79	accessibility	aerodynamically	amiability
UUPUU	69	ambiguities	biologically	chromatography
PUUSU	65	aleatory	alienated	alienating
SPUU	65	alluvial	antecedent	asymmetries
PUUS	63	actualize	aftereffect	aftereffects
UPS	60	adulthood	aforesaid	aforethought
PUP	57	amputee	amputees	anchormen
PPU	53	addresses	archbishop	archetypal
SUPUUU	44	agriculturalist	agriculturally	architecturally
SUPUSU	38	beneficiaries	beneficiary	differentiated
PUPU	25	deputation	duodenal	easygoing
PUSUU	25	amphitheatre	arbitrarily	arbitrariness
SUPUS	25	archipelago	braggadocio	differentiate
SUUP	25	aquamarine	cabriolet	catamaran
UPUUSU	21	ameliorated	anticipatory	articulatory
PSUU	19	airworthiness	backfiring	bicycling
USUUPU	19	acidification	detoxification	disorientation
SUSUPU	17	bioengineering	discontinuation	endometriosis
SSUPU	15	acceleration	antidepressants	asymptomatic
SSPU	13	anticancer	asbestosis	cappuccino
SUSUPUU	13	autobiographical	biotechnological	comprehensibility
USUP	13	comedienne	communiques	concessionaire
UUUPU	12	disinclination	equivocation	exoneration
UPSU	11	aforementioned	escapism	impregnated
USPU	11	departmental	electronic	electronics
PPUU	10	archdiocese	archenemy	asynchronous
SSPUU	10	bougainvillea	conductivity	domesticity
USP	10	abductee	abductees	detainees
UUSUPU	10	chlorofluorocarbon	decontamination	differentiation
PPP	9	abs	api	byu
PUUUU	9	amateurism	caricaturist	cumulatively
SPUS	9	deactivate	iconoclast	interpolate
SPUSU	9	allegiances	deactivated	exculpatory
SPUUU	9	autonomously	concomitantly	extravagantly
UPPU	9	dislocation	dislocations	disputation
UPUUS	9	corroborative	deteriorate	deteriorates
SUPS	8	antiaircraft	carbohydrate	elephantine
SUPUP	8	xxi	xxii	xxiii
SSUPUU	7	advisability	dendrochronology	humanitarian
UPP	7	alongside	attendee	attendees
UPUSUU	7	appreciatively	environmentalists	identifiable
UUPUUU	7	inappropriately	indistinguishable	internationalist
UUUPUU	7	experimentally	gubernatorial	irregularities
PUUP	6	overproduced	overreact	videotape
SUSPU	6	ferromagnetic	instrumentation	jurisprudential
SUSPUU	6	bacteriology	biotechnology	extraterrestrials
SUUUPU	6	atherosclerosis	counterrevolution	macroeconomic
UUPUS	6	differentiates	incapacitate	insubordinate
UUPUSU	6	decontaminated	incapacitated	incapacitating
PSP	5	franchisee	hitherto	microchip
UPUPU	5	coagulation	miscalculation	miscalculations
USUUPUU	5	electromechanical	incompatibility	individuality
PSS	4	elbowroom	nobodies	nobody
PUUPU	4	minicomputer	minicomputers	overproduction
SUPUUUU	4	hypersensitivity	multiculturalism	multilateralism
SUU	4	gasify	greedier	greediest
SUUUPUU	4	epidemiologist	epidemiologists	heterogeneity
USPUU	4	electricity	electrolysis	familiarity
UUUP	4	interviewee	interviewees	reintroduce
PSSU	3	lobotomy	moviegoers	retrofitted
PUSSU	3	absolutism	alcoholism	parallelism
SU	3	rumour	rumours	tonsil
SUPSU	3	multiprocessor	opportunism	reincarnated
SUUPUS	3	generalissimo	megalomaniac	verisimilitude
UUPS	3	biofeedback	disenfranchise	disenfranchised
PPUSU	2	reactivated	reactivating	
PSUPU	2	microcomputer	microcomputers	
PSUS	2	midafternoon	newspaperman	
PUPUS	2	overemphasize	underestimate	
PUUPUU	2	interrelationship	overcapacity	
SPS	2	trusteeship	zydeco	
SSP	2	denouement	rapprochement	
SSUPUUU	2	unceremoniously	unconstitutionally	
SUPUPU	2	xxvii	xxxvii	
SUPUUSU	2	interdisciplinary	unilateralism	
SUSP	2	arbitrageurs	indochinese	
SUSUUPU	2	individualistic	misidentification	
SUUPS	2	corticosteroid	corticosteroids	
SUUPUSU	2	cardiopulmonary	individualism	
SUUSUPU	2	telecommunication	telecommunications	
SUUUUPUU	2	epidemiological	heterosexuality	
UPUUUU	2	accountability	imaginatively	
USUPUSU	2	electromagnetism	intellectualism	
USUPUUSU	2	authoritarianism	egalitarianism	
USUPUUU	2	conspiratorially	contemporaneously	
USUSPU	2	electrodynamic	electrodynamics	
USUU	2	expressionless	purportedly	
UUPUUSU	2	internationalism	oversimplification	
UUSUPUU	2	irresponsibility	unavailability	
UUUPUS	2	idiosyncrasies	idiosyncrasy	
UUUUPU	2	idiosyncratic	unenthusiastic	
PPS	1	blacksmithing		
PPUS	1	reactivate		
PPUUP	1	110		
PSPU	1	indexation		
PSPUU	1	receptivity		
PUPUPU	1	chlorofluorocarbons		
PUPUSU	1	underestimated		
PUPUU	1	overshadowing		
PUPUUSU	1	nondiscriminatory		
PUPUUU	1	operationally		
PUSUPU	1	overrepresented		
PUSUS	1	overqualified		
PUUUPUU	1	radioactivity		
SPPU	1	oxymoron		
SPUSUU	1	excruciatingly		
SPUUSU	1	participatory		
SSSPU	1	disadvantageous		
SSUP	1	realpolitik		
SSUPUUSU	1	totalitarianism		
SSUUPU	1	uncharacteristic		
SSUUPUU	1	uncharacteristically		
SSUUU	1	unanswerable		
SUS	1	cogitate		
SUSSPUU	1	superconductivity		
SUSUP	1	multimillionaire		
SUSUU	1	endometrial		
SUUPUUU	1	ritualistically		
SUUS	1	heterodox		
SUUSPUU	1	immunodeficiency		
SUUUPUSU	1	counterrevolutionary		
UPPS	1	impolitic		
UPSS	1	electroshock		
UPSUSU	1	conciliatory		
UPSUU	1	unenviable		
UPUSUSU	1	environmentalism		
USPUUU	1	electronically		
USSSUPU	1	socioeconomic		
USU	1	accredit		
USUPUUS	1	electrocardiogram		
UUPSU	1	disenfranchisement		
UUPSUU	1	unimaginative		
UUS	1	impolite		
UUU	1	tourniquet		
UUUPUSU	1	undifferentiated		
UUUUSU	1	electrophoresis		