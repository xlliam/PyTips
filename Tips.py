import os
import pandas as pd

######   change the path to read the data   ######
os.chdir('Path to read the data')
dataset_1 = pd.read_csv('dataset1.csv')

##### dataset_1 contains two columns: var1, var2, the structure is given by ####
# ..   var1    var2 ..
#..     e1      f1  ..
#..  e2;e3;e4  f2;f3;f4 ..
#..
#### Below pieces of codes try to split the stack element and put them into different rows
FullName = list(dataset_1)
StackName = ['var1', 'var2']
IndexName = list(filter(lambda x: x not in StackName, FullName))

dataset_1new = \
    (
        dataset_1.set_index(IndexName)
        .stack()
        .str.split(';', expand=True)
        .stack()
        .unstack(-2)
        .reset_index(-1)
        .reset_index()
    )

#### Read the txt data with three fields in the dataset
#### the data structure is given by
#    "000234","0.0","0.012232456",....
####################################
# Way 1 --- Read txt file
import csv
f = open('dataset2.txt', "r")
csvReader = csv.reader(f, quotechar='"', delimiter=',',
                       quoting=csv.QUOTE_ALL, skipinitialspace=True)
dataset_2w1 = pd.DataFrame(csvReader)
f.close()
# Way 2 --- Read txt file
dataset_2w2 = pd.read.csv('dataset2.txt', quotechar='"', delimiter=',',
                          skipinitialspace=True, quoting=csv.QUOTE_ALL,
                          names=('A', 'B', 'C'))

#######  Python Read SAS dataset
from sas7bdat import SAS7BDAT
dataset_3 = SAS7BDAT('dataset3.sas7bdat').to_data_frame()
# replace field name "var1" with field name "var2"
dataset_3.columns = dataset_3.columns.str.replace('var1', 'var2')
# replace multiple field names
dataset_3.rename(columns={'var1': 'var2', 'var3': 'var4'}, inplace=True)
# lower case all column names
dataset_3.columns = dataset_3.columns.str.lower()
# change the data type of a column
dataset_3['var3'] = dataset_3['var3'].astype(int)
# replace values in one column
dataset_3.loc[dataset_3['var4'] == 1.0, 'var5'] = 0.0
# each value of a column minus the same value (1000)
dataset_3['var6'] = dataset_3['var6'].substract(1000)