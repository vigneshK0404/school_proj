from dataLoader import DataLoader

class NaiveBayes():
    def __init__(self,file_path : str):
        dL = DataLoader(file_path)
        dL.load_data()
        dL.split_data()

        self.trainLabels = dL.trainLabels
        self.trainData = dL.trainData

        self.hamPrior = 0
        self.spamPrior = 0

        self.hamDict = {}
        self.spamDict = {}

    def train():
        hamCount = 0
        spamCount = 0
        hamWordList = set()
        spamWordList = set()

        for lidx in range(self.trainLabels):
            if self.trainLabels[lidx] == 0:
                hamCount += 1
                for words in self.trainData[lidx] :
                    for word in words :
                        if word not in hamWordList:
                            hamWordList.add(word)
                            self.hamDict[word] = 1
                        else:
                            self.hamDict[word] += 1



            else:
                spamCount += 1
                for words in self.trainData[lidx] :
                    for word in words :
                        if word not in hamWordList:
                            hamWordList.add(word)
                            self.hamDict[word] = 1
                        else:
                            self.hamDict[word] += 1

        self.hamPrior = hamCount / (hamCount + spamCount)
        self.spamPrior = spamCount / (hamCount + spamCount)



