import pandas as pd

person = pd.read_excel("person_1.xlsx", index_col=None)

print(person.head())

person.to_csv("person.csv")