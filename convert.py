import pandas as pd

df = pd.read_csv("input.csv", index_col=None)

for index, person in df.iterrows():
    first = person["name"].strip().split(" ")[0]
    last = person["name"].strip().split(" ")[-1]
    df.loc[index, 'first'] = first
    print(df.loc[index, 'first'])
    df.loc[index, 'last'] = last
    print(df.loc[index, 'last'])


df.to_csv("output.csv", index=False)