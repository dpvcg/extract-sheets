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
    echo "extracting spreadsheet data for ${tab}"
    python3 ./extract_spreadsheet_data.py "$tab"
done
# generate combined rdf
echo "running RDF serializer"
python rdf_serializer.py
# # results are in a temporary file /tmp/dpvcg.html
# # insert tab files into documentation at line
# # format for import is #import tab_name.html
echo "Generating HTML docs"
cp ./docs/dpvcg.html ./docs/index.html
for tab in "${Tabs[@]}"
do
    echo "Generating HTML for ${tab}"
    sed -e "/#import ${tab}/{r docs/${tab}.html" -e "d}" ./docs/index.html > /tmp/dpvcg.html
    mv /tmp/dpvcg.html ./docs/index.html
done
# HTML spec for Legal Basis
cp ./docs/dpvcg-legal-basis.html ./docs/dpv-gdpr.html
echo "Generating HTML for Legal Basis"
sed -e "/#import LegalBasis/{r docs/LegalBasis.html" -e "d}" ./docs/dpv-gdpr.html > /tmp/dpvcg.html
mv /tmp/dpvcg.html ./docs/dpv-gdpr.html
# END
echo "DONE"
