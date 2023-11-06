import time
import argparse
from TextDataPrep import json_call

parser = argparse.ArgumentParser(description='Processes the dataset and responses to requests.')
parser.add_argument('--inp', dest='INPUT', default="Why is there a chicken crossing the road? Do you know?", type=str, help='Request input')
args = parser.parse_args()
inp = args.INPUT

__name__ = "LanguageProcessor"
class MissingInput(Exception):
    def __init__(self, message="Missing input for further operations. {--inp (str)}"):
        self.message = message
        super().__init__(self.message)
if inp is None: raise MissingInput #Error if missing input (--inp (str))

def filter_symbol(word:str) -> str:
    """Filters out the symbols in a single word."""
    filtered_word = []
    for symbol in str(word): 
        if symbol.isalpha(): filtered_word.append(symbol)
    filtered_word = "".join(filtered_word)
    return str(filtered_word)

def keyword_search(word:str):
    """Searches for keyword in dataset and returns the possible words."""
    for key in DATASET.keys():
        if str(key) == word:
            return DATASET[key]

def spelling_check(word:str) -> str:
    """Spellchecker using bag_of_words.json list. (compares index_match and len_match)"""
    bow = json_call("bag_of_words.json", "r")
    leader = [word, 0]
    for bow_word in bow:
        if len(bow_word) < len(word) - 1 or len(bow_word) > len(word) + 1:
            continue
        matches = 0
        for i in range(min(len(word), len(bow_word))):
            if word[i] == bow_word[i]:
                matches += 1
        if matches > leader[1]:
            leader = [bow_word, matches]
    return leader[0]

#tokenize input
if ("!" or "?" or ".") not in inp: inp = inp+"." #add because of type.error in *sort by sentences*
sentence_set = []
single_set = []
#sort by sentences
for word in inp.split():
    if "!" in word or "?" in word or "." in word:
        single_set.append(word.lower())
        sentence_set.append(single_set)
        single_set = []
    else:
        single_set.append(word.lower())
input_set = []
for sentence in sentence_set: input_set.append(" ".join(sentence))
#output --> input_set

filtered_inp_set = []
#filter out symbols of sentence_set(input)
for single_inp in input_set:
    word_list = single_inp.split() #raw word_list
    filtered_word_list = [] #word_list without symbols
    for word in word_list: filtered_word_list.append(filter_symbol(word))
    filtered_inp_set.append(filtered_word_list)
#output --> input_set without symbols

# --> following new processing system