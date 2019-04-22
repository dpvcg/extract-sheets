# extract-sheets
Extract vocab data from collaborative Google Sheets

Original script by Axel Polleres - [https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html](https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html)


## Running the script

1. Enable Google Spreadsheets API and download  `credentials.json` from [https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python)
2. Install [requirements](requirements.txt)
3. Run `python dpvcg-extract.py 'SHEET_NAME' > SHEET_NAME.html`
4. Running for the first time may open a browser window for OAuth verification
