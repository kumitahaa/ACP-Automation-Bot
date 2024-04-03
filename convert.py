import pandas as pd

df = pd.read_csv("input.csv", index_col=None)
for index, person in df.iterrows():
    dob = person["dob"]
    print(dob)
    try:
        df.loc[index, 'dob'] = "/".join([dob.split("-")[1], dob.split("-")[0], dob.split("-")[2]])
    except:
       df.drop(index, inplace=True)     
    print(person["dob"])
    print("=====")

df.to_csv("test_out.csv", index=False)