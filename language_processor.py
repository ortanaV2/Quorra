import time
import argparse
from transformer import json_call

parser = argparse.ArgumentParser(description='Processes the dataset and responses to requests.')
parser.add_argument('--inp', dest='INPUT', default="Why there is a chicken crossing road? Do you know?", type=str, help='Request input')
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

def keyword_search(word:str) -> list[str] | None:
    """Searches for keyword in dataset and returns the possible words."""
    for key in DATASET.keys():
        if str(key) == word:
            return DATASET[key]

#tokenize input
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
print(input_set)

filtered_inp_set = []
#filter out symbols of sentence_set(input)
for single_inp in input_set:
    word_list = single_inp.split() #raw word_list
    filtered_word_list = [] #word_list without symbols
    for word in word_list: filtered_word_list.append(filter_symbol(word))
    filtered_inp_set.append(filtered_word_list)
#output --> input_set without symbols


#following code probably not useful (delete/change later)
#process input
DATASET = json_call("dataset.json", "r")
for single_inp in filtered_inp_set:
    #searching for appending words chain
    for index, word in enumerate(single_inp): 
        appending_words = keyword_search(word) #next words according to dataset
        if (index+1) < len(single_inp): 
            next_word = single_inp[index+1] #next word from input
        else: 
            next_word = None
            
        print(word, next_word, appending_words) #debug

        #following snippet makes no logical sense
        #NOTE: change later and check if there is another word with the same meaning
        if (appending_words and next_word) is not None:
            if next_word not in appending_words:
                #check if other word links to next_word and put it behind it (is this) --> (this is)
                for possible_word in appending_words:
                    check_next_word = keyword_search(possible_word)
                    if check_next_word is not None:
                        if next_word in check_next_word:
                            single_step_word = possible_word
                                   
