import sys
import pandas as pd
import numpy as np
from scipy.stats import wilcoxon

import scipy.stats as stats

pd.options.display.float_format = '{:.10f}'.format

columns = ["cat","item_id","timetamp" , "target_value","pre_prediction","post_prediction","pre","post"]

df = pd.read_csv(sys.argv[1],
    names = columns,
    low_memory=True,
    header=1,
    dtype=str
    )

df = df.astype({'target_value':'float',
                'pre_prediction':'float',
                'post_prediction':'float',
                'pre':'float',
                'post':'float'})


print('avg-pre=', df['pre'].mean())
print('avg-post=', df['post'].mean())


stat, p = wilcoxon(df['pre'], df['post'])
print('Wilcoxon Statistics=%.5f, p=%.5f' % (stat, p))
