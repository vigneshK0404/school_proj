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
        self.remset = {"cincinnati","oh","chicago","il","ny"}
        self.leftover = None

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
                #print(key)
                #print(f"{self.df["Description"].iloc[idx].to_string()}")

                
            self.transactions[key] = total

        misc = self.df["Amount"].sum()
        self.leftover = self.df.drop(idxs)
        
        #print(tmp)
        #print(self.df)

        return       
        





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

        print("\nEnter existing or new Category followed by | and a handle, if handle is empty file will record full name\n")

        repeats = set()

        for i in range(dfLen):
            desc = self.leftover["Description"].iloc[i]
            found_flag = False

            #print(f"repeats : {repeats}")
            for j in repeats:
                if j in desc:
                    found_flag = True
                    break

            if not found_flag:
                categoryInput = input(f"Category for {desc} : ")

                x = categoryInput.split("|")
                if len(x) == 2:
                    category,desc = x
                else:
                    category = categoryInput

                category = category.strip()
                desc = desc.strip()
                repeats.add(desc)

                if category in self.categories.keys():
                    self.categories[category].append(desc)
                else:
                    self.categories[category] = [desc]

                if category in self.transactions.keys():
                    self.transactions[category] += self.leftover["Amount"].iloc[i]
                else:
                    self.transactions[category] = self.leftover["Amount"].iloc[i]


        with open(self.categoryPath, 'w') as file:
            yaml.dump(self.categories, file, default_flow_style=False)


    def displayTrans(self):
        pass



if __name__ == "__main__":
    #disc = Discover("discover_statement.csv","categories.yaml")
    #disc.clean_csv()
    #disc.categorize()
    #print(disc.transactions)

    boa = BOA("boa_statement.csv","categories.yaml")
    boa.clean_csv()
    boa.categorize()
    print(boa.transactions)
    manage = manageTransactions(boa.transactions,boa.leftover,"categories.yaml")
    manage.tally()


    #print(boa.df)
