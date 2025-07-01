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

rdffile = "data/bop_data.rdf"
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
# SELECT ?entryuri ?lemma 
# ?language ?pos ?gender 
# ?definition (group_concat(distinct ?form) as ?forms) 
select distinct ?pos

WHERE {
	?entryuri a ontolex:LexicalEntry ; rdfs:label ?lemma ; otv:language ?language.
			optional { ?entryuri otv:partOfSpeech ?pos .} 
			optional { ?entryuri otv:gender ?gender . }
			optional { ?entryuri skos:definition ?definition . }
			optional { ?entryuri ontolex:lexicalForm [ontolex:writtenRep ?form] . }
} group by ?entryuri ?lemma ?language ?pos ?gender ?definition ?forms
"""
print('Getting entries info with sparql...')
entries = g.query(entry_query, initNs=namespaces)
entrycount = 0
print(f"Got {len(entries)} SPARQL results.")

count = 0
for entry in entries:
	print(entry)
	continue
	count += 1
	print(f"[{count}/{len(entries)}] Now processing: {entry}")
	BOP_id = str(entry.entryuri)
	print(f"BOP ID is: {BOP_id}")
	lemma = str(entry.lemma)
	lang = entry.lemma.language
	pos = pos_map[entry.pos]
# 	entrycount += 1
# 	entryuri = str(entry.entryuri)
# 	lemmas = str(entry.lemmas)
# 	language = isolang_map[entry.language.n3()]
# 	if entry.pos:
# 		pos = ontology_map[entry.pos.n3()]
# 	else:
# 		pos = "Q19" # undefined POS
# 	print(f'\n[{str(entrycount)}] Now processing entry with original URI {entryuri}: lemmagroup {lemmas}, pos {pos}.')
# 	rewrite = False
# 	if entryuri in lexeme_map:
# 		continue
# 		# rewrite = True
# 		# lexeme = kwbi.wbi.lexeme.new(language=language, lexical_category=pos)
# 		# # lexeme = kwbi.wbi.lexeme.get(entity_id=lexeme_map[entryuri])
# 		# print('Found this lexeme on wikibase: ' + lexeme_map[entryuri])
# 		# print(str(lexeme.get_json()))
# 	else:
# 		time.sleep(0.2)
# 		lexeme = kwbi.wbi.lexeme.new(language=language, lexical_category=pos)
# 	for lem_lang in lemmas.split('|'):
# 		lem_lang_split = lem_lang.split('@')
# 		reallang = lem_lang_split[1]
# 		lemlang = wikilang_map[lem_lang_split[1]]
# 		lemtext = lem_lang_split[0]
# 		lexeme.lemmas.set(language=lemlang , value=lemtext)
# 	lexeme.claims.add(kwbi.URL(prop_nr='P11', value=str(entryuri)))
# 	lexeme.claims.add(kwbi.Item(prop_nr='P10', value=dictitem))
# 	if entry.gender:
# 		lexeme.claims.add(kwbi.Item(prop_nr='P13', value=ontology_map[entry.gender.n3()]))
#
# 	sensecount = 0
# 	for senseuri in entry.senses.split(' '):
# 		if not senseuri.startswith('http'):
# 			continue
# 		print('  Processing sense: '+senseuri)
# 		sensecount += 1
# 		# get sense level information
# 		sense_query = """
# 		SELECT DISTINCT ?senseuri
# 						(group_concat(concat(?def,"@",lang(?def));SEPARATOR="|") as ?definitions)
# 						(group_concat(str(?usguri);SEPARATOR="|") as ?usguris)
# 		WHERE {
# 			BIND(<""" + senseuri + """> as ?senseuri)
# 			?senseuri skos:definition ?def.
# 			 optional { ?senseuri ontolex:usage ?usguri. }
# 		} group by ?senseuri ?lemma ?definitions ?usguris """
#
# 		senses = g.query(sense_query, initNs=namespaces)
# 		for sense in senses:
# 			newsense = kwbi.Sense()
# 			newsense.claims.add(kwbi.URL(prop_nr='P11', value=senseuri))
# 			definitions = str(sense.definitions).split("|")
# 			print('Senseglosses: '+str(definitions))
# 			for definition in definitions:
# 				defsplit = definition.split('@')
# 				if len(defsplit) == 2:
# 					deftext = defsplit[0]
# 					deflang = defsplit[1]
# 				newsense.glosses.set(language=wikilang_map[deflang], value=deftext)
# 			usages = str(sense.usguris).split('|')
# 			if len(usages[0]) > 0:
# 				print('usages: ', str(usages))
#
# 				# get usage example level information
# 				usg_query = """
# 									SELECT DISTINCT ?usageuri (group_concat(concat(?usage,"@",lang(?usage));SEPARATOR="|") as ?usages)
# 									WHERE { BIND(<""" + senseuri + """> as ?senseuri)
# 									?senseuri ontolex:usage ?usageuri.
# 										?usageuri rdf:value ?usage.
# 									} group by ?usageuri ?usages """
#
# 				usgs = g.query(usg_query, initNs=namespaces)
# 				for usg in usgs:
# 					print(str(usg))
# 					xpllist = str(usg.usages).split('|')
# 					print('xpllist', str(xpllist))
# 					xpldict = {}
# 					for xpl in xpllist:
# 						usgsplit = xpl.split('@')
# 						xpldict[usgsplit[1]] = usgsplit[0]
# 					print(str(xpldict))
# 					qualifiers = kwbi.Qualifiers()
# 					qualifiers.add(kwbi.String(prop_nr='P14', value=reallang))
# 					qualifiers.add(kwbi.MonolingualText(prop_nr='P16', language="en", text=xpldict['en']))
# 					newsense.claims.add([kwbi.MonolingualText(prop_nr="P12", language="ku-latn",
# 															  text=xpldict[reallang], qualifiers=qualifiers)],
# 										action_if_exists=kwbi.ActionIfExists.FORCE_APPEND)
# 			lexeme.senses.add(newsense)
# 	print(f'    Added {str(sensecount)} senses to the lexeme.')
#
# 	formcount = 0
#
# 	for formuri in entry.forms.split(' '):
# 		if not formuri.startswith('http'):
# 			continue
# 		print('  Processing form: '+formuri)
# 		formcount += 1
# 		# get form level information
# 		form_query = """
# 		  SELECT DISTINCT ?formuri (lang(?wrep) as ?wreplang) ?wrep ?number ?gender WHERE {
# 		  BIND(<""" + formuri + """> as ?formuri)
# 			 ?formuri ontolex:writtenRep ?wrep.
# 			 optional { ?formuri lexinfo:number ?number . }
# 			 optional { ?formuri lexinfo:gender ?gender . }
# 			 # case, etc. should go here
# 		  } group by ?formuri ?wreplang ?wrep ?number ?gender"""
#
# 		forms = g.query(form_query, initNs=namespaces)
# 		for form in forms:
# 			grammatical_features = []
# 			if form.number:
# 				grammatical_features.append(ontology_map[form.number.n3()])
# 			if form.gender:
# 				grammatical_features.append(ontology_map[form.gender.n3()])
# 			newform = kwbi.Form()
# 			newform.grammatical_features = grammatical_features
# 			newform.representations.set(language=wikilang_map[str(form.wreplang)], value=str(form.wrep)) # we assume here cardinality 1 for ontolex:writtenRep
# 			newform.claims.add(kwbi.URL(prop_nr='P11', value=formuri))
# 			lexeme.forms.add(newform)
# 	print(f'    Added {str(formcount)} forms to the lexeme.')
#
# 	if rewrite:
# 		lexeme.id = lexeme_map[entryuri]
#
# 	done = False
# 	while not done:
# 		try:
# 			# print(str(lexeme.get_json()))
# 			lexeme.write(is_bot=True, clear=rewrite)
# 			done = True
# 		except Exception as ex:
# 			if "404 Client Error" in str(ex):
# 				print('Got 404 response from wikibase, will wait and try again...')
# 				time.sleep(10)
# 			else:
# 				print('Unexpected error:\n' + str(ex))
# 				sys.exit()
#
# 	with open('data/lexeme-mapping.csv', 'a') as mappingcsv:
# 		mappingcsv.write(entryuri + '\t' + lexeme.id + '\n')
# 	print('Finished processing ' + lexeme.id)

