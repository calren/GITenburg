import re
import operator
import sys

book_file = sys.argv[1]

file = open(book_file, 'r')
text = file.read().lower()
file.close()
text = re.sub('[^a-z\ \']+', " ", text)
words = list(text.split())
print len(words);

uniqueWords = dict();
for word in words:
    key = word
    if key in uniqueWords:
        uniqueWords[key] += 1
    else:
        uniqueWords[key] = 1

sorted_unique_words = sorted(uniqueWords.items(), key=operator.itemgetter(1), reverse=True)

for x in range(81, 120):
    print (sorted_unique_words[x]);
print(len(uniqueWords));