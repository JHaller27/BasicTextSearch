from textSearch import *


method = PrioritySearch()
searcher = TextSearcher(method)

with open('data/grimms_tales.txt', 'r') as fin:
    text = fin.read()
    text = text.replace('\n', ' ')
    for sentence in text.split('.'):
        searcher.add(sentence + ".")

print(repr(searcher))

terms = ["house", "the", "and", "good"]
print("Searching with [", " + ".join(terms), "]")
found = searcher.search(terms)

count = 0
for x in reversed(list(found)):
    count += 1

    print(x)
    print("=" * 60)

print(f"{count=}")
