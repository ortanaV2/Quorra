import time
import argparse
from transformer import json_call

parser = argparse.ArgumentParser(description='Processes the dataset and responses to requests.')
parser.add_argument('--inp', dest='INPUT', type=str, help='Request input')
args = parser.parse_args()
inp = args.INPUT

__name__ = "LanguageProcessor"
class MissingInput(Exception):
    def __init__(self, message="Missing input for further operations. {--inp (str)}"):
        self.message = message
        super().__init__(self.message)
if inp is None: raise MissingInput #Error if missing input (--inp (str))

#upcoming --> tokenize input

    