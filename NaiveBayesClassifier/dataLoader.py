import re
from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

class DataLoader():
    def __init__(self, file_path : str):
        with open(file_path,"rt") as f:
            raw_input = f.read().lower()
            lines = re.sub(pattern = r'[^\w\s]', repl = "", string = raw_input)
            lines = raw_input.splitlines()
            
        self.labels = []
        self.data = []

        
        
        for entry in lines:
            #print(entry)
            if (not entry.startswith("ham")) and (not entry.startswith("spam")):
                continue
            
            entrySplit = entry.split("\t")
            self.labels.append(entrySplit[0])
            self.data.append(entrySplit[-1])




if __name__  == "__main__":
    dL = DataLoader("SMSSpamCollection.txt")
    print(dL.data[-2])
    print(dL.labels[-2])

