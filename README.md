# extract-sheets
Extract vocab data from collaborative Google Sheets

Original script by Axel Polleres - [https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html](https://lists.w3.org/Archives/Public/public-dpvcg/2019Apr/0098.html)

Modified script by Harshvardhan J. Pandit

Requires python 3.6+; 
Requires html-tidy

## Running the script

1. Enable Google Spreadsheets API and download  `credentials.json` from [https://developers.google.com/sheets/api/quickstart/python](https://developers.google.com/sheets/api/quickstart/python)
2. Install [requirements](requirements.txt)
3. Run `./generate_docs.sh`

To only generate HTML version of tabs in sheet, run `python3 extract_spreadsheet_data.py 'SHEET_NAME' > SHEET_NAME.html`

