host=$(hostname)
cpus=$(grep -c ^processor /proc/cpuinfo)
echo "Running on $host with $cpus cpus and $total_mem_in_gb GB"
mkdir -p $HOME/benchmark-results
RESULTS="$HOME/benchmark-results/${host}-${cpus}-${total_mem_in_gb}GB"
mkdir -p $(dirname $RESULTS)
cd ~/tests/R-test/cms_test
# Start test
# Run on 157GB nodes
# 0=15GB, 1=34GB, 3=102GB (1 node), 5=170GB (2 nodes), 10=340GB (3 nodes), 16=544GB (4 nodes), 20=680GB (5 nodes)
for x in  0 1 3 5 10 16 20
do
	        echo Starting sample size $x
		        SAMPLE_RESULTS="$RESULTS-samples-$x"
			        nosetests -v cms_test.py -s -a "samples=$x,function=all" --with-json --json-file=$SAMPLE_RESULTS.json 2>&1 > $SAMPLE_RESULTS.log
done
