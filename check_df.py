import pandas as pd,random


df = pd.read_csv("input.csv", )
for index, person in df.iterrows():
    try:
        person["ssn"] = str(person["ssn"]).split(".")[0]
        print("Fix ssn")
        person["phone"] = str(person["phone"]).split(".")[0]
        print("Fix phone")
        person["zip"] = str(person["zip"]).split(".")[0]
        print("Fix zip")
    except:
        pass
    print(person["ssn"])
    print(person["phone"])
    print(person["zip"])

df.to_csv("input masmi 2.csv", index=False)
