import re
import operator
import sys
from urllib import urlopen
import yaml
import csv
from collections import OrderedDict

# there's a common_english_words.txt file that lists the most common ~300 english words, we ignore those in our list
file = open("common_english_words.txt", 'r')
common_words = file.read().lower()
file.close()
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
        text = file.read()
        file.close()
        # take out all the text before the actual start of the book, such as gutenberg intro
        text = text.split(row['title'])[1]
        text = text.lower()
        # take out anything that's not a letter
        text = re.sub('[^a-z\ \']+', " ", text)
        text = re.sub(' [^a-z]+', "", text)
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
        sorted_unique_words_dict = OrderedDict((sorted_unique_words)[:199])
        
        # get file to save name
        book_yml_file = book_name + ".csv"
        
        with open(book_yml_file, 'wb') as f:    #w for python 2.7
            fieldnames = ['word', 'appearances']
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for k, v in sorted_unique_words_dict.items():
                w.writerow({'word' : k, 'appearances': v})
            w.writerow({'word' : "total unique words", 'appearances': str(len(sorted_unique_words))})

# print( "total number of unique words: " + str(len(uniqueWords)));

