import pandas as pd
from abc import ABC,abstractmethod
import yaml
import re


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
        self.df = pd.read_csv(path)
        self.remset = {"cincinnati","oh"}

        with open(categoryPath) as stream:
            try:
                self.categories = yaml.safe_load(stream)
                self.transactions = dict.fromkeys(self.categories)
            except yaml.YAMLError as exc:
                print(exc)


    def clean_csv(self):
        self.df["Description"] = self.df["Description"].str.lower()
        for i in self.remset:
            self.df["Description"] = self.df["Description"].str.replace(i,'')

        self.df["Description"] = self.df["Description"].str.replace(r'[^A-Za-z\s]','',regex=True).str.strip()
        return
    
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
                print(key)
                print(f"{self.df["Description"].iloc[idx].to_string()}")

                
            self.transactions[key] = total

        misc = self.df["Amount"].sum()
        leftover = self.df.drop(idxs)   

        #TODO: pass tmp into add YAML and give user the choice to choose what category, add new category or add to misc if error
        
        #print(tmp)
        #print(self.df)

        return self.transactions, leftover        
        





class BOA(Financial_Tracker):
    def __init__(self,path : str,categoryPath : str):
        super().__init__(path,categoryPath)

    def clean_csv(self):
        self.df = self.df[["Posted Date", "Payee", "Amount"]].rename(columns={"Posted Date": "Date", "Payee": "Description"})
        self.df["Amount"] = -self.df["Amount"]
        super().clean_csv()
        return
        

class Discover(Financial_Tracker):
    def __init__(self,path : str,categoryPath : str):
        super().__init__(path,categoryPath)
        
    def clean_csv(self):
        self.df = self.df[["Post Date","Description","Amount"]].rename(columns={"Post Date": "Date"})
        super().clean_csv()
        return    


class manageTransactions():
    def __init__(self,transactions : dict, leftover : pd.DataFrame, categoryPath : str):
        self.transactions = transactions
        self.leftover = leftover
        self.categoryPath = categoryPath

        with open(categoryPath) as stream:
            try:
                self.categories = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


    def __add__(self,other):
        retT = {}
        for key in self.transactions.keys():
            retT[key] = self.transactions[key] + other.transactions[key]

        retL = pd.concat([self.leftover,other.leftover])

        return retT, retL

   
    def tally(self):
        dfLen = len(self.leftover)
        if dfLen == 0:
            print("Nothing to Tally")
            return

        print("Existing Categories")
        print(self.transactions.keys())

        
        for i in range(dfLen):
            desc = self.leftover["Description"].iloc[i]
            category = input(f"Category for {desc} : ")

            if category in self.categories.keys():
                self.categories[category].append(desc)
            else:
                self.categories[category] = [desc]

            if category in self.transacrions.keys():
                self.transactions[category] += self.leftover["Amount"].iloc[i]
            else:
                self.transactions[category] = self.leftover["Amount"].iloc[i]


        with open(categoryPath, 'w') as file:
            yaml.dump(self.categories, file, default_flow_style=False)


    def displayTrans(self):
        pass



if __name__ == "__main__":
    disc = Discover("discover_statement.csv","categories.yaml")
    disc.clean_csv()
    print(disc.df)
    print(disc.categorize())

    #boa = BOA("boa_statement.csv","categories.yaml")
    #boa.clean_csv()
    #print(boa.categorize())

    #print(boa.df)
