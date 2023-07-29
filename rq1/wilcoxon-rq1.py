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

df = pd.read_csv(sys.argv[1],
    names = columns,
    low_memory=True,
    header=1
    )
print('Shape ',df.shape)

pre_greater = df[df['pre']>df['post']].count()[0]
post_greater = df[df['pre']<df['post']].count()[0]
count_equal = df[df['pre']==df['post']].count()[0]
count_zero = df[ (df['pre']==0) & (df['post']==0)].count()[0]

print('pre-greater = ',pre_greater)
print('post-greater = ',post_greater)
print('equal = ',count_equal)
print('zero = ',count_zero)

print('avg-pre=', df['pre'].mean())
print('avg-post=', df['post'].mean())

stat, p = wilcoxon(df['pre'], df['post'])
print('Wilcoxon Statistics=%.3f, p=%.10f' % (stat, p))

# interpret
alpha = 0.05
if p > alpha:
 print('Same distribution (fail to reject H0)')
else:
 print('Different distribution (reject H0)')
  
