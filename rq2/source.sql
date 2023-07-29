select case 
when cluster_member like '%smooth%' then 'smooth'
when cluster_member like '%lumpy%' then 'lumpy'
when cluster_member like '%intmittent%' then 'intermittent'
when cluster_member like '%erratic%' then 'erratic'
else 'none' end cluster_member,
cat, item_id, timestamp, target_value, pre_prediction, post_prediction, abs(target_value-pre_prediction) pre_error, abs(
target_value-post_prediction) post_error
From t_cluster_deepar_sbc
