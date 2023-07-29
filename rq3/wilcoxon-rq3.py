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
    file='s3://dissert-430103706720-datalake/wilcoxon/rq3-ensemble.csv'

df = pd.read_csv(file,
    names = columns,
    low_memory=True,
    header=1
    )

df = df.astype({'target_value':'float',
                'pre_prediction':'float',
                'post_prediction':'float',
                'pre':'float',
                'post':'float'})

print('Method A=', df['pre'].mean())
print('Method B=', df['post'].mean())

stat, p = wilcoxon(df['pre'], df['post'])
print('Wilcoxon Statistics=%.5f, p=%.5f' % (stat, p))
