# extract-sheets
Extract vocab data from collaborative Google Sheets

Original script by Axel Polleres - [https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html](https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html)

Modified script by Harshvardhan J. Pandit

Requires `python 3.6+`; packages: `requirements.txt`
Requires `html-tidy`

## instructions

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
4. Install requirements `pip install -r requirements.txt` and [tidy](http://www.html-tidy.org/)
   1. Highly recommended to use [virtualenv](https://virtualenv.pypa.io/en/stable/)
5. Run `./generate_docs.sh`

## code structure

* `extract_spreadsheet.py` downloads the Google Sheets document with one file per tab
* `extract_document.py` downloads the Google Docs specification document
* `clean_document.py` gets rid of all Google document structure and tidies up the HTML
* `generate_docs.sh` runs the above three, and additionally merges the document, and cleans it using the `tidy` tool

The generated files are in the docs folder