import pandas as pd

df = pd.read_excel("input.xlsx", index_col=None)


df.to_csv("output.csv", index=False)