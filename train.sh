ret=$#

if [ $ret -ne 3 ]; then
  echo ""
  echo "correct usage: train.sh model_variant uv|mv S3folder"
  echo ""  
  exit
fi

source activate pytorch

for f in `cd $HOME/data/;ls -1Sr *.csv | head -1000`
do

	echo $f

        running=`ps -ef | grep train.[p]y | wc -l`

        if [ "$running" -ge 2 ]
        then
        echo "wait"
        wait
        fi

        sleep 1
        echo "submitting "$f

        python train.py $HOME/data/$f $HOME/predictions/$f $1 $2 &

done

echo "waiting on predict.py to complete"
wait

aws s3 sync /home/ec2-user/predictions/ s3://dissert-430103706720-datalake/$3/

#uncomment to terminate on completion
#sudo shutdown now
