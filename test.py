from textSearch import *


searcher = TextSearcher()
method = PrioritySearch()

with open('data/grimms_tales.txt', 'r') as fin:
    text = fin.read()
    text = text.replace('\n', ' ')
    for sentence in text.split('.'):
        searcher.add(sentence)

# print(searcher)

terms = ["house", "the", "and", "good"]
print("Searching with [", " + ".join(terms), "] and", str(method))
found = searcher.search(terms, method)

count = 0
for x in found:
    count += 1

    print(x)
    print("=" * 60)

print(f"{count=}")
