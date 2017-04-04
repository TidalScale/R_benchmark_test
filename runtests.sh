# Chuck Piercey
#!/bin/bash
sudo swapoff -a
#the Aproximate in memory size is 34 GB * the x value below (i.e. 20*34 = 640 GB).
for x in 1 5 10 17 20
do
        echo Starting size $x
        /usr/bin/time --format="\nMax mem:%M kilobytes\n" R --no-save -q --slave < cms_data_analysis.R --args 1 $x /data/cms False >> testoutput.txt
done
