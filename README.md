THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL TIDALSCALE BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

# R_benchmark_test

This software benchmark explores the performance of R analytics over a large data set on a TidalScale system.

The TidalScale HyperKernel provides the ability to scale-up the execution of applications beyond the limits of a single physical server. Unlike traditional scale-up or scale-out approaches — which either require purchasing new hardware or rewriting software to run across clusters — TidalScale’s approach creates a Software-Defined Server that runs on existing commodity hardware and doesn’t require any changes to operating systems or application software. The result: improving application performance and achieving insights sooner without the expense of scaling up or the time lost to traditional scale-out efforts. 

R is an analytic and statistical programming language whose use is rapidly spreading as organizations sharpen their ability to understand and learn from data they amass. Many operations in R are memory intensive, and analysts and data scientists often struggle to keep their working data sets within the limitations of a single computer to avoided the dreaded "Memory Cliff".

The TidalScale Hyperkernel makes it possible for multiple physical computers to operate as a single system which enables the unmodified application to use the aggregate RAM, CPUs and I/O of the underlying hardware. The R application therefore "sees" a single computer system while the TidalScale Hyperkernels enable growth and performance by scaling-out on commodity hardware. 

In this benchmark, we compare the performance and capacity of R applications with large datasets, running on "bare metal" servers versus a server instance on TidalScale. The benchmark results illustrate important aspects of TidalScale performance as of version 1.0. We demonstrate scalable performance of four different R operations which, more generally, are representative of the kinds of analytic workloads that benefit from running on large, coherent systems.

## Test Software

This software test requires the following software:

* CentOS 7.2
* Revolution R Open 8.0.3 with a CRAN snapshot taken on 2015-04-01

TidalScale's internal regression test framework is written in Python to be OS-independent and is executed under the control of the Nose test framework. Nose extends Python's standard unittest module (see https://docs.python.org/2/library/unittest.html) and provides options for test discovery/selection and the recording of test results in a standardized way among many other capabilities. This R benchmark program relies on Nose test.

## Downloading the Test Data

All data is accessible from the Data Entrepreneurs Synthetic Public Use Data Set (see https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF.html).

Run the scripts/cms_data_download.sh script at the Linux command line to download all of the necessary data files in a directory that has >70GB storage space. Then you must modify cms_data_analysis.R to point at that directory.

To run all of the different-sized R tests in one go, simply run the runtests.sh script at the Linux command line. A full test run takes about a week (if you have a system large enough to hold all the data in memory ;).

## Installing R packages

After installing R you will need to install the following packages one at a time from inside R:

> install.packages('foo', repos='http://cran.us.r-project.org') 

Where 'foo'= (checkpoint, pryr, dplyr, mgcv, rpart, randomForest, FNN, doParallel, foreach, Matrix)

## Running the Test

This is a long running job so it is convenient to start a tmux session and then execute the runtest.sh script such that the results are written to a text file:

$ ./runtests.sh | tee testresult.txt

You can edit the runtests.sh script to test any combination of in-memory workload sizes desired.

## Test Results

The https://www.tidalscale.com/R_benchmark.html white paper documents our benchmark results from running this test on a 5 node TidalScale system.

## Comments and Observations

* In our experience of trying various CPU configurations, it appears that R does best on systems with 8 CPUs. This is true on both bare metal hardware _and_ TidalScale systems.
* Garbage collection in R affects load times negatively (no matter what system it is running on). In this benchmark we control garbage collection by turning it off (`gc(F)`) during file load and then turning it on (`gc(T)`) for subsequent operations.
* A log-log chart is the best way to observe results in a manner that allows one to see patterns at all sizes of test runs.

## Correct Output

$ [1] "/data/cms"
$           used (Mb) gc trigger (Mb) max used (Mb)
$ Ncells 1197785 64.0    1590760 85.0  1476915 78.9
$ Vcells 1732626 13.3    2899967 22.2  2092494 16.0
$ [1] 1 2 3 4 5
$  [1] "1A" "1B" "2A" "2B" "3A" "3B" "4A" "4B" "5A" "5B"
$ [1] "Number of cores in use 7"
$ [1] "load time user time 1112.684"
$ [1] "load time system time 544.766"
$ [1] "load time elapse time 2255.8"
$ [1] "load time user child 0"
$ [1] "load time sys child 0"
$ [1] "size of individual data frame 30 GB"
$ [1] "mem_used after data load 30.1 GB"
$ [1] "join time user time 169.891"
$ [1] "join time system time 11.616"
$ [1] "join time elapse time 181.387"
$ [1] "join time user child 0"
$ [1] "join time sys child 0"
$ [1] "size of data frame after join 45.5 GB"
$ [1] "mem_used after data join 77.3 GB"
$              used    (Mb)  gc trigger     (Mb)   max used    (Mb)
$ Ncells    2160505   115.4     4418719    236.0    4418719   236.0
$ Vcells 9651980455 73638.8 14227509132 108547.3 9706860384 74057.5
$ [1] "gam model user time 471.255"
$ [1] "gam model system time 89.2850000000001"
$ [1] "gam model elapse time 560.175"
$ [1] "gam model user child 0"
$ [1] "gam model sys child 0"
$ [1] "mem_used after executing gam model 81.1 GB"
$ [1] "glm model user time 835.507"
$ [1] "glm model system time 172.99"
$ [1] "glm model elapse time 1014.964"
$ [1] "glm model user child 0"
$ [1] "glm model sys child 0"
$ [1] "mem_used after executing glm model 93.5 GB"
$ [1] "decision trees user time 458.995"
$ [1] "decision trees system time 0"
$ [1] "decision trees elapse time 458.726000000001"
$ [1] "decision trees user child 0"
$ [1] "decision trees sys child 0"
$ [1] "mem_used after executing decision trees model 93.5 GB"
$ [1] "random forest user time 272.128"
$ [1] "random forest system time 3.77599999999995"
$ [1] "random forest elapse time 275.719"
$ [1] "random forest user child 0"
$ [1] "random forest sys child 0"
$ [1] "mem_used after executing random forest model 93.6 GB"
$ [1] "K nearest neighbors user time 920.164"
$ [1] "K nearest neighbors system time 2.851"
$ [1] "K nearest neighbors elapse time 922.388"
$ [1] "K nearest neighbors user child 0"
$ [1] "K nearest neighbors sys child 0"
$ [1] "mem_used after executing knn model 93.9 GB"
$ [1] "/data/cms"
$           used (Mb) gc trigger (Mb) max used (Mb)
$ Ncells 1197784 64.0    1590760 85.0  1476915 78.9
$ Vcells 1732625 13.3    2899967 22.2  2092488 16.0


