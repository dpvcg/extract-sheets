#!/usr/bin/env bash
#author: @coolharsh55

# generates documentation for all tabs in DPVCG document

# these are the tabs in the spreadsheet
declare -a Tabs=(
    "BaseOntology"
    "TechnicalOrganisationalMeasure"
    "PersonalDataCategory"
    "Processing"
    "Purpose"
    "RecipientsDataControllersDataSubjects"
    "LegalBasis"
    "Consent"
    )
# generate a html for each file in the tab
# this will saved as tab_name.html
for tab in "${Tabs[@]}"
do
    python3 ./extract_spreadsheet_data.py "$tab" > ./docs/${tab}.html
done
# download the documentation (Google Docs file)
python3 extract_document.py
# results are in a temporary file /tmp/dpvcg.html
# insert tab files into documentation at line
# format for import is #import tab_name.html
cp /tmp/dpvcg.html /tmp/dpvcg2.html
for tab in "${Tabs[@]}"
do
    sed -e "/#import ${tab}/{r docs/${tab}.html" -e "d}" /tmp/dpvcg2.html > /tmp/dpvcg3.html
    mv /tmp/dpvcg3.html /tmp/dpvcg2.html
done
rm /tmp/dpvcg.html
mv /tmp/dpvcg2.html docs/dpvcg.html
tidy docs/dpvcg.html > docs/dpvcg.html
# generate a nice index.html
tree docs -H '.' -L 1 --noreport --charset utf-8 -o docs/index.html
