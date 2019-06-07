# extract-sheets
Extract vocab data from collaborative Google Sheets

Original script by Axel Polleres - [https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html](https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html)

Modified script by Harshvardhan J. Pandit

Requires `python 3.6+`; packages: `requirements.txt`
~Requires `html-tidy`~


## code structure

* ~`extract_spreadsheet.py` downloads the Google Sheets document with one file per tab~
* `extract_document.py` downloads the Google Docs specification document
* `clean_document.py` gets rid of all Google document structure and tidies up the HTML
* `generate_docs.sh` runs the above three, and additionally merges the document, and cleans it using the `tidy` tool
* The generated files are in the `docs` folder
* The generated RDF files are in the `docs/rdf` folder
* The main page is `docs/dpvcg.html` which is rendered into `docs/index.html`
* The page for Legal basis is `docs/dpvcg-legal-basis.html` which is rendered into `docs/dpv-gdpr.html`

## How it all works

* Downloading vocabulary from Spreadsheet: The `extract_spreadsheet.py` script downloads the Google Spreadsheet data per tab, saves it as a HTML file in the `docs` folder, and a RDF file in the `docs/rdf` folder.
* The `docs/dpvcg.html` file is the "template"
* `generate_docs.sh` inserts the vocabularies in the `docs/dpvcg.html` file where the string "#import {vocab}" occurs.
* `rdf_serializer.py` serializes the RDF files, and combines all vocabularies into a single graph as `docs/rdf/dpv.ttl`
* The generated HTML documentation uses reSpec, which sorts out all the CSS and layout.   

## instructions

### Setting up the project
1. Enable Google Spreadsheets API
   1. Go to [Google Cloud Console](https://console.cloud.google.com/)
   2. Start a new project
   3. Go to the API section (from drop-down menu, top-left corner)
   4. Activate the following APIs from the Library section
      1. Google Sheets API
      2. Google Drive API
   5. Go back to the Credentials menu from the base menu (the one which shows Dashboard, Library, Credentials in the left sidebar)
   6. Select create new credentials of type "OAuth client ID"
      1. If asked, click on create consent screen (top-right corner)
      2. Fill in details (only a name is necessary), submit
      3. Select "web application" from offered choices
      4. Dismiss popup with ID and secret key
      5. Click on the download (down arrow in right corner) button for created app
2. Download / clone this repo
3. Put the downloaded json file in the repo with the name "credentials.json"
4. Install requirements `pip install -r requirements.txt` ~and [tidy](http://www.html-tidy.org/)~
   1. Highly recommended to use [virtualenv](https://virtualenv.pypa.io/en/stable/)

### Edit the HTML files (only)
1. Edit files in `docs` folder (only edit the following files)
   1. `docs/dpvcg.html`
   2. `docs/dpvcg-legal-basis.html`
2. run `./generate_docs.sh`

### Sync with spreadsheet
1. run `./generate_docs.sh --spreadsheet`

### Working offline
1. The data is saved in `pickled` folder.
2. run `./generate_docs.sh --spreadsheet --cache`
