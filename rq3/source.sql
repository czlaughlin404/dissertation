CREATE TABLE t_ensemble_rq3_avg
WITH (
     format = 'TEXTFILE', 
     external_location = 's3://dissert-430103706720-datalake/result/t_ensemble_rq3_avg/',
     field_delimiter = ',',
     write_compression ='NONE'
     )
     as
select t.cat, t.item_id, t.timestamp, 
t.target_value, 
pre.pre_prediction as pre_prediction,
ensemble.post_prediction as post_prediction
from 
(select cat, item_id, timestamp, target_value from t_ensemble_deepar_uv) t JOIN
(
select cat, item_id, timestamp, avg(post_prediction) as post_prediction from (
select cat, item_id, timestamp,post_prediction from t_cluster_tft_sbc union all
select cat, item_id, timestamp,post_prediction from t_cluster_tft_sbc union all
select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc union all
select cat, item_id, timestamp,post_prediction from t_ensemble_deepar union all
select cat, item_id, timestamp,post_prediction from t_ensemble_tft 
union all select cat, item_id, timestamp,post_prediction from t_ensemble_tft 
union all select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc16 where (cluster_member like '%erratic%')
union all select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc16 where (cluster_member like '%smooth%')
union all select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc64 where (cluster_member like '%erratic%')
union all select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc64 where (cluster_member like '%smooth%')
-- select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc16 union all
-- union all select cat, item_id, timestamp, post_prediction from t_cluster_deepar_sbc64 
-- select cat, item_id, timestamp, post_prediction from t_cluster_ff_sbc union all
-- select cat, item_id, timestamp,post_prediction from t_ensemble_arima union all
-- select cat, item_id, timestamp,post_prediction from t_ensemble_deepar_uv union all
-- select cat, item_id, timestamp,post_prediction from t_ensemble_ets union all
-- select cat, item_id, timestamp,post_prediction from t_ensemble_ff union all
-- select cat, item_id, timestamp,post_prediction from t_ensemble_theta
) group by  cat, item_id, timestamp
) ensemble
on (ensemble.item_id=t.item_id and ensemble.cat=t.cat and ensemble.timestamp=t.timestamp)
join (select cat, item_id, timestamp, post_prediction as pre_prediction from t_ensemble_tft) pre 
on (pre.item_id=t.item_id and pre.cat=t.cat and pre.timestamp=t.timestamp)

select cat, abs(target_value-pre_prediction) pre_mae, abs(target_value-post_prediction) post_mae From t_ensemble_rq3_avg
