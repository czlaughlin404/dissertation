# install dependencies onto public AMI ami-09c8945ef3e92c451

source activate pytorch
sudo yum update
pip3 install autogluon==0.7
pip3 install awswrangler

mkdir $HOME/data/ 2> /dev/null
mkdir $HOME/predictions/ 2> /dev/null
