# Generate Predictions after server build


1. Harvest data and generate forecasts for any number of discrete data or model types. In the harvest.py script, there are two arguments.  First, is the filename to be created as part of the data extraction.  Second is the SQL where clause appropriate to unload the data.  Unloads can occur on category, item, KMeans classes, SBC class or any combination thereof.  A full list of data fields which are eligible for selection follows as a list of bullet points.

```
source activate pytorch
python3 harvest.py test1.csv "item_id like '18.%3828100213'"
python3 harvest.py test2.csv "item_id like '18.%3828100313'"
```

- category
- item_id
- timestamp
- target_value
- qty
- price
- sale_code_m
- sale_code_g
- sale_code_b
- sale_code_x
- sale_code_n
- sale_code_c
- sale_code_l
- sale_code_s 
- record_exist
- out_of_stock
- holiday
- thanksgiving_lead1
- thanksgiving_lag1
- christmas_lead1
- christmas_lag1
- sbc_class
- class16
- class64


2. Train and generate forecast. This script is responsible for cursoring though a list of one or more harvested files at `$HOME/data`, one at a time, and producing a future forecast at `$HOME/predictions`. The command line arguments for train.py include: (1) the model architecture to be used, (2) if the data is to be prepared as univariate or multivariate (covariates), and (3) the name of the S3 folder that will recieve the prediction data post training. A list of valid model arguments follows as a bullet point list.
```
./train.sh 
./train.sh AutoARIMA uv experimentname
```
- AutoARIMA
- SimpleFeedForward
- DeepAR
- TemporalFusionTransformer
- Theta
- DynamicOptimizedTheta
- AutoETS
- AutoGluonTabular

3. Place data lake view on CSV data. Using the `experimentname` variable in the prior step, place an Athena table on top of the CSV data published. The idea is to accumulate as many experiments as desired, using different combinations of models and data.  For models that support global/cross-learning, they are able to learn across all time-series presented in the set.

```
CREATE EXTERNAL TABLE experimentname (
  `cat` string, 
  `item_id` string, 
  `timestamp` string, 
  `mean` float)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ',' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://dissert-430103706720-datalake/experimentname/'
```
