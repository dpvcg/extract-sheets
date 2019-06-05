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
    python3 ./extract_spreadsheet_data.py "$tab"
done
# generate rdf
# python rdf_serializer.py
# # download the documentation (Google Docs file)
# python3 extract_document.py
# python3 clean_document.py
# # results are in a temporary file /tmp/dpvcg.html
# # insert tab files into documentation at line
# # format for import is #import tab_name.html
cp ./docs/dpvcg.html ./docs2/index.html
for tab in "${Tabs[@]}"
do
    sed -e "/#import ${tab}/{r docs2/${tab}.html" -e "d}" ./docs2/index.html > /tmp/dpvcg.html
    mv /tmp/dpvcg.html ./docs2/index.html
done
# # clean the HTML
# tidy -config tidy.config /tmp/dpvcg.html > docs/dpvcg.html
# # remove temporary files
# rm /tmp/dpvcg.html
# # generate a nice index.html
# tree docs -H '.' -L 1 --noreport --charset utf-8 -o docs/index.html
