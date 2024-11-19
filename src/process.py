import pandas as pd
try:
    box = pd.read_csv("data/box1_old.csv", index_col=0)
except FileNotFoundError:
    raise FileNotFoundError("rename box1.csv to box1_old.csv")
# rename the header to "x", "y", "z"
box.columns = ["x", "y", "z"]
box.drop_duplicates(keep='first', inplace=True, ignore_index=True)
print(box.head())
box.to_csv("data/box1.csv", index=False)

box.sample(frac=1).reset_index(drop=True).to_csv("data/box1_random.csv", index=False)