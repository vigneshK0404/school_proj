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

        
        self.trainRatio = 0.8
        self.testRatio = 0.2
        self.labels = []
        self.data = []

        self.trainLabels = []
        self.trainData = []
        self.testLabels = []
        self.testData = []

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

        trainidx = int(self.trainRatio*len(tempidx))
        testidx = int(self.testRatio*len(tempidx))
        
        tempTrain = tempidx[:trainidx]
        tempTest = tempidx[trainidx:]

        trainLabels = []
        trainData = []

        testData = []
        testLabels = []
        
        for idx in tempTrain:
            trainLabels.append(self.labels[idx])
            trainData.append(self.data[idx])

        for idx in tempTest:
            testLabels.append(self.labels[idx])
            testData.append(self.data[idx])


        self.trainLabels = trainLabels
        self.trainData = trainData
        self.testLabels = testLabels
        self.testData = testData


if __name__  == "__main__":
    dL = DataLoader("SMSSpamCollection.txt")
    dL.load_data()
    dL.split_data() 

    countHam = 0
    countSpam = 0

    for i in dL.labels :
        if i == 0:
            countHam += 1
        elif i == 1:
            countSpam += 1

        else :
            print("Error!")
        
    print(countHam)
    print(countSpam)


