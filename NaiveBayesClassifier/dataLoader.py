import re
from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import random


#RUN ONCE
#import nltk
#nltk.download("punkt")
#nltk.download('stopwords')

class DataLoader():
    def __init__(self, file_path : str):
        with open(file_path,"rt") as f:
            raw_input = f.read().lower()

            
        self.labels = []
        self.data = []
        pS = PorterStemmer()

        stopWords = set(stopwords.words('english'))

        lines = re.sub(r'[^\w\s]','',raw_input)
        lineList = lines.splitlines()
        
        for entry in lineList:
            #print(entry)
            if (not entry.startswith("ham")) and (not entry.startswith("spam")):
                continue
            
            entrySplit = entry.split("\t")
            self.labels.append(entrySplit[0])
            tokenList = word_tokenize(entrySplit[-1], language = "english", preserve_line = False)
            self.data.append([pS.stem(word) for word in tokenList if word not in stopWords])

    def load_data(self):
        self.labels = [0 if label == "ham" else 1 for label in self.labels]
        
    def split_data(self):
        tempidx = list(range(len(self.labels)))
        random.shuffle(tempidx)
        tempLabels = []
        tempData = []
        for idx in tempidx:
            tempLabels.append(self.labels[idx])
            tempData.append(self.data[idx])

        self.labels = tempLabels
        self.data = tempData


if __name__  == "__main__":
    dL = DataLoader("SMSSpamCollection.txt")
    print(f"{dL.labels[-1]} : {dL.data[-1]}")
    dL.load_data()
    print(f"{dL.labels[-1]} : {dL.data[-1]}")
    dL.split_data()
    print(f"{dL.labels[-1]} : {dL.data[-1]}")


