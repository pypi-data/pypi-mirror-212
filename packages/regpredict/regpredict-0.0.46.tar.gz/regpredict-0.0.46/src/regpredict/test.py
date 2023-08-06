import pandas as pd
from regbot import signal

df = pd.read_csv('../reinforce/regbot_v46_training.csv')

y_pred = []
def getSignal(t,u,v,w,x,y,z):
    return signal(t,u,v,w,x,y,z)

print(df.head())
df = df.sample(frac=1).reset_index(drop=True)
print(df.head())
df = df[df['targets'] == -1].tail(20)
print(df.head())

df['result'] = df.apply(lambda row: getSignal(row['a'], row['b'], row['macd'], row['rsi-05'], row['rsi-15'],row['close-gradient'],row['close-gradient-neg']), axis=1)

print(df.head())

print(len(df[df['result'] == df['targets']]), len(df))
