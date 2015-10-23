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

The TidalScale Hyperkernel provides the ability to scale-up the execution of applications beyond the limits of a single server. TidalScale's approach delivers better performance for the application while avoiding the need for re-architecting the application or re-engineering for scale-out to achieve good performance. 

R is an analytic and statistical programming language whose use is rapidly spreading as organizations sharpen their ability to understand and learn from data they amass. Many operations in R are memory intensive, and analysts and data scientists often struggle to keep their working data sets within the limitations of a single computer. The TidalScale Hyperkernel makes it possible for multiple physical computers to operate as a single system which enables the unmodified application to use the aggregate RAM, CPUs and I/O of the underlying hardware. The R application therefore "sees" a single computer system while the TidalScale Hyperkernels enable growth and performance by scaling-out on commodity hardware. 

In this benchmark, we compare the performance and capacity of R applications with large datasets, running on "bare metal" servers versus a server instance on TidalScale. The benchmark results illustrate important aspects of TidalScale performance as of version 1.0. We demonstrate scalable performance of four different R operations which, more generally, are representative of the kinds of analytic workloads that benefit from running on large, coherent systems.

## Test Software

This software test requires the following software:

* CentOS 6.5
* Revolution R Enterprise 3.1 (but this should work fine on Revolution R Open)

TidalScale's internal regression test framework is written in Python to be OS-independent and is executed under the control of the Nose test framework. Nose extends Python's standard https://docs.python.org/2/library/unittest.html[unittest] module and provides options for test discovery/selection and the recording of test results in a standardized way among many other capabilities. This R benchmark program relies on Nose test.

## Downloading the Test Data

All data is accessible from https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF.html [Data Entrepreneurs Synthetic Public Use Data Set].

Run the scripts/cms_data_download.sh script at the Linux command line to download all of the necessary data files.

To run all of the different-sized R tests in one go, simply run the runtests.sh script at the Linux command line. A full test run takes about a week.

## Test Results

The R_performance_analysis.pdf white paper documents our benchmark results from running this test on a 5 node TidalScale system.

## Comments and Observations

* In our experience of trying various CPU configurations, it appears that R does best systems with 8 CPUs. This is true on both bare metal hardware _and_ TidalScale systems.
* Garbage collection in R affects load times negatively. In this benchmark we control garbage collection by turning it off (`gc(F)`) during file load and then turning it on (`gc(T)`) for subsequent operations.
* A log-log chart is the best way to observe results in a manner that allows one to see patterns at all sizes of test runs.




