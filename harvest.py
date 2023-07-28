import boto3
import sys
import awswrangler as wr
boto3.setup_default_session(region_name="us-east-2")

outfile='/home/ec2-user/data/'+sys.argv[1]

sql1 = 'select category,item_id,timestamp,target_value,qty,price, \
        sale_code_m,sale_code_g,sale_code_b,sale_code_x,sale_code_n,\
        sale_code_c,sale_code_l,sale_code_s,record_exist,out_of_stock,\
        holiday,thanksgiving_lead1,thanksgiving_lag1,christmas_lead1,christmas_lag1\
        from training_data\
        where\
        ' 
sql2 = 'order by category,item_id, timestamp'

sql_where = sys.argv[2]

sql_str = sql1 + ' ' + sql_where + ' ' + sql2

print('SQL = ',sql_str)

df = wr.athena.read_sql_query(sql=sql_str, database="dissert")
df.to_csv(outfile, index=False)
