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

== Test Software ==

This software test requires the following software:

* CentOS 6.5
* Revolution R Enterprise 3.1 (with dplyr and __ plugins installed)

== Downloading the Test Data ==

All data is accessible from http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF.html[2008 to 2010 Data Entrepreneurs Synthetic Public Use Data Set].

Run the cms_data_download.sh script at the Linux command line to download all of the necessary data files.

To run all of the different-sized R tests in one go, simply run the runtests.sh script at the Linux command line. A full test run takes about 40 hours.

== Test Results ==

The R_performance_analysis.pdf white paper documents our benchmark results from running this test on a 5 node TidalScale system.

== Comments and Observations ==

xxx


