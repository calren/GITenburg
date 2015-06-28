import re
import operator
import sys
from urllib import urlopen
import yaml
import csv

with open('/Users/carenchang/Desktop/repos_list.tsv') as csvfile:
    reader = csv.DictReader(csvfile)

# book_file should be the raw text file from github, such as
# https://raw.githubusercontent.com/GITenberg/Les-Mis-rables_135/master/135.txt
book_file = sys.argv[1]

# there's a common_english_words.txt file that lists the most common ~300 english words, we ignore those in our list
file = open("common_english_words.txt", 'r')
common_words = file.read().lower()
file.close()
text = re.sub('[^a-z\ \']+', " ", common_words)
common_words_list = list(common_words.split())

# get the file
file = urlopen(book_file, 'r')
# save the file in a list with all lower cased letters
text = file.read().lower()
file.close()
# take out anything that's not a letter
text = re.sub('[^a-z\ \']+', " ", text)
# split the words by spaces
words = list(text.split())

# for each words in the list of words, if it has already been seen increase its count, otherwise add it to the list
uniqueWords = dict();
for word in words:
    key = word
    if key in uniqueWords:
        uniqueWords[key] += 1
    elif key not in common_words_list:
        uniqueWords[key] = 1

# sort the list of unique words by most seen
sorted_unique_words = sorted(uniqueWords.items(), key=operator.itemgetter(1), reverse=True)
# sorted_unique_words_dict = dict(sorted(uniqueWords.items(), key=operator.itemgetter(1), reverse=True))

# print the most seen 50 words
#for k,v in sorted_unique_words[:49]:
#    print k, v
#print str(k) + " appears " + str(v) + " times"

# get file to save name
book_yml_file = book_file.split("/")[4] + ".yml"

with open(book_yml_file, 'w') as outfile:
    outfile.write( yaml.dump(sorted_unique_words[:49], default_flow_style=False) )

# print the number of total unique words


# print( "total number of unique words: " + str(len(uniqueWords)));