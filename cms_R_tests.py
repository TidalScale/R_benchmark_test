"""
This automation test tests cms data analysis R script with a range of samples of different size.
"""

import os.path
from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ts.test.shell import command
from psutil import virtual_memory
import re


CMS_TEST_R_FILENAME = 'cms_test.R'
CMS_DATA_PATH = os.path.join("data","cms_medicare")

# Expected outcome of R cms data analysis
EXPECTED_OUTPUT = ['load time user time', 'load time system time', 'load time elapse time',
                   'load time user child ','load time sys child',
                   'join time user time', 'join time system time', 'join time elapse time',
                   'join time user child', 'join time sys child',
                   'gam model user time', 'gam model system time', 'gam model elapse time',
                   'gam model user child','gam model sys child',
                   'glm model user time', 'glm model system time', 'glm model elapse time',
                   'glm model user child', 'glm model sys child',
                   'size of data frame after join', 'size of individual data frame' ]

"""
    This method keeps a test when a file path error occurs
"""
def validate_file_path_error(output, rc):
    if rc == 101:
        raise SkipTest('CMS dataset samples path does not exist!')

"""
    This method validates available memory before running automation tests.
"""
def validate_available_memory(size):
    virtual_mem = virtual_memory()
    available_mem = virtual_mem.available / (1024.0**3) # Get available size in gigabytes (bytes/1024 ^3 )
    if available_mem < size:
        raise SkipTest('Insufficent memory, cannot run test.')
    return True

"""
    Compares actual output from unit tests with expected output
"""
def cms_match_results(output, expected_output, size):
    #Extract benchmark results from stdout.
    output = output.split('\n')
    data_key = 'performance' + '-sample-' + str(size)

    # Removes [1] and additional spaces
    output = [re.sub(r'\[1\]', "", item).strip() for item in output]
    data_points = {}
    
    # System time results measured in seconds
    for line in output:
        for tag in expected_output:
            # Compare actual output with expected values to evaluate success of the test, regular expression matching is case insensitive
            result = re.search(tag, line)
            if result:
                # Search for a float value, integer value, or interger with text
                result = re.search('\d+.\d+ \w+|\d+ \w+|\d+.\d+|\d+', line, re.I)
                if result:
                    data_points.update({tag: result.group()})
                    break

    # The test is successfull if receive all expected outputs
    assert len(data_points.keys()) == len(expected_output)
    return{data_key: data_points}

"""
   This method runs cms data analysis R script in R using command line.
"""
def cms_analyze_with_R(filename, nsample, data_path, smoke_test):
    test_script_dir = os.path.dirname(os.path.realpath(__file__))
    source_file = os.path.join(test_script_dir, filename)
    
    # Provide range sequence of samples with a begin range and an end range.
    begin = 1
    end = nsample
    run_script_cmd = "R --no-save -q --slave < {0} --args {1} {2} {3} {4}".format(source_file, begin, end, data_path, smoke_test)
    
    rc, output = command(run_script_cmd)
    print rc
    validate_file_path_error(output, rc)
    assert rc == 0
    return output

"""
    This method analyzes cms dataset samples.
"""
def cms_data_analysis(nsample, size, smoke_test = False):
    cms_sample_test_details = None
    # Validate available memory before running automation test
    if validate_available_memory(size):
        output = cms_analyze_with_R(CMS_TEST_R_FILENAME, nsample, CMS_DATA_PATH, smoke_test)
        # validate_file_path_error(output)     # Validates file path errors
        cms_sample_test_details = cms_match_results(output, EXPECTED_OUTPUT, nsample)
    return cms_sample_test_details

"""
    This test tests cms data analysis in R with 1 sample
"""
@attr(nsample = "1")
def R_cms_sample_1_test():
    memory_size_GB = 17  # Expected memory for 1 sample dataset in gigabytes
    R_cms_sample_1_test.details = cms_data_analysis(nsample = 1, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 2 samples
"""
@attr(nsample = "2")
def R_cms_sample_2_test():
    memory_size_GB = 34  # Expected memory for 2 sample dataset in gigabytes
    R_cms_sample_2_test.details = cms_data_analysis(nsample = 2, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 3 samples
"""
@attr(nsample = "3")
def R_cms_sample_3_test():
    memory_size_GB = 51  # Expected memory for 3 sample dataset in gigabytes
    R_cms_sample_3_test.details = cms_data_analysis(nsample = 3, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 4 samples
"""
@attr(nsample = "4")
def R_cms_sample_4_test():
    memory_size_GB = 68  # Expected memory for 4 sample dataset in gigabytes
    R_cms_sample_4_test.details = cms_data_analysis(nsample = 4, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 5 samples
"""
@attr(nsample = "5")
def R_cms_sample_5_test():
    memory_size_GB = 85  # Expected memory for 5 sample dataset in gigabytes
    R_cms_sample_5_test.details = cms_data_analysis(nsample = 5, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 6 samples
"""
@attr(nsample = "6")
def R_cms_sample_6_test():
    memory_size_GB = 101  # Expected memory for 6 sample dataset in gigabytes
    R_cms_sample_6_test.details = cms_data_analysis(nsample = 6, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 7 samples
"""
@attr(nsample = "7")
def R_cms_sample_7_test():
    memory_size_GB = 118  # Expected memory for 7 sample dataset in gigabytes
    R_cms_sample_7_test.details = cms_data_analysis(nsample = 7, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 8 samples
"""
@attr(nsample = "8")
def R_cms_sample_8_test():
    memory_size_GB = 135  # Expected memory for 8 sample dataset in gigabytes
    R_cms_sample_8_test.details = cms_data_analysis(nsample = 8, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 9 samples
"""
@attr(nsample = "9")
def R_cms_sample_9_test():
    memory_size_GB = 152  # Expected memory for 9 sample dataset in gigabytes
    R_cms_sample_9_test.details = cms_data_analysis(nsample = 9, size = memory_size_GB)

"""
    This test tests cms data analysis in R with 10 samples
"""
@attr(nsample = "10")
def R_cms_sample_10_test():
    memory_size_GB = 169  # Expected memory for 10 sample dataset in gigabytes
    R_cms_sample_10_test.details = cms_data_analysis(nsample = 10, size = memory_size_GB)

"""
    This test tests cms data analysis in R with small sample
"""
@attr(nsample = "0")
def R_cms_sample_smoke_test():
    memory_size_GB = 7.3  # Expected memory for 10 sample dataset in gigabytes
    R_cms_sample_smoke_test.details = cms_data_analysis(nsample = 1, size = memory_size_GB, smoke_test = True)

