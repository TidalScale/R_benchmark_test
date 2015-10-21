"""
Center for Medicaid Service (CMS) medicare data analysis with different sample sizes.
"""

import os.path
from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
from ts.test.shell import command
from psutil import virtual_memory
import re
from nose.tools import make_decorator
from nose.tools import with_setup
from ts.test.decorators import os_family

""" File name of CMS data analysis R script """
CMS_TEST_R_GLM = 'cms_data_analysis_glm.R'
CMS_TEST_R_GAM = 'cms_data_analysis_gam.R'
CMS_TEST_R_FILENAME = 'cms_data_analysis.R'
CMS_DATA_PATH = os.path.join('/', 'data', 'cms')

GB_MEMORY_PER_SAMPLE = 17
MAX_SAMPLES = 20

# File names of CMS medicare data
CMS_PATIENT = 'DE1_0_{0}_Beneficiary_Summary_File_Sample_{1}.csv'
CMS_INPATIENT = 'DE1_0_2008_to_2010_Inpatient_Claims_Sample_{0}.csv'
CMS_OUTPATIENT = 'DE1_0_2008_to_2010_Outpatient_Claims_Sample_{0}.csv'
CMS_CARRIER_CLAIMS = 'DE1_0_2008_to_2010_Carrier_Claims_Sample_{0}.csv'
CMS_DRUG = 'DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_{0}.csv'
YEARS = [2008, 2009, 2010]
CLAIMS = ['1A', '2B']

# Expected outcome of R cms data analysis
EXPECTED_OUTPUT = { CMS_TEST_R_FILENAME: ['load time user time', 'load time system time', 'load time elapse time',
                   'load time user child ', 'load time sys child',
                   'join time user time', 'join time system time', 'join time elapse time',
                   'join time user child', 'join time sys child',
                   'gam model user time', 'gam model system time', 'gam model elapse time',
                   'gam model user child', 'gam model sys child',
                   'glm model user time', 'glm model system time', 'glm model elapse time',
                   'glm model user child', 'glm model sys child',
                   'decision trees user time', 'decision trees system time', 'decision trees elapse time',
                   'decision trees user child', 'decision trees sys child',
                   'random forest user time', 'random forest system time', 'random forest elapse time',
                   'random forest user child', 'random forest sys child',
                   'K nearest neighbors user time', 'K nearest neighbors system time', 'K nearest neighbors elapse time',
                   'K nearest neighbors user child', 'K nearest neighbors sys child',
                   'size of data frame after join', 'size of individual data frame',
                   'mem_used after data load', 'mem_used after data join',
                   'mem_used after executing gam model', 'mem_used after executing glm model',
                   'mem_used after executing decision trees model', 'mem_used after executing random forest model',
                   'mem_used after executing knn model'],
                   CMS_TEST_R_GLM: ['join time sys child', 'glm model elapse time', 'load time user time', 'load time sys child', 'load time user child ', 'glm model user child', 'mem_used after data load', 'load time system time', 'glm model system time', 'glm model sys child', 'join time system time', 'mem_used after executing glm model', 'glm model user time', 'size of data frame after join', 'load time elapse time', 'join time user time', 'join time elapse time', 'mem_used after data join', 'join time user child', 'size of individual data frame'],
                   CMS_TEST_R_GAM: ['join time sys child', 'gam model elapse time', 'load time user time', 'load time sys child', 'load time user child ', 'gam model user child', 'mem_used after data load', 'load time system time', 'gam model system time', 'gam model sys child', 'join time system time', 'mem_used after executing gam model', 'gam model user time', 'size of data frame after join', 'load time elapse time', 'join time user time', 'join time elapse time', 'mem_used after data join', 'join time user child', 'size of individual data frame']
                   }


def validate_data_files_exists(size, data_path):
    """ Validates whether data files for cms samples exist"""

    # If any file is missing the test will be skipped.
    for i in range(1, size + 1):
        validate_patient_file_exist(filename=CMS_PATIENT, years=YEARS, sample_id=i, data_path=data_path)
        validate_cms_file_exist(filename=CMS_INPATIENT, sample_id=i, data_path=data_path)
        validate_cms_file_exist(filename=CMS_OUTPATIENT, sample_id=i, data_path=data_path)
        validate_claims_file_exist(filename=CMS_CARRIER_CLAIMS, claim_ids=CLAIMS, data_path=data_path)
        validate_cms_file_exist(filename=CMS_DRUG, sample_id=i, data_path=data_path)
    return True


def validate_cms_file_exist(filename, sample_id, data_path):
    """Validate whether cms files exist. """
    return validate_file_exist(filename=filename.format(sample_id), data_path=data_path)


def validate_claims_file_exist(filename, claim_ids, data_path):
    """Validate whether files for carrier claims exist. """
    [validate_file_exist(filename=filename.format(i), data_path=data_path) for i in claim_ids]


def validate_patient_file_exist(filename, years, sample_id, data_path):
    """Validate whether files for beneficiary exist. """
    [validate_file_exist(filename=filename.format(i, sample_id), data_path=data_path) for i in years]


def validate_file_exist(filename, data_path):
    """ Validate whether the file exists """

    if not os.path.exists(os.path.join(data_path, filename)):
        raise SkipTest('Error! File %s does not exist.' % filename)
    return True


