# usage
# arg1 = input CSV
# arg2 = output CSV
# arg3 = model variation
# arg4 = determines univariate or multivariate data prep
# python train.py $HOME/data/test.csv $HOME/predictions/test.csv AutoARIMA uv
#

import numpy as np
import sys
import pandas as pd
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
import autogluon.core as ag

print ("starting +++++++++++++++++++++++++++++++++++++++++++++++++++")
print (sys.argv[1])
print ("+++++++++++++++++++++++++++++++++++++++++++++++++++")


verbose_level=4

columns = ["category","item_id","timestamp","target_value","qty","price","sale_code_m","sale_code_g","sale_code_b","sale_code_x","sale_code_n","sale_code_c","sale_code_l","sale_code_s","record_exist","out_of_stock","holiday","thanksgiving_lead1","thanksgiving_lag1","christmas_lead1","christmas_lag1"]

df = pd.read_csv(sys.argv[1],
    names = columns,
#    low_memory=True,
#    parse_dates=["timestamp"],
    dtype=str,
    header=0
    )

prediction_length = 8

if sys.argv[4] == 'uv':
    df=df[["category","item_id","timestamp","target_value"]]
    columns = ["item_id","timestamp","target_value"]

    df["item_id"] = df['category'].astype(str) +":"+ df["item_id"]
    df.drop(columns=["category"], inplace=True)

else:

    known_covariate_names=["ppe","qty","sale_code_m","sale_code_g","sale_code_b","sale_code_x","sale_code_n","sale_code_c","sale_code_l","sale_code_s","record_exist","out_of_stock","holiday","thanksgiving_lead1","thanksgiving_lag1","christmas_lead1","christmas_lag1"]

    df['ppe'] = round(df['price'].apply(pd.to_numeric)/df['qty'].apply(pd.to_numeric),2)
    df['ppe'] = df['ppe'].fillna(0)

    df["item_id"] = df['category'].astype(str) +":"+ df["item_id"]

    static_features = df[["item_id"]]
    df.drop(columns=["category","price"], inplace=True)

    df[known_covariate_names] = df[known_covariate_names].apply(pd.to_numeric)

    static_features = static_features.drop_duplicates()
    static_features[["cat", "upc"]] = static_features.item_id.str.split(":", expand=True)
    static_features[["store", "upc"]] = static_features.upc.str.split(".", expand=True)
    static_features["store"] = static_features["store"].astype("category")
    static_features["upc"] = static_features["upc"].astype("category")
    static_features["mfr"] = static_features.upc.str[:5].astype("category")

    static_features.set_index("item_id", inplace=True)

    print('Static features')
    print(static_features.head(2))


if sys.argv[3]=="SimpleFeedForward":
    hyperparameter_settings={"SimpleFeedForward":{ "context_length": prediction_length*6, "hidden_dimensions": [100,100], "epochs":150}}
    print("Running SimpleFeedForward", hyperparameter_settings)

elif sys.argv[3]=="DeepAR":
    hyperparameter_settings={
           "DeepAR": {'context_length': 16, 'epochs': 100, 'hidden_size': 128, 'num_layers': 3, 'dropout_rate': 0.05}
           }

elif sys.argv[3]=="TemporalFusionTransformer":
    hyperparameter_settings={
           "TemporalFusionTransformer": { 
                "epochs": 200,
                "dropout_rate": 0.5
                                         }
           }

elif sys.argv[3]=="AutoARIMA":
    hyperparameter_settings={
           "AutoARIMA":{ "n_jobs": 1}
           }

elif sys.argv[3]=="Theta":
    hyperparameter_settings={
           "Theta": {"n_jobs": 1}
           }

elif sys.argv[3]=="DynamicOptimizedTheta":
    hyperparameter_settings={
           "DynamicOptimizedTheta": {"n_jobs": 1}
           }

elif sys.argv[3]=="AutoETS":
    hyperparameter_settings={
           "AutoETS": {"n_jobs": 1}
           }

elif sys.argv[3]=="AutoGluonTabular":
    hyperparameter_settings={ "AutoGluonTabular":{}
                }

else:
    print("No valid model setting, exiting")
    quit()

print("===================================================")
print(sys.argv[3], hyperparameter_settings)
print("===================================================")


df = TimeSeriesDataFrame.from_data_frame(
    df,
    id_column="item_id",
    timestamp_column="timestamp"
    )

train_data = df.slice_by_timestep(None, -prediction_length)


if sys.argv[4] =='uv':
    
    print ('univariate model')
    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        verbosity=verbose_level,
        target="target_value",
        eval_metric="RMSE",
        freq="W-THU",
        quantile_levels=[0.5])

else:
    train_data.static_features = static_features
    known_covariates = df.slice_by_timestep(-prediction_length, None)[known_covariate_names]

    print ('multivariate model')
    predictor = TimeSeriesPredictor(
        prediction_length=prediction_length,
        known_covariates_names=known_covariate_names,
        verbosity=verbose_level,
        target="target_value",
        eval_metric="RMSE",
        freq="W-THU",
        quantile_levels=[0.5])

    print(known_covariates.head(2))


print(train_data.head(2))
print(train_data.columns)

print ('predictor.fit')

predictor.fit(
    train_data,
    hyperparameter_tune_kwargs=None,
    enable_ensemble = False,
    verbosity=verbose_level,
    random_seed=0,
    hyperparameters=hyperparameter_settings
)

predictor.save()


if sys.argv[4] == 'uv':

    predictions = predictor.predict(train_data,
        quantile_levels=[0.5],
        random_seed=0,
        verbosity=verbose_level)
else:

    predictions = predictor.predict(train_data,
        known_covariates=known_covariates,
        quantile_levels=[0.5],
        random_seed=0,
        verbosity=verbose_level)

predictions.drop(columns=["0.5"], inplace=True)
predictions["mean"] = round(predictions["mean"],2)
predictions.to_csv(sys.argv[2])
