"""serialize metadata from sheets into RDF files."""
from rdflib import Graph

VOCABS = [
    "BaseOntology",
    "TechnicalOrganisationalMeasure",
    "PersonalDataCategory",
    "Processing",
    "Purpose",
    "RecipientsDataControllersDataSubjects",
    "LegalBasis",
    "Consent",
]

PREFIXES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'dct': 'http://purl.org/dc/terms/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'time': 'http://www.w3.org/2006/time#',
    'odrl': 'http://w3.org/ns/odrl/2/',
    'prov': 'http://www.w3.org/ns/prov#',
    'spl': 'http://www.specialprivacy.eu/langs/usage-policy#',
    'svd': 'http://www.specialprivacy.eu/vocabs/data#',
    'svpu': 'http://www.specialprivacy.eu/vocabs/purposes#',
    'svpr': 'http://www.specialprivacy.eu/vocabs/processing#',
    'svr': 'http://www.specialprivacy.eu/vocabs/recipients#',
    'svl': 'http://www.specialprivacy.eu/vocabs/locations#',
    'svdu': 'http://www.specialprivacy.eu/vocabs/duration#',
    'sw': 'http://www.w3.org/2003/06/sw-vocab-status/ns#',
    'dpv': 'http://w3.org/ns/dpv#',
    'dpv-gdpr': 'http://w3.org/ns/dpv-gdpr#',
}

with open('./docs/rdf/ontology_metadata.ttl', 'r') as fd:
    ontology_metadata = fd.read()
with open('./docs/rdf/ontology_legal_basis_metadata.ttl', 'r') as fd:
    ontology_legal_basis_metadata = fd.read()


def validate_rdf(vocab):
    """Validate file. will throw errors."""
    g = Graph()
    g.parse(f'./docs/rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./docs/rdf/{vocab}.ttl', format='ttl')
    # TODO: add more formats


def detect_prefixes(code):
    '''detect which prefixes are used in the code'''
    prefixes = set()
    keys = [(p, p + ':') for p in PREFIXES.keys()]
    for item in code:
        for line in item:
            for prefix, notation in keys:
                if notation in line:
                    prefixes.add(prefix)
    return prefixes


def serialize_rdf(name, code):
    prefixes = detect_prefixes(code)
    with open(f'./docs/rdf/{name}.ttl', 'w') as fd:
        for prefix in prefixes:
            fd.write(f"@prefix {prefix}: <{PREFIXES[prefix]}> .")
            fd.write('\n')
        if name == "LegalBasis":
            fd.write(ontology_legal_basis_metadata)
        else:
            fd.write(ontology_metadata)
        fd.write('\n')
        for item in code:
            fd.write(' ;\n'.join(item) + ' .\n\n')
    validate_rdf(name)


def combine_graphs(vocabs=VOCABS):
    g = Graph()
    vocabs.remove('LegalBasis')
    for vocab in vocabs:
        g.parse(f'./docs/rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./docs/rdf/dpv.ttl', format='ttl')
    # TODO: add more formats


if __name__ == '__main__':
    combine_graphs()