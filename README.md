1. Raw ZIP files stored: s3://dissert-430103706720-datalake/movement/zip/
2. Unzip movement files stored: s3://dissert-430103706720-datalake/movement/csv/

3.  Place SQL table on top of raw CSV

CREATE EXTERNAL TABLE IF NOT EXISTS dissert.movement(
 upc string,
 STORE string,
 WEEK string,
 MOVE string,
 QTY  string,
 PRICE  string,
 SALE string,
 profit string,
 ok string,
 price_hex string,
 profit_hex string)
 ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
 LOCATION 's3://dissert-430103706720-datalake/movement/csv/'
 TBLPROPERTIES ("skip.header.line.count"="1")


ISSUE IS SOME FILE HAVE UPC/STORE TRANSPOSED

 #  upc store   week    move    qty price   sale    profit  ok  price_hex   profit_hex
1   139 3400000239  345 69  1   0.33    B   3.63    1   3FD51EB851EB851F    400D0A3D70A3D70A
2   139 3400000239  346 67  1   0.33    B   3.73    1   3FD51EB851EB851F    400DD70A3D70A3D7
3   139 3400000239  347 61  1   0.33    B   7.57    1   3FD51EB851EB851F    401E47AE147AE148
4   139 3400000239  348 78  1   0.33    B   8.22    1   3FD51EB851EB851F    402070A3D70A3D71
5   139 3400000239  349 66  1   0.33    B   8.42    1   3FD51EB851EB851F    4020D70A3D70A3D7
6   139 3400000239  350 74  1   0.33    B   7.51    1   3FD51EB851EB851F    401E0A3D70A3D70A
7   139 3400000239  351 49  1   0.33    B   7.11    1   3FD51EB851EB851F    401C70A3D70A3D71
8   139 3400000239  352 45  1   0.36    B   15.24   1   3FD70A3D70A3D70A    402E7AE147AE147B
9   139 3400000239  353 34  1   0.55        42.93   1   3FE199999999999A    4045770A3D70A3D7
10  139 3400000239  354 30  1   0.55        42.54   1   3FE199999999999A    4045451EB851EB85


4. Use Case to transpose, some raw files have UPC and Store number transposed

CREATE TABLE movement_aligned_csv
WITH (
     format = 'TEXTFILE', 
     external_location = 's3://dissert-430103706720-datalake/movement/clean_csv',
     field_delimiter = ',',
     write_compression ='NONE'
     )
     as
 select 
  substring("$Path",49, 4) as category,
  case 
  when length(upc)<=5 then upc
  else store 
  end as store,
  case
  when length(upc)>5 then upc
  else store 
  end as upc,
  week,
  move,
  qty,
  price,
  sale,
  profit,
  ok
   from dissert.movement 


5. Compress as parquet

CREATE TABLE movement_aligned_parquet
WITH (
     format = 'PARQUET',
     external_location = 's3://dissert-430103706720-datalake/movement/clean_parquet/',
     write_compression ='SNAPPY'
     )
     as
     select * from movement_aligned_csv



6. Create a holiday dimension table; manually annotated thanksgiving and christmas lead/lag

CREATE EXTERNAL TABLE IF NOT EXISTS dissert.week(
 week string,
 timestamp string,
 holiday_label string,
 week_id int,
 year_id int,
 month_id int,
 holiday int,
 thanksgiving_lead1 int,
 thanksgiving_lag1 int,
 christmas_lead1 int,
 christmas_lag1 int
)
 ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
 LOCATION 's3://dissert-430103706720-datalake/week/'
 TBLPROPERTIES ("skip.header.line.count"="1")
 

7.  Create a Cartesian table of all products, stores, weeks; this is a key table, no non-key-attributes

CREATE TABLE movement_aligned_key_cartisian
WITH (
     format = 'PARQUET',
     external_location = 's3://dissert-430103706720-datalake/movement/key_cartisian/',
     write_compression ='SNAPPY'
     )
as
select data_key.category, data_key.store, data_key.upc, week_key.week from
(select distinct category, store, upc from dissert.movement_aligned_parquet
where 
cast(week as integer)<=280
and week>='1' and ok ='1') data_key ,
(select week from week where cast(week as integer)<=280) week_key

