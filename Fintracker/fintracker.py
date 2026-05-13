import pandas as pd
from abc import ABC,abstractmethod
import yaml


class BluePrint(ABC):
    @abstractmethod
    def clean_csv(self):
        pass

    @abstractmethod
    def categorize(self):
        pass


class Financial_Tracker(BluePrint):
    def __init__(self,path : str, categoryPath : str):
        self.path = path
        self.df = None

        with open("categories.yaml") as stream:
            try:
                self.categories = yaml.safe_load(stream)
                self.transactions = dict.fromkeys(self.categories)
            except yaml.YAMLError as exc:
                print(exc)


    def clean_csv(self):
        print("Not implemented in base class")
        pass
    
    def categorize(self):
        idxs = []
        for key in self.categories.keys():
            total = 0
            for value in self.categories[key]:
                idx = self.df["Description"].index[self.df["Description"].str.contains(value)]
                idxs.extend(idx)
                if len(idx) == 0:
                    continue
                total += self.df["Amount"].iloc[idx].sum()                
                
            self.transactions[key] = total

        misc = self.df["Amount"].sum()
        tmp = self.df["Amount"].drop(idxs)
        self.transactions["misc"] = tmp.sum()

        #print(tmp)
        #print(self.df)

        return self.transactions






class BOA(Financial_Tracker):
    def __init__(self,path : str,categoryPath : str):
        super().__init__(path,categoryPath)
        self.df = pd.read_csv(self.path)[["Posted Date", "Payee", "Amount"]].rename(columns={"Posted Date": "Date", "Payee": "Description"})


    def clean_csv(self):
        self.df["Amount"] = -self.df["Amount"]
        self.df["Description"] = self.df["Description"].str.lower()
        pass
        

class Discover(Financial_Tracker):
    def __init__(self,path : str,categoryPath : str):
        super().__init__(path,categoryPath)
        self.df = pd.read_csv(self.path)[["Post Date","Description","Amount"]].rename(columns={"Post Date": "Date"})


        
    def clean_csv(self):
        self.df["Description"] = self.df["Description"].str.lower()
        pass
        



if __name__ == "__main__":
    boa = BOA("boa_statement.csv","categories.yaml")
    boa.clean_csv()
    disc = Discover("discover_statement.csv","categories.yaml")
    disc.clean_csv()

    print(disc.categorize())
    print(boa.categorize())

    #print(boa.df)
    #print(disc.df)
