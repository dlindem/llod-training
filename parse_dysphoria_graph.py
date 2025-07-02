from rdflib import Graph, URIRef
import time, sys

# # load existing lexemes lookup table
# with open('data/bop_lexeme-mapping.csv') as mappingcsv:
# 	mappingrows = mappingcsv.read().split('\n')
# 	lexeme_map = {}
# 	for row in mappingrows:
# 		print(row)
# 		mapping = row.split('\t')
# 		if len(mapping) == 2:
# 			lexeme_map[mapping[0]] = mapping[1]
# print(f'Loaded {str(len(lexeme_map))} existing lexeme mappings.')

pos_map = {
	"noun": "Q11",
	"none": "Q12"
}

lang_map = {
	"de": "Q13",
	"en": "Q15",
	"fr": "Q14"
}

gender_map = {
	"none": "",
	"masculine": "",
	"feminine": "",
	"neuter": ""
}

rdffile = "data/GenderDysphoria.ttl"
# dictitem = "Q38"

# parse TTL
g = Graph()
g.parse(rdffile)
print('RDF loaded.')

# g.serialize(destination="data/bop_data.ttl")
# sys.exit()

namespaces = {} # build the ns prefix object for rdflib sparql initNs
for ns_prefix, namespace in g.namespaces():
	namespaces[ns_prefix] = URIRef(namespace)

# get entry level information
entry_query = """
SELECT ?owl_class

WHERE {
	?owl_class rdf:type owl:Class
} 
"""
print('Getting entries info with sparql...')
entries = g.query(entry_query, initNs=namespaces)
entrycount = 0
print(f"Got {len(entries)} SPARQL results.")

count = 0
for entry in entries:
	print(str(entry.owl_class))
