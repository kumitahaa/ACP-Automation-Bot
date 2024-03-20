import pandas as pd

person = pd.read_excel("person.xlsx", index_col=None)

print(person.head())

person.to_csv("person.csv")