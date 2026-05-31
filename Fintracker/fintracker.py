import pandas as pd
from abc import ABC,abstractmethod
import yaml
import re
from datetime import datetime

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
        self.groupedLeftover = {}
        self.groupedTrans = {}

        with open(categoryPath) as stream:
            try:
                self.categories = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


    def clean_csv(self):
        self.df["Description"] = self.df["Description"].str.lower()
        for i in self.remset:
            self.df["Description"] = self.df["Description"].str.replace(i,'')

        self.df["Description"] = self.df["Description"].str.replace(r'[^A-Za-z\s]','',regex=True).str.strip()
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%m/%d/%Y')
        self.df = self.df.sort_values(by="Date") 
  
        return
    
    def categorize(self):
        grouped = self.df.groupby(self.df['Date'].dt.to_period('M'))
        for period, group in grouped:
            month_name = str(period)
            transactions = dict.fromkeys(self.categories)
            idxs = []
            for key in self.categories.keys():
                total = 0
                for value in self.categories[key]:
                    idx = grouped["Description"].index[grouped["Description"].str.contains(value)]
                    idxs.extend(idx)
                    if len(idx) == 0:
                        continue
                    total += grouped["Amount"].iloc[idx].sum()
                    
                transactions[key] = total

            self.GroupedTrans[month_name] = transactions
            self.GroupedLeftover[month_name] = self.df.drop(idxs)
            
        return       
        





class BOA(Financial_Tracker):
    def __init__(self,path : str,categoryPath : str):
        super().__init__(path,categoryPath)

    def clean_csv(self):
        self.df = self.df[["Posted Date", "Payee", "Amount"]].rename(columns={"Posted Date": "Date", "Payee": "Description"})
        self.df["Amount"] = -self.df["Amount"]
        super().clean_csv()

        with open("dateFileBOA.txt") as f:
            x = f.read()
            if x != "":
                xs = x.split("-")
                tmpEarly,tmpLate = xs
                tmpEarly = datetime.strptime(tmpEarly,"%m/%d/%Y")
                tmpLate = datetime.strptime(tmpLate,"%m/%d/%Y")
                self.df = self.df.loc[(self.df["Date"] < tmpEarly) | (self.df["Date"] > tmpLate) ]

        if len(self.df) == 0:
            return

        early = self.df["Date"].iloc[0]
        late = self.df["Date"].iloc[-1]
        with open("dateFileBOA.txt", "w") as f:
            f.write(f"{early.strftime('%m/%d/%Y')}-{late.strftime('%m/%d/%Y')}")

        return
        

class Discover(Financial_Tracker):
    def __init__(self,path : str,categoryPath : str):
        super().__init__(path,categoryPath)
        
    def clean_csv(self):
        self.df = self.df[["Post Date","Description","Amount"]].rename(columns={"Post Date": "Date"})
        super().clean_csv()

        with open("dateFileDisc.txt") as f:
            x = f.read()
            if x != "":
                xs = x.split("-")
                tmpEarly,tmpLate = xs
                tmpEarly = datetime.strptime(tmpEarly,"%m/%d/%Y")
                tmpLate = datetime.strptime(tmpLate,"%m/%d/%Y")
                self.df = self.df.loc[(self.df["Date"] < tmpEarly) | (self.df["Date"] > tmpLate) ]

        if len(self.df) == 0:
            return

        early = self.df["Date"].iloc[0]
        late = self.df["Date"].iloc[-1]
        with open("dateFileDisc.txt", "w") as f:
            f.write(f"{early.strftime('%m/%d/%Y')}-{late.strftime('%m/%d/%Y')}")

        return    


class manageTransactions():
    def __init__(self,GroupedTrans : dict, GroupedLeftover : dict, categoryPath : str):
        self.GroupedTrans = GroupedTrans
        self.GroupedLeftover = GroupedLeftover
        self.categoryPath = categoryPath

        with open(categoryPath) as stream:
            try:
                self.categories = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)


    def __add__(self,other):
        GretT = {}
        selfM = set(self.GroupedTrans.keys()) 
        otherM = set(other.GroupedTrans.keys())
        totalM = selfM | otherM

        for month in totalM:
            retT = {}
            if month in (selfM & otherM):
                st = self.GroupedTrans[month]
                ot = other.GroupedTrans[month]
                for key in st.keys():
                    retT[key] = st[key] + ot[key]

                GretL[month] = pd.concat([self.GroupedLeftover[month],other.GroupedLeftover[month]])

            elif month in (selfM - otherM):
                for key in st.keys():
                    retT[key] = st[key] 

                GretL[month] = self.GroupedLeftover[month]
            else:
                for key in ot.keys():
                    retT[key] = ot[key] 

                GretL[month] = other.GroupedLeftover[month]


        return manageTransactions(GretT, GretL, self.categoryPath)

   
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

    disc = Discover("discover_statement.csv","categories.yaml")
    disc.clean_csv()

    boa = BOA("boa_statement.csv","categories.yaml")
    boa.clean_csv()

    discL = len(disc.df) != 0
    boaL = len(boa.df) != 0

    if discL:
        disc.categorize()
        managedisc = manageTransactions(disc.transactions,disc.leftover,"categories.yaml")
        
    if boaL:
        boa.categorize()
        manageboa = manageTransactions(boa.transactions,boa.leftover,"categories.yaml")


    if discL and boaL:
        manageT = manageboa + managedisc
    elif discL and not boaL:
        manageT = managedisc
    elif boaL and not discL:
        manageT = manageboa


    if discL or boaL:
        manageT.tally()
        
        print("BOA")
        print(boa.transactions)
        print(boa.leftover)
     
        print("DISC")
        print(disc.transactions)
        print(disc.leftover)
        print("Total")
        print(manageT.transactions)
