import wikibase, csv, time

pos_mapping = {"adjetivo": "Q6",
               "advérbio": "Q9",
               "nome": "Q7",
               "preposição": "Q10",
               "pronome": "Q11",
               "verbo": "Q8"}

def result_write(data):
    with open('data/data_leonor_uploaded.csv', 'a') as file:
        file.write(data)
    print(f"Saved row result: {data}")

with open ('data/data_leonor.csv') as file:
    data = csv.DictReader(file, delimiter="\t")
    row_before = None
    for row in data:
        print(f"\nNow processing {row}...")
        time.sleep(1)
        if not row_before:
            result_write("\t".join(row.keys()) + "\n")

        if row["Lema"] != "":
            if row["POS"] != "":
                lex_cat = pos_mapping[row["POS"]]
                print(f"Found POS {lex_cat}")
            new_lexeme = wikibase.bot.lexeme.new(lexical_category=lex_cat, language="Q4")
            new_lexeme.lemmas.set(language="pt", value=row["Lema"])
            new_lexeme.claims.add(wikibase.ExternalID(prop_nr="P9", value=row["ID"])) # takes for granted that lines with a lemma have something in column "ID"
            print(new_lexeme.get_json())
            new_lexeme.write()

        new_row = {"lexeme_uri": "https://llod-training.wikibase.cloud/entity/" + new_lexeme.id}
        for key in row.keys():
            if row[key] != "": # assumes that first row has something in every column
                new_row[key] = row[key]
            elif row_before:
                new_row[key] = row_before[key]
            else:
                new_row[key] = ""
        row_before = new_row
        result_write("\t".join(new_row.values()) + "\n")



