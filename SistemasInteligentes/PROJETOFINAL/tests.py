from ReadDataSet import *
# READ AND CLEAR DATASET
BruteData = read_csv_file('train.csv')  
data = clearDataset(BruteData)
for prices in data['Radio_AM_FM']:
    if prices not in ['am','fm','am/fm']:
        print(prices)