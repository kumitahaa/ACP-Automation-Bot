import pandas as pd


df = pd.read_csv("output.csv", )
first_row_zip = df.loc[0, 'zip']
print(first_row_zip)
a = len(str(int(first_row_zip)))
print(a)
print(df.columns)