8.  join the key table with movement_aligned_parquet for a zero filled table.  Note use of coalese for zero filling.

CREATE TABLE movement_aligned_zero_filled
WITH (
     format = 'PARQUET',
     external_location = 's3://dissert-430103706720-datalake/movement/zero_filled/',
     write_compression ='SNAPPY'
     )
as
select 
c.category,
c.store,
c.upc,
c.week,
w.timestamp,
coalesce(d.move,'0') as target_value,
coalesce(d.price,'0') as price,
coalesce(d.qty,'0') as qty,
coalesce(d.sale,'X') as sale_code,
coalesce(d.ok,'0') as record_exist
from
dissert.movement_aligned_key_cartisian c LEFT OUTER JOIN
(select * from dissert.movement_aligned_parquet
where ok = '1') d 
on (
c.week = d.week and
c.store = d.store and
c.upc = d.upc and
c.category = d.category
)
join week w on (w.week = c.week)
where cast(w.week as integer)<=220


9.  Which products had no sales at all, these need to be excluded.

CREATE TABLE exclude_zero_target_value_upc_store
WITH (
     format = 'PARQUET',
     external_location = 's3://dissert-430103706720-datalake/exclude-zero-target/',
     write_compression ='SNAPPY'
     )
as
select category, store, upc 
from movement_aligned_zero_filled
where cast(week as real) <= 208
group by category, store, upc
having sum(cast(target_value as real))=0


10.   Correct data error in two category files 'wptw','wtti', excluding items with no sales from prior step.

create table dissert.movement_aligned_zero_filled_corrected
WITH (
     format = 'PARQUET',
     external_location = 's3://dissert-430103706720-datalake/movement_aligned_zero_filled_corrected/',
     write_compression ='SNAPPY'
     )
as
select category, store, upc, week, timestamp,target_value,
price as qty, qty as price,  --- FLIP FLOP THESE for WPTW and WTTI
case when sale_code='M' then 1 else 0 end sale_code_m,
case when sale_code='G' then 1 else 0 end sale_code_g,
case when sale_code='B' then 1 else 0 end sale_code_b,
case when sale_code='X' then 1 else 0 end sale_code_x,
case when sale_code='N' then 1 else 0 end sale_code_n,
case when sale_code='C' then 1 else 0 end sale_code_c,
case when sale_code='L' then 1 else 0 end sale_code_l,
case when sale_code='S' then 1 else 0 end sale_code_s,
record_exist
from
movement_aligned_zero_filled
where 
cast(week as real)<=208
and (category, store, upc) not in (select category, store, upc from exclude_zero_target_value_upc_store)
and category  in  ('wptw','wtti')
union all
select category, store, upc, week, timestamp,target_value,qty, price, 
case when sale_code='M' then 1 else 0 end sale_code_m,
case when sale_code='G' then 1 else 0 end sale_code_g,
case when sale_code='B' then 1 else 0 end sale_code_b,
case when sale_code='X' then 1 else 0 end sale_code_x,
case when sale_code='N' then 1 else 0 end sale_code_n,
case when sale_code='C' then 1 else 0 end sale_code_c,
case when sale_code='L' then 1 else 0 end sale_code_l,
case when sale_code='S' then 1 else 0 end sale_code_s,
record_exist
from
movement_aligned_zero_filled
where 
cast(week as real)<=208
and (category, store, upc) not in (select category, store, upc from exclude_zero_target_value_upc_store)
and category not in  ('wptw','wtti')



11. Unload for forecaster and cluster assignments


CREATE TABLE rq3_monolith_all_category
WITH (
     format = 'TEXTFILE', 
     external_location = 's3://dissert-430103706720-datalake/movement/rq3_monolith',
     field_delimiter = ',',
     write_compression ='NONE'
     )
     as
select
move.category,
move.item_id,
move.timestamp,
move.target_value,
qty,
price,
sale_code_m,
sale_code_g,
sale_code_b,
sale_code_x,
sale_code_n,
sale_code_c,
sale_code_l,
sale_code_s,
move.record_exist,
case when price='0' and move.target_value ='0' and record_exist='1' then '1' else '0' end as out_of_stock,
cw.holiday,
cw.thanksgiving_lead1,
cw.thanksgiving_lag1,
cw.christmas_lead1,
cw.christmas_lag1
From 
(
select 
category,
store||'.'||upc as item_id,
week,
timestamp,
target_value,
qty,
price,
sale_code_m,
sale_code_g,
sale_code_b,
sale_code_x,
sale_code_n,
sale_code_c,
sale_code_l,
sale_code_s,
record_exist
from movement_aligned_zero_filled_corrected
) move
JOIN week cw
on (move.week = cw.week)
order by category, item_id, timestamp


12.  Import results from Data Wrangler Kmeans cluster label

 CREATE EXTERNAL TABLE IF NOT EXISTS dissert.rq3_cluster_label (
 item_id string,
 class04 string,
 class08 string,
 class16 string,
 class32 string,
 class64 string,
 class128 string,
 class256 string
 )
 ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
 LOCATION 's3://dissert-430103706720-datalake/movement/knn-cluster/ts-kmeans-cluster-yyyymmdd-template-2023-04-23T13-45-15/'
 TBLPROPERTIES ("skip.header.line.count"="1")

select
cl.class16,count(1)
from rq3_cluster_label cl join rq3_monolith_all_category d
on (cl.item_id= d.category||':'||d.item_id)
group by cl.class16
 
13. Import results from Data Wrangler SBC Cluster Label

