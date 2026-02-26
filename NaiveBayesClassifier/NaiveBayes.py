from dataLoader import DataLoader
import math

alpha = 1

class NaiveBayes():
    def __init__(self,file_path : str):
        dL = DataLoader(file_path)
        dL.load_data()
        dL.split_data()

        self.trainLabels = dL.trainLabels
        self.trainData = dL.trainData

        #print(f"{self.trainLabels[-1]} : {self.trainData[-1]}")

        self.hamPrior = 0
        self.spamPrior = 0

        self.hamDict = {}
        self.spamDict = {}
        self.hamWordList = set()
        self.spamWordList = set()


        self.totalUniqueWords = 0
        self.totalHamWords = 0
        self.totalSpamWords = 0

    def train(self,):
        hamCount = 0
        spamCount = 0
        

        for lidx in range(len(self.trainLabels)):
            words = self.trainData[lidx]

            if self.trainLabels[lidx] == 0:
                hamCount += 1
                self.totalHamWords += len(words)
                for word in words :
                    if word not in self.hamWordList:
                        self.hamWordList.add(word)
                        self.hamDict[word] = 1
                    else:
                        self.hamDict[word] += 1



            else:
                spamCount += 1
                self.totalSpamWords += len(words)
                for word in words :
                    if word not in self.spamWordList:
                        self.spamWordList.add(word)
                        self.spamDict[word] = 1
                    else:
                        self.spamDict[word] += 1


        self.hamPrior = hamCount / (hamCount + spamCount)
        self.spamPrior = spamCount / (hamCount + spamCount)

        self.totalUniqueWords = len(self.hamWordList) + len(self.spamWordList)
        for i,j in zip(self.hamDict.keys(), self.spamDict.keys()):
            self.hamDict[i] = math.log10((self.hamDict[i] + alpha)/(self.totalHamWords + alpha*self.totalUniqueWords))
            self.spamDict[j] = math.log10((self.spamDict[j] + alpha)/(self.totalSpamWords + alpha*self.totalUniqueWords))


    def prediction(self,words : list):
        
        hamProb = 0
        spamProb = 0
        for idx in range(len(words)):
            word = words[idx]
            if word in self.hamWordList:
                hamProb += self.hamDict[word]
            else:
                hamProb += math.log10(alpha/(self.totalHamWords + alpha*self.totalUniqueWords))

            if word in self.spamWordList:
                spamProb += self.spamDict[word]
            else:
                spamProb += math.log10(alpha/(self.totalSpamWords + alpha*self.totalUniqueWords))


        print(f"{words} : hamProb - {hamProb} \nspamProb - {spamProb}")


        inference = 0 if hamProb > spamProb else 1

        return inference



if __name__ == "__main__":
    nB = NaiveBayes("SMSSpamCollection.txt")
    nB.train()

    #print(nB.prediction(["rofl","its","going","to","fun"]))
    #print(nB.prediction(["text","100","to","confirm"]))

    print(f"spams : {nB.spamWordList}")
    print(f"hams : {nB.hamWordList}")





        




            
