from NaiveBayesClassifier import NaiveBayesClassifier
from dataLoader import DataLoader


class EvaluationMetrics():
    def __init__(self,dL : DataLoader):
        
        nB = NaiveBayes(dL)
        nB.train()

        self.testLabels = dL.testLabels
        self.testData = dL.testData


    def compute_metrics():




if __name__ == "__main__":
    dL = DataLoader(file_path)
    dL.load_data()
    dL.split_data()