CREATE EXTERNAL TABLE rq3_cluster_sbc_label(
  item_id string ,
  unique_item_date string ,
  mean string ,
  sd string ,
  last_date string ,
  first_date string ,
  cv2 string ,
  adi string ,
  pct_contrib string ,
  class string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
  's3://dissert-430103706720-datalake/movement/sbc/sbc-v3-2023-04-30T15-36-12'
TBLPROPERTIES (
  'skip.header.line.count'='1', 
  'transient_lastDdlTime'='1683164861')


14. Enrich with SBC cluster and KMeans 16 class, KMeans 64 class labels.  This is unloaded for forecaster operations

create table dissert.training_data
WITH (
     format = 'PARQUET',
     external_location = 's3://dissert-430103706720-datalake/training-data/',
     write_compression ='SNAPPY'
     )
as
select
d.category, d.item_id, d.timestamp, d.target_value, d.qty, d.price, sale_code_m,
sale_code_g, sale_code_b, sale_code_x, sale_code_n, sale_code_c, sale_code_l, sale_code_s, 
record_exist, out_of_stock,holiday, thanksgiving_lead1, thanksgiving_lag1, christmas_lead1, christmas_lag1,
coalesce(sbc.class,'none') sbc_class,
cl.class16, cl.class64
from rq3_monolith_all_category d
 left outer join rq3_cluster_sbc_label sbc 
on (sbc.item_id= d.category||':'||d.item_id)
 join rq3_cluster_label cl
on (cl.item_id= d.category||':'||d.item_id)

#####
product forecast, harvest, predict



### Table 6

select 
avg(pre_error) avg_pre_error, 
avg(post_error) avg_post_error, 
count(1) record_count, 
count(distinct item_id) distinct_item_count
from (
select 
item_id,
abs(target_value-pre_prediction) pre_error,
abs(target_value-post_prediction) post_error
from (
select
td.category as cat,
td.item_id,
td.timestamp,
sum(td.target_value) target_value,
sum(round(pre.pre_prediction,0)) as pre_prediction,
sum(round(post.post_prediction,0)) as post_prediction
from
(select category, item_id, timestamp, cast(target_value as decimal) as target_value from dissert.training_data) td
 join  
(
select cat, item_id, timestamp, post_prediction as pre_prediction from dissert.t_ensemble_deepar_uv) pre
on (
pre.item_id = td.item_id
and pre.timestamp = td.timestamp
and pre.cat = td.category 
)
JOIN (
select cat, item_id, timestamp, post_prediction from dissert.t_ensemble_deepar) post
on (
td.item_id = post.item_id
and post.timestamp = td.timestamp
and post.cat = td.category
) 
group by 
td.category,
td.item_id, td.timestamp
)
)



### TABLE 7

select 
avg(pre_error) avg_pre_error, 
avg(post_error) avg_post_error, 
count(1) record_count, 
count(distinct item_id) distinct_item_count
from (
select 
item_id,
abs(target_value-pre_prediction) pre_error,
abs(target_value-post_prediction) post_error
from (
select
td.category as cat,
td.item_id,
td.timestamp,
sum(td.target_value) target_value,
sum(round(pre.pre_prediction,0)) as pre_prediction,
sum(round(post.post_prediction,0)) as post_prediction
from
(select category, item_id, timestamp, cast(target_value as decimal) as target_value from dissert.training_data) td
 join  
(
select cat, item_id, timestamp, post_prediction as pre_prediction from dissert.t_ensemble_deepar) pre
on (
pre.item_id = td.item_id
and pre.timestamp = td.timestamp
and pre.cat = td.category 
)
JOIN (
select cat, item_id, timestamp, post_prediction from dissert.t_cluster_deepar_sbc) post
on (
td.item_id = post.item_id
and post.timestamp = td.timestamp
and post.cat = td.category
) 
group by 
td.category,
td.item_id, td.timestamp
)
)


### TABLE 8

select 
avg(pre_error) avg_pre_error, 
avg(post_error) avg_post_error, 
count(1) record_count, 
count(distinct item_id) distinct_item_count
from (
select 
item_id,
abs(target_value-pre_prediction) pre_error,
abs(target_value-post_prediction) post_error
from (
select
td.category as cat,
td.item_id,
td.timestamp,
sum(td.target_value) target_value,
sum(round(pre.pre_prediction,0)) as pre_prediction,
sum(round(post.post_prediction,0)) as post_prediction
from
(select category, item_id, timestamp, cast(target_value as decimal) as target_value from dissert.training_data) td
 join  
(
select cat, item_id, timestamp, post_prediction as pre_prediction from dissert.t_ensemble_deepar) pre
on (
pre.item_id = td.item_id
and pre.timestamp = td.timestamp
and pre.cat = td.category 
)
JOIN (
select cat, item_id, timestamp, post_prediction from dissert.t_cluster_deepar_sbc16) post
on (
td.item_id = post.item_id
and post.timestamp = td.timestamp
and post.cat = td.category
) 
group by 
td.category,
td.item_id, td.timestamp
)
)


### TABLE 9
select 
avg(pre_error) avg_pre_error, 
avg(post_error) avg_post_error, 
count(1) record_count, 
count(distinct item_id) distinct_item_count
from (
select 
item_id,
abs(target_value-pre_prediction) pre_error,
abs(target_value-post_prediction) post_error
from (
select
td.category as cat,
td.item_id,
td.timestamp,
sum(td.target_value) target_value,
sum(round(pre.pre_prediction,0)) as pre_prediction,
sum(round(post.post_prediction,0)) as post_prediction
from
(select category, item_id, timestamp, cast(target_value as decimal) as target_value from dissert.training_data) td
 join  
(
select cat, item_id, timestamp, post_prediction as pre_prediction from dissert.t_ensemble_deepar) pre
on (
pre.item_id = td.item_id
and pre.timestamp = td.timestamp
and pre.cat = td.category 
)
JOIN (
select cat, item_id, timestamp, post_prediction from dissert.t_cluster_deepar_sbc64) post
on (
td.item_id = post.item_id
and post.timestamp = td.timestamp
and post.cat = td.category
) 
group by 
td.category,
td.item_id, td.timestamp
)
)







#### THIS IS TABLE 11, 2.188 MAE

select 
'ensemble' measure,
avg(post_error) avg_post_error, 
stddev(post_error) as sd_post_error,
skewness(post_error) as skewness_post_error,
kurtosis(post_error) as kurtosis_post_error,
count(1) obs_count , 
count(distinct cat||item_id) unique_item
from (
select t.cat, t.item_id, t.timestamp, 
abs(t.target_value-pre.pre_prediction) as pre_error,
abs(t.target_value-ensemble.post_prediction) as post_error 
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
)


then persist best as this...

CREATE TABLE t_ensemble_rq3_avg
WITH (
     format = 'TEXTFILE', 
     external_location = 's3://dissert-430103706720-datalake/result/t_ensemble_rq3_avg/',
     field_delimiter = ',',
     write_compression ='NONE'
     )
     as
-- persist as ...
