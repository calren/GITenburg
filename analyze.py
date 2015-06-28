import re
import operator
import sys
from urllib import urlopen

book_file = sys.argv[1]

file = open("common_english_words.txt", 'r')
common_words = file.read().lower()
file.close()
text = re.sub('[^a-z\ \']+', " ", common_words)
common_words_list = list(common_words.split())


file = urlopen(book_file, 'r')
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
    elif key not in common_words_list:
        uniqueWords[key] = 1

sorted_unique_words = sorted(uniqueWords.items(), key=operator.itemgetter(1), reverse=True)
sorted_unique_words_dict = dict(sorted(uniqueWords.items(), key=operator.itemgetter(1), reverse=True))

for x in range(1, 50):
    print (sorted_unique_words[x]);
# print(len(uniqueWords));