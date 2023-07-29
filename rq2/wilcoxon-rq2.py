import sys
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

import scipy.stats as stats

pd.options.display.float_format = '{:.10f}'.format

columns = ["cluster_member", "cat","item_id","timetamp" , "target_value","pre_prediction","post_prediction","pre","post"]

if len(sys.argv)>1:
    file=sys.argv[1]
else:
    file='s3://dissert-430103706720-datalake/wilcoxon/rq2-deepar-sbc.csv'

df1 = pd.read_csv(file,
    names = columns,
    low_memory=True,
    header=1
    )

print ('Method A ', df1['pre'].mean())
print ('Method B ', df1['post'].mean())

for cl in df1.cluster_member.unique():

    df2 = df1[df1['cluster_member']==cl]

    stat, p = wilcoxon(df2['pre'], df2['post'])
    print(cl, 'Wilcoxon Statistics=%.5f, p=%.5f' % (stat, p))
