import pandas as pd

s = pd.Series(["Lion", "Monkey", "Rabbit"])
print(s.str.findall("Monkey"))

