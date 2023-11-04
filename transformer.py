import json

class DataNotGiven(Exception):
    """
    Error for json_call() if data is not given.
    """
    def __init__(self, message="Asked for data but None was given."):
        self.message = message
        super().__init__(self.message)

def json_call(path:str, call_type:str, data=None):
    """
    Compressed json reading and writing function.
    call_type: ('r', 'w')
    """
    if call_type == "r":
        with open(path, call_type) as json_file:
            data = json.load(json_file)
        return data
    if call_type == "w":
        if data is None:
            raise DataNotGiven
        else:
            with open(path, call_type) as json_file:
                json.dump(data, json_file)

training_text = (open("./tmp/training_text.txt", "r").read()).split() #get training text

#tokenize training text
sentence_set = []
single_set = []
#sort by sentences
for word in training_text:
    if "!" in word or "?" in word or "." in word:
        single_set.append(word)
        sentence_set.append(single_set)
        single_set = []
    else:
        single_set.append(word)
separated_set = []
for sentence in sentence_set: separated_set.append(" ".join(sentence))

dataset:dict = json_call(path="dataset.json", call_type="r") #load json dataset file
for inp in separated_set:
    symbol_list = []
    #filter out symbols
    for symbol in inp:
        if (symbol.isalpha()) or (symbol == " "):
            symbol_list.append(symbol.lower())
    word_list = ("".join(symbol_list)).split()

    word_list_len = len(word_list)

    #build dataset structure
    #append upcoming word to the previous one (word_list[index+1])
    for index, word in enumerate(word_list):
        if word in dataset.keys():
            if (index+1) < word_list_len:
                if word_list[index+1] not in dataset[word]:
                    dataset[word].append(word_list[index+1])
        else:
            if (index+1) < word_list_len:
                dataset[word] = [word_list[index+1]]

json_call(path="dataset.json", call_type="w", data=dataset) #dump json dataset file
