import sys
import csv
from search import search_string, description

res = []

def cloze_word(sentense, word, level="1"):
    return sentense.lower().replace(word, "{{c"+level+"::"+word+"}}")


with open(sys.argv[1], 'r') as f:
    contents = f.read()
    items = contents.split("\n\n")
    for item in items:
        lines = item.split("\n")
        word = lines[0]
        exp = lines[1]
        eg = lines[2:]
        dct = search_string(word)
        exp2 = cloze_word(description(word), word, "1")
        for x in [{"sentence": cloze_word(x, word, "1"),"exp2": exp2, "exp": exp, "dict": dct  } for x in eg]:
            res.append(x)


with open('{0}.csv'.format(sys.argv[1]), 'w') as csv_file:
    fieldnames = ['sentence','exp2', 'exp', 'dict']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    for row in res:
        print(row['sentence'])
    writer.writerows(res)
