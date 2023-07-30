# Overall process flow

First, a server needs to be built for data processing. The data is large; more than 100M records which require more memory than a typical laptop. For this research, cloud computing was used.  These are the principal steps used in the multi-month research.

## Build cloud server(s)
To build a server, this [script](build-server.md) offers a model. During the course of this study, many servers were used concurrently to process different input datasets against a matrix of time-series models.  At times, data could be large when training an entire category.  At other times, the data is smaller when training only a specific slice of kmeans segmented data.  Clusters should be carefully provisioned to have enough memory for the task.

## Download data from source

As a one-time event, data must be downloaded from The University of Chicago's Booth School servers for your use. A script has been provided to make this easy, located [here](download-source.md).

>CAUTION: There is an error with the original data format. File wtti.csv has price and quantity columns transposed. File wana.csv has store and upc transposed.  These are addressed in the next section with data preparation.  If you do not follow this method, be aware of exceptions, so you can address them.

```
test$ head -2 wana.csv
STORE,UPC,WEEK,MOVE,QTY,PRICE,SALE,PROFIT,OK,PRICE_HEX,PROFIT_HEX
76,1192603016,306,0,1,0,,0,1,0000000000000000,0000000000000000
test$ head -2 wtti.csv
STORE,UPC,WEEK,MOVE,PRICE,QTY,SALE,PROFIT,OK,PRICE_HEX,PROFIT_HEX
2,1122542346,336,0,0,1,,0,1,0000000000000000,0000000000000000
test$ head -2 wcer.csv
STORE,UPC,WEEK,MOVE,QTY,PRICE,SALE,PROFIT,OK,PRICE_HEX,PROFIT_HEX
51,317,372,1,1,26.02,,62.52,1,403A051EB851EB85,404F428F5C28F5C3
test$ head -2 wber.csv
STORE,UPC,WEEK,MOVE,QTY,PRICE,SALE,PROFIT,OK,PRICE_HEX,PROFIT_HEX
2,294,298,11,1,2.62,,-18.83,1,4004F5C28F5C28F6,C032D47AE147AE14
test$
```

## Data Preparation, Cleansing, Time-Series Filling, Parquet Compression

This [script](historic-data-prep.md) provides direction on making a normalized set of training data available for the research.  Ultimately, the CSV data is made available as a cloud data lake, stored in an object store, where it can be queried with SQL in a serverless fashion.

## Generate Predictions

This [script](generate-predictions.md) provides guidance for harvesting correct portions of data, training a model and publishing predictions back to a cloud lake. Steps in this script can be run for as many slices of data and models as desired.

## Analysis and Statisical Testing

This [script](doc-tables.md) provides SQL used to harvest data from the data lake including true history of demand, and predicted demand across multiple forecast experiments. The Wilcoxon Signed-Rank test was used for each of the three research questions.  The following scripts show how the tests were run.  Effectively, in each, a set of matched pairs on time, store, UPC show two models compared to one another.

```
python rq1\wilcoxon-rq1.py
python rq1\wilcoxon-rq1-cat.py
python rq2\wilcoxon-rq1.py
python rq3\wilcoxon-rq3.py
```
