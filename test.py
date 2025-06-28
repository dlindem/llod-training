import wikibase

item = wikibase.bot.item.new()

item.labels.set(language="en", value="hello")

item.write()

