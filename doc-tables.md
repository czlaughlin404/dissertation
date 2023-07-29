

# Table 6
```
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

```

# TABLE 7
```
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
```

#  TABLE 8
```
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
```

#  TABLE 9

```
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
```



# Table 11

```
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
```
