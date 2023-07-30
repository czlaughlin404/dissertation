
# Build cloud server

1. Use Deep Learning machine image with pytorch installed, ami-09c8945ef3e92c451

2.  Select a CPU size (others exist too)
	|    Size|	vCPUs	Memory |(GiB)
	|-----|------|------|
	| c5.large	|2|	4|
	| c5.xlarge|	4	|8|
	| c5.2xlarge	|8|	16|
	| c5.4xlarge	|16|	32|
	| c5.9xlarge|	36|	72|
	| c5.12xlarge|	48|	96|
	| c5.18xlarge|	72|	144|
	| c5.24xlarge|	96	|192|
	| c5.metal	|96|	192|

3.  Add permissions, security groups, etc

|topic|comment|
|----|----|
| IAM role  |  needs S3, Athena, Glue |
| VPC | public subnet |
| SG | needs to allow connection for you |

4. Connect to the server via SSH

5. Clone hub and install software
```
git clone https://github.com/czlaughlin404/dissertation.git
chmod 770 $HOME/dissertation/*.sh
cd $HOME/dissertation/
dependency.sh
```
