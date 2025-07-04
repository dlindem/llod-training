import llodtr_wikibase
import csv, time, re, json

# load semantic features mapping from CSV
with open('data/semantic_features_leonor.csv') as file:
    csvrows = csv.DictReader(file, delimiter=",")
    semfeat_mapping = {}
    for row in csvrows:
        semfeat_mapping[row["literal"]] = row["item"]
    input(f"\nLoaded semantic features:\n{semfeat_mapping}\nPress ENTER to continue\n")

with open ('data/senses_leonor.csv') as file:
    data = csv.DictReader(file, delimiter="\t")

    for row in data:
        print(f"\nNow processing {row}...")
        time.sleep(1)
        lexeme_id = row["Wikibase L-ID"]
        lexeme = llodtr_wikibase.bot.lexeme.get(entity_id=lexeme_id)

        new_sense = llodtr_wikibase.Sense()
        new_sense.glosses.set(language="pt", value=row["Definition"].strip())
        if row["Example"] != "":
            new_sense.claims.add(llodtr_wikibase.MonolingualText(prop_nr="P10", language="pt", text=row["Example"].strip()))
        print("Created new sense with definition and example")
        for semfeat in semfeat_mapping:
            if re.search(semfeat, row['semfeat']):
                semfeat_item = semfeat_mapping[semfeat]
                new_sense.claims.add(llodtr_wikibase.Item(prop_nr="P12", value=semfeat_item))
                print(f"Added semantic feature to sense: {semfeat_item}")
        if row['Coocorrente'] != "":
            new_sense.claims.add(llodtr_wikibase.MonolingualText(prop_nr="P11", language="pt", text=row["Coocorrente"].strip()))
            print(f"Added coocurrente: {row["Coocorrente"].strip()}")
        if row['sense_num'] != "":
            new_sense.claims.add(llodtr_wikibase.String(prop_nr="P16"))

        lexeme.senses.add(new_sense)
        #(json.dumps(lexeme.get_json(), indent=2))

        lexeme.write()




