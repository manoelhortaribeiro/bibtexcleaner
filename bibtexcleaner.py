import bibtexparser
import argparse

parser_args = argparse.ArgumentParser(description='Cleans bibtex.')
parser_args.add_argument('--src')
parser_args.add_argument('--dst')

args = parser_args.parse_args()

src = args.src
dst = args.dst

parser = bibtexparser.bparser.BibTexParser(common_strings=True)

with open(src) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file, parser=parser)

fields_to_keep = {
    "book": ["ID", "title", "author", "year", "publisher"],
    "inproceedings": ["ID", "title", "booktitle", "author", "year"],
    "article": ["ID", "title", "author", "journal", "year", "pages"],
    "incollection": ["ID", "title", "booktitle", "year", "author", "publisher", "pages"],
    "misc": ["ID", "title", "url"]
}

new_database = bibtexparser.bibdatabase.BibDatabase()

new_entries = []
for i in bib_database.entries:
    try:
        to_keep = fields_to_keep[i["ENTRYTYPE"]]
        tmp = {"ENTRYTYPE": i["ENTRYTYPE"]}
        for j in to_keep:
            if j in i:
                tmp[j] = i[j]
        new_entries.append(tmp)
    except:
        continue

new_database.entries = new_entries

writer = bibtexparser.bwriter.BibTexWriter()
with open(dst, 'w') as bibtex_file:
    bibtex_file.write(writer.write(new_database))
