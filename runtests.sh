host=$(hostname)
cpus=$(grep -c ^processor /proc/cpuinfo)
echo "Running on $host with $cpus cpus and $total_mem_in_gb GB"
mkdir -p $HOME/benchmark-results
RESULTS="$HOME/benchmark-results/${host}-${cpus}-${total_mem_in_gb}GB"
mkdir -p $(dirname $RESULTS)
cd ~/tests/R-test/cms_test
# Start test
# Run on five 128GB nodes (i.e. a 640GB guest)
for x in  0 1 3 5 8 10 13 17
do
	        echo Starting sample size $x
		        SAMPLE_RESULTS="$RESULTS-samples-$x"
			        nosetests -v cms_test.py -s -a "samples=$x,function=all" --with-json --json-file=$SAMPLE_RESULTS.json 2>&1 > $SAMPLE_RESULTS.log
done
