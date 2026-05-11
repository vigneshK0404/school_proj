import pandas as pd
from abc import ABC,abstractmethod


class BluePrint(ABC):
    @abstractmethod
    def clean_csv(self):
        pass


class Financial_Tracker(BluePrint):
    def __init__(self,path : str):
        self.path = path
        self.df = None

    def clean_csv(self):
        print("Not implemented in base class")
        pass


class BOA(Financial_Tracker):
    def __init__(self,path : str):
        super().__init__(path)
        self.df = pd.read_csv(self.path)[["Posted Date", "Payee", "Amount"]].rename(columns={"Posted Date": "Date", "Payee": "Description"})


    def clean_csv(self):
        self.df["Amount"] = -self.df["Amount"]
        pass
        

class Discover(Financial_Tracker):
    def __init__(self,path : str):
        super().__init__(path)
        self.df = pd.read_csv(self.path)[["Post Date","Description","Amount"]].rename(columns={"Post Date": "Date"})


        
    def clean_csv(self):
        pass
        



if __name__ == "__main__":
    boa = BOA("boa_statement.csv")
    boa.clean_csv()
    disc = Discover("discover_statement.csv")

    print(boa.df)
    print(disc.df)
