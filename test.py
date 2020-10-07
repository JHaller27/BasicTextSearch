from textSearch import *


searcher = TextSearcher()
method = PrioritySearch()

searcher.add("Hello world")
searcher.add("Hello, space")
searcher.add("Good bye, world")
searcher.add("Good bye space")
searcher.add("Bye y'all")
searcher.add("Howdy, y'all")

# print(searcher)

terms = ["Hello", "spaCe"]
print("Searching with [", " + ".join(terms), "] and", str(method))
found = searcher.search(terms, method)

print(list(found))
