import sys
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

import scipy.stats as stats

pd.options.display.float_format = '{:.10f}'.format

columns = ["cat","item_id","timetamp" , "target_value","pre_prediction","post_prediction","pre","post"]

if len(sys.argv)>1:
    file=sys.argv[1]
else:
    file='s3://dissert-430103706720-datalake/wilcoxon/rq1.csv'

df1 = pd.read_csv(sys.argv[1],
    names = columns,
    low_memory=True,
    header=1
    )

for c in df1.cat.unique():

    df = df1[df1['cat']==c]

    print(c, df.shape)

    print('mean',df['pre'].mean())
    print('mean',df['post'].mean())

    stat, p = wilcoxon(df['pre'], df['post'])
    print(c, 'Wilcoxon Statistics=%.5f, p=%.5f' % (stat, p))
