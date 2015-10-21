import os
from urllib2 import urlopen, HTTPError, URLError
from zipfile import ZipFile, ZipInfo
import cStringIO
import re

"""
    This constant contains a key value pair of sample number and URLs locations which is used to download data for all 20 samples.
"""
CMS_SAMPLES_URLS = {1:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_1.zip',
              'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_1.zip',
              'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_1.zip',
              'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.zip',
              'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.zip',
              'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.zip',
              'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.zip',
              'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.zip'],
    2:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_2.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_2.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_2.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_2.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_2.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_2A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_2B.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_2.zip'],
    3:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_3.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_3.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_3.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_3.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_3.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_3A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_3B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_3.zip'],
    4:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_4.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_4.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_4.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_4.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_4.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_4A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_4B.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_4.zip'],
    5:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_5.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_5A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_5B.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_5.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_5.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_5.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_5.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_5.zip',],
    6:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_6.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_6A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_6B.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_6.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_6.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_6.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_6.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_6.zip',],
    7:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_7.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_7A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_7B.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_7.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_7.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_7.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_7.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_7.zip',],
    8:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_8.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_8A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_8B.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_8.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_8.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_8.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_8.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_8.zip',],
    9:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_9.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_9A.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_9B.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_9.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_9.zip',
       'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_9.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_9.zip',
       'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_9.zip',],
    10:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_10.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_10A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_10B.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_10.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_10.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_10.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_10.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_10.zip',],
    11:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_11.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_11.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_11.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_11.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_11.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_11A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_11B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_11.zip',],
    12:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_12.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_12.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_12.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_12.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_12.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_12A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_12B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_12.zip',],
    13:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_13.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_13.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_13.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_13.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_13.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_13A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_13B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_13.zip',],
    14:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_14.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_14.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_14.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_14.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_14.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_14A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_14B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_14.zip',],
    15:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_15.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_15.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_15.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_15.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_15.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_15A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_15B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_15.zip',],
    16:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_16.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_16.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_16.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_16.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_16.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_16A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_16B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_16.zip',],
    17:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_17.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_17.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_17.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_17.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_17.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_17A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_17B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_17.zip',],
    18:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_18.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_18.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_18.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_18.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_18.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_18A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_18B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_18.zip',],
    19:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_19.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_19.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_19.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_19.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_19.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_19A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_19B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_19.zip',],
    20:['http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_20.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2009_Beneficiary_Summary_File_Sample_20.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2010_Beneficiary_Summary_File_Sample_20.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_20.zip',
        'http://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_20.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_20A.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_20B.zip',
        'http://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_20.zip',],}

"""
    This method downloads cms data from the web.
"""
def get_cms_data(data_path, samples):
    cms_data_dir, result = get_dir_path(data_path)
    if result:
        [download_data_from_url(url, cms_data_dir) for x in samples for urls in CMS_SAMPLES_URLS[x] for url in urls.split(',') if not file_exist(url, cms_data_dir)]

"""
    This method gets cmd data directory path, if the directory does not exist it creates the directory structure.
"""
def get_dir_path(path):
    result = False
    try:
        cms_data_dir = os.path.realpath(path)
        if not os.path.exists(cms_data_dir):
            os.makedirs(cms_data_dir)
        result = True
    except IOError:
        print 'Unexpected error. Cannot create directory'
    return (cms_data_dir, result)

"""
    This method downloads compressed data from the web and stores it as a decompressed csv file.
"""
def download_data_from_url(url, cms_data_dir):
    web_zip_file = None
    try:
        web_zip_file = urlopen(url)
        buffer = cStringIO.StringIO(web_zip_file.read()) # Reads compressed zip file in memory and stores in buffer
        # Unzip and save file
        with zipfile.ZipFile(buffer) as zfile:
            zfile.extract(zfile.namelist()[0], cms_data_dir)
    except HTTPError as e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code:', e.code
        print 'Error:', e.read()
    except URLError as e:
        print 'We failed to reach a server.'
        print e.reason
    except IOError:
        print 'An unepected error occured while reading or extracting zip file from web.'
    except RuntimeError:
        print 'An error occured at run time! Error occured while reading zip file'
    return web_zip_file

"""
    This method extracts file name from the URL and checks whether the sample file exist in the cms data directory.
"""
def file_exist(url, cms_data_dir):
    result = False
    try:
        matches = re.search("\w*.zip", url)
        filename = matches.group()[:-4]      # Remove ".zip" file extension
        filename += ".csv"                   # Use filename with .csv extension
        source_file = os.path.join(cms_data_dir, filename)
        if os.path.exists(source_file):
            result = True
    except NoneType:
        print 'Match not found for file name in URL.'
    return result
