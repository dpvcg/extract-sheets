#!/usr/bin/env bash
#author: @coolharsh55

# generates documentation for all tabs in DPVCG document

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

for tab in "${Tabs[@]}"
do
    python3 ./dpvcg-extract.py "$tab" > ./docs/${tab}.html
done