def has_enough_memory(minimum_memory):
    """
    Check for sufficient memory

    NOTE: minimum memory in GiB
    """

    virtual_mem = virtual_memory()
    available_mem = virtual_mem.available / (1024.0 ** 3)  # Get available size in gigabytes (bytes/1024 ^3 )
    if available_mem < minimum_memory:
        raise SkipTest('Minimum %.1f GiB required but only %.1f GiB available (short by %.1f GiB).' % (minimum_memory, available_mem, minimum_memory - available_mem))
    return True


def memory_required(nsamples):
    """Memory in GB required to run test"""

    if nsamples==0:
        return 0 #7.3
    else:
        return float(GB_MEMORY_PER_SAMPLE * nsamples)


def cms_match_results(output, expected_output, size):
    """Compares actual output from unit tests with expected output"""

    # Extract benchmark results from stdout.
    output = output.split('\n')
    data_key = 'performance'

    # Removes [1] and additional spaces
    output = [re.sub(r'\[1\]', "", item).strip() for item in output]
    data_points = {}

    # System time results measured in seconds
    for line in output:
        for tag in expected_output:
            # Compare actual output with expected values to evaluate success of the test, regular expression matching is case insensitive
            result = re.search(tag, line)
            if result:
                # Search for a float value, integer value, or integer with text
                result = re.search('\d+.\d+ \w+|\d+ \w+|\d+.\d+|\d+', line, re.I)
                if result:
                    data_points.update({tag: result.group()})
                    break

    # The test is successful when receive all expected outputs
    assert len(data_points.keys()) == len(expected_output)
    return {data_key: data_points}


def cms_analyze_with_R(filename, nsample, data_path, smoke_test):
    """This method runs cms data analysis R script in R using command line."""

    test_script_dir = os.path.dirname(os.path.realpath(__file__))

    # Provide range sequence of samples with a begin range and an end range.
    begin = 1
    end = nsample
    cd_cmd = 'cd %s;' % test_script_dir
    run_script_cmd = "R --no-save -q --slave < {0} --args {1} {2} {3} {4}".format(filename, begin, end, data_path,
                                                                                  smoke_test)

    test_cmd = ' '.join([cd_cmd, run_script_cmd])
    rc, output , _ = command(test_cmd)
    assert rc == 0, "Command \"%s\" returned %d" % (test_cmd, rc)
    return output


def cms_data_analysis(samples, minimum_memory, smoke_test=False, rscript=CMS_TEST_R_FILENAME):
    """analyzes samples"""

    cms_sample_test_details = None
    # Validate available memory and file exist before running automation test
    if has_enough_memory(minimum_memory) and validate_data_files_exists(size=samples, data_path=CMS_DATA_PATH):
        output = cms_analyze_with_R(rscript, samples, CMS_DATA_PATH, smoke_test)
        # validate_file_path_error(output)     # Validates file path errors
        cms_sample_test_details = cms_match_results(output, EXPECTED_OUTPUT[rscript], samples)
    return cms_sample_test_details


def setup_function(size=1, data_path=CMS_DATA_PATH):
    validate_data_files_exists(size, data_path=data_path)
    # Clear buffer caches
    if os_family == 'Linux':
        rc, _, _ = command("sync && sudo sh -c \"echo 3 > /proc/sys/vm/drop_caches\"")
        assert rc == 0
        rc, _, _ = command("sudo swapoff -a")
        assert rc == 0


def samples(num):
    """Decorator sets number of samples"""

    def sample_decorator(func):
        def test_wrapper():
            # Sample 0 is smoke test
            if num == 0:
                func.sample = 1
                func.smoke_test=True
            else:
                func.sample = num
                func.smoke_test = False

            func.minimum_memory = memory_required(func.sample)

            # Execute test
            func()

        return make_decorator(func)(test_wrapper)

    return sample_decorator


complete_test = """
@with_setup(setup=setup_function())
@attr(samples=%(samples)d, function='all')
@samples(%(samples)d)
def R_cms_sample_%(samples)d_test():
    func = R_cms_sample_%(samples)d_test
    func.details = cms_data_analysis(
        func.sample,
        func.minimum_memory,
        smoke_test=func.smoke_test,
        rscript=CMS_TEST_R_FILENAME
        )
"""


glm_test = """
@with_setup(setup=setup_function())
@attr(samples=%(samples)d, function='glm')
@samples(%(samples)d)
def R_cms_glm_sample_%(samples)d_test():
    func = R_cms_glm_sample_%(samples)d_test
    func.details = cms_data_analysis(
        func.sample,
        func.minimum_memory,
        smoke_test=func.smoke_test,
        rscript=CMS_TEST_R_GLM
        )
"""


gam_test = """
@with_setup(setup=setup_function())
@attr(samples=%(samples)d, function='gam')
@samples(%(samples)d)
def R_cms_gam_sample_%(samples)d_test():
    func = R_cms_gam_sample_%(samples)d_test
    func.details = cms_data_analysis(
        func.sample,
        func.minimum_memory,
        smoke_test=func.smoke_test,
        rscript=CMS_TEST_R_GAM
        )
"""


# Generate test functions with different sample sizes
# Sample 0 test is smoke test
for x in range(0, MAX_SAMPLES + 1):
    for t in [complete_test, glm_test, gam_test]:
        exec t % {'samples': x}

#http://pythontesting.net/framework/nose/nose-fixture-reference/