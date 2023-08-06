import plantpathoppi_ml as ppp
import pandas as pd

df = pd.read_csv("example.csv")
var = df.to_numpy()
x = ppp.predict(var)
print(x)
y = ppp.predict_proba(var)
print(y)
ppp.gen_file(var)