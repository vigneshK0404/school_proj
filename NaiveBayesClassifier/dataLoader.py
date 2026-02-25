import re
from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


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





if __name__  == "__main__":
    dL = DataLoader("SMSSpamCollection.txt")
    print(dL.labels[-2])
    print(dL.data[-2])

