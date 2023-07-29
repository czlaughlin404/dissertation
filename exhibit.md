Use Deep Learning AMI
ami-09c8945ef3e92c451

Select a CPU size (others exist too)
Size	vCPUs	Memory (GiB)
c5.large	2	4
c5.xlarge	4	8
c5.2xlarge	8	16
c5.4xlarge	16	32
c5.9xlarge	36	72
c5.12xlarge	48	96
c5.18xlarge	72	144
c5.24xlarge	96	192
c5.metal	96	192

Add permissions, security groups, etc
IAM role S3-EC2-Full-Admin 
VPC  vpc-a31397c8 
SG sg-04e79bfabc9bbb340 (launch-wizard-3)

Connect to the server via SSH

Clone hub and install software

git clone https://github.com/czlaughlin404/dissertation.git
chmod 770 $HOME/dissertation/*.sh
cd $HOME/dissertation/
dependency.sh


Harvest data and generate forecasts for any number of discrete data or model types

clear
source activate pytorch
python3 harvest.py test1.csv "item_id like '18.%3828100213'"
python3 harvest.py test2.csv "item_id like '18.%3828100313'"

Train and generate forecast

./train.sh 
./train.sh AutoARIMA uv experimentname

Place data table view on CSV data

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
