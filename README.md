# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL TIDALSCALE BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# R_benchmark_test

== Test Software ==

This software test requires the following software:

* CentOS 6.5
* Revolution R Enterprise 3.1 (with dplyr and __ plugins installed)

== Downloading the Test Data ==

All data is accessible from http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF.html[2008-2010 Data Entrepreneurs’ Synthetic Public Use Data Set].

Run the cms_data_download.sh script at the Linux command line to download all of the necessary data files.

To run all of the different-sized R tests in one go, simply run the runtests.sh script at the Linux command line.

== Test Results ==

The R_performance_analysis.pdf white paper documents our benchmark results from running this test on a 5 node TidalScale system.


