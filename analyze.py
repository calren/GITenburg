import re
import operator
import sys
from urllib import urlopen
import yaml
import csv

# there's a common_english_words.txt file that lists the most common ~300 english words, we ignore those in our list
file = open("common_english_words.txt", 'r')
common_words = file.read().lower()
file.close()
text = re.sub('[^a-z\ \']+', " ", common_words)
common_words_list = list(common_words.split())

# get all books and get url for text
with open('/Users/carenchang/Desktop/repos_list.tsv') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect="excel-tab")
    for row in reader:
        book_name = row['gitb_name']
        book_file = "https://raw.githubusercontent.com/GITenberg/" + book_name + "/master/" + row['text_files'].strip('[]').split(", ")[0]
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

        # get file to save name
        book_yml_file = book_name + ".yml"

        with open(book_yml_file, 'w') as outfile:
            outfile.write( yaml.dump(sorted_unique_words[:49], default_flow_style=False) )

        # print( "total number of unique words: " + str(len(uniqueWords)));