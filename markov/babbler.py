import random
import glob
import sys
import traceback

"""
Markov Babbler

After being trained on text from various authors, it will
'babble' (generate random walks) and produce text that
vaguely sounds like the author of the training texts.

run as: python3 babbler.py 
or optioanlly with parameters: python3 babbler.py 2 tests/test1.txt 5 
"""

# ------------------- Implementation Details: -------------------------------
# Our entire graph is a dictionary
#   - keys/states are ngrams represented (could have been tuple, CANNOT be a list,
#       because we need to use states as dictionary keys, and lists are not hashable)
#   - values are either lists or Bags
# Starter states are a list of words (could have been a Bag; either an ordered or unordered collection, with duplicates allowed)
# When we pick a word, we transition to a new state
# e.g. suppose we are using bigrams and are at the state ‘the dog’ and we pick the word ‘runs’. 
# Our new state is ‘dog runs’, so we look up that state in our dictionary, and then get the next word, and so on…
# Ending states can generate a special "stop" symbol; we will use ‘EOL’.
#   If we generate the word ‘EOL’, then the sentence is over. Since all words are lower-case, this won’t be confused for a legitimate word

# --------------------- Tasks --------------------------------
# class Babbler:
    # def __init__(self, n, seed=None)      # already completed with initial data structures
    # def add_file(self, filename)          # already completed; calls add_sentence(), so go there next, read comments, and plan out your steps
    # def add_sentence(self, sentence)      # implement this
    # def get_starters(self)                # implement this
    # def get_stoppers(self)                # implement this
    # def get_successors(self, ngram)       # implement this
    # def get_all_ngrams(self)              # implement this
    # def has_successor(self, ngram)        # implement this
    # def get_random_successor(self, ngram) # implement this
    # def babble(self)                      # implement this

# ------------------- Tips ----------------------------------
# read through all the comments in the below functions before beginning to code
# remember that our states are n-grams, so whatever the n value is, that's how many words per state (including starters and stoppers)
# our successors (the value for each key in our dictionary) are strings representing words (not states, since n-gram states could be of multiple words)
# since we will represent your n-grams as strings, remember to separate words with a space 
# when updating your state, make sure you don't end up with extra spaces or you won't find it in the dictionary
# add print statements while debugging to ensure is step in your process is working as intended

import random

class Babbler:
    
    def __init__(self, n, seed=None):
        self.n = n
        if seed is not None:
            random.seed(seed)
        self.brainGraph = {}
        self.starters = []
        self.stoppers = []

    def add_file(self, filename):
        print("Reading from your file...")
        for line in [line.rstrip().lower() for line in open(filename, errors='ignore').readlines()]:
            self.add_sentence(line)
        print("Done reading from your file.")
        print("\n---------resulting graph: --------")
        print(self.brainGraph)
        print("----------------------------------\n")

    def add_sentence(self, sentence):
        words = sentence.strip().lower().split()
        if len(words) < self.n:
            return

        for i in range(len(words) - self.n + 1):
            ngram = ' '.join(words[i:i + self.n])
            if i == 0:
                self.starters.append(ngram)

            next_index = i + self.n
            if next_index < len(words):
                next_word = words[next_index]
            else:
                next_word = 'EOL'
                self.stoppers.append(ngram)

            if ngram not in self.brainGraph:
                self.brainGraph[ngram] = []

            self.brainGraph[ngram].append(next_word)

    def get_starters(self):
        return self.starters

    def get_stoppers(self):
        return self.stoppers

    def get_successors(self, ngram):
        return self.brainGraph.get(ngram, [])

    def get_all_ngrams(self):
        return list(self.brainGraph.keys())

    def has_successor(self, ngram):
        return ngram in self.brainGraph and len(self.brainGraph[ngram]) > 0

    def get_random_successor(self, ngram):
        successors = self.get_successors(ngram)
        if successors:
            return random.choice(successors)
        return None

    def babble(self):
        if not self.starters:
            return ""

        current_ngram = random.choice(self.starters)
        words = current_ngram.split()

        while True:
            next_word = self.get_random_successor(current_ngram)
            if not next_word or next_word == 'EOL':
                break
            words.append(next_word)
            current_ngram = ' '.join(words[-self.n:])

        return ' '.join(words)

# nothing to change here; read, understand, move along
def main(n=3, filename='tests/test1.txt', num_sentences=5):
    """
    Simple test driver.
    """
    
    print('Currently running on ',filename)
    babbler = Babbler(n)
    babbler.add_file(filename)

    try:
        print(f'num starters {len(babbler.get_starters())}')
        print("\t",babbler.get_starters())
        print(f'num ngrams {len(babbler.get_all_ngrams())}')
        print(f'num stoppers {len(babbler.get_stoppers())}')
        print("\t",babbler.get_stoppers())
        print("------------------------------\nPreparing to drop some bars...\n")
        for _ in range(num_sentences):
            print(babbler.babble())
    except Exception as e:
        print("This code crashed... QQ\n"+
            " - make sure you have implemented all of the above methods\n"+
            " - review the crash report below\n"+
            " - add lots of print statements to your methods to ensure they are working as you intended\n")
        print("--------------------------Crash Report:--------------------------")
        traceback.print_exc() 

# nothing to change here; read, understand, move along
# to execute this script, in a terminal nagivate to your cs317/markov folder, unless already there
# enter the following terminal command: python3 babbler.py
# default values below will be used; alternatively you can provide up to 3 arguments (n, filename, num_sentences), for example: python3 babbler.py 2 tests/test2.txt 10
if __name__ == '__main__': 
    print("Entered arguments: ",sys.argv)
    sys.argv.pop(0) # remove the first parameter, which should be babbler.py, the name of the script
    # -------default values -----------
    n = 3
    filename = 'tests/test1.txt'
    num_sentences = 5
    #----------------------------------
    if len(sys.argv) > 0: # if any argumetns are passed, first is assumed to be n
        n = int(sys.argv.pop(0))
    if len(sys.argv) > 0: # if any more were passed, the next is assumed to be the filename
        filename = sys.argv.pop(0)
    if len(sys.argv) > 0: # if any more were passed, the next is assumed to be number of sentences to be generated 
        num_sentences = int(sys.argv.pop(0))
    main(n, filename, num_sentences) # now we call main with all the actual or default arguments