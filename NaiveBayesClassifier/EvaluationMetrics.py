from NaiveBayes import NaiveBayes
from dataLoader import DataLoader


class EvaluationMetrics():
    def __init__(self, testLabels, testData, nB : NaiveBayes):
       
        self.nB = nB

        self.testLabels = testLabels
        self.testData = testData

                
        #If we consider this to be a spam identifier, then a positive would we it is spam, negative means it is ham. True positive then would be precdiction is spam and it is actually spam, False positive is when pred is pos but truth is neg, true neg is ham and pred is ham, False neg is we predict ham but it is spam.
    def compute_metrics(self):
        TP = 0
        FP = 0
        TN = 0
        FN = 0

        for words, label in zip(self.testData, self.testLabels):
            predLabel = self.nB.prediction(words)
            
            if label == 1 : #truth is spam
                if label and predLabel :
                    TP += 1
                else :
                    FN += 1

            else:
                if not (label and predLabel) :
                    TN += 1
                else :
                    FP += 1

        accuracy = (TP + TN)/(TP + TN + FN + FP)
        precision = TP/(TP + FP)
        recall = TP/(TP + FN)
        F1 = 2 * precision * recall / (precision + recall)

        return TP,FP,TN,FN,accuracy,precision,recall,F1

if __name__ == "__main__":
    dL = DataLoader("SMSSpamCollection.txt")
    dL.load_data()
    dL.split_data()

    nB = NaiveBayes(dL.trainLabels,dL.trainData)
    nB.train()

    eM = EvaluationMetrics(dL.testLabels, dL.testData, nB)
    
    print(eM.compute_metrics())






