CREATE TABLE t_deepar_uv_mv_rq1
WITH (
     format = 'TEXTFILE', 
     external_location = 's3://dissert-430103706720-datalake/result/t_deepar_uv_mv_rq1/',
     field_delimiter = ',',
     write_compression ='NONE'
     )
     as
select 
td.category as cat,
td.item_id, 
td.timestamp,
cast(td.target_value as decimal) target_value, 
pre.post_prediction pre_prediction, 
post.post_prediction post_prediction,
abs(cast(td.target_value as decimal)-pre.post_prediction) pre_error, 
abs(cast(td.target_value as decimal)-post.post_prediction) post_error
from
dissert.training_data td
join  dissert.t_ensemble_deepar_uv pre
on (
pre.item_id = td.item_id
and pre.timestamp = td.timestamp
and pre.cat = td.category
)
join  dissert.t_ensemble_deepar post
on (
post.item_id = td.item_id
and post.timestamp = td.timestamp
and pre.cat = td.category)
join 
(select distinct
split_part(item_id,':',1) as cat,
split_part(item_id,':',2) as item_id
from 
dissert.rq3_cluster_sbc_label 
) filter on (filter.cat =  td.category and filter.item_id=td.item_id)


select 
  cat, 
  item_id, 
  timestamp, 
  target_value, 
  pre_prediction, 
  post_prediction, 
  abs(target_value-pre_prediction) pre_error, 
  abs(target_value-post_prediction) post_error
From t_deepar_uv_mv_rq1
