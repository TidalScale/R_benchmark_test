# Clear the memory before running
rm(list= ls())

options(echo=FALSE) # Hides R commands in output file
args <- commandArgs(trailingOnly = TRUE) # trailingOnly=TRUE means that only your arguments are returned
args_from <- as.numeric(args[1])   # Get cms sample start of range
args_to <- as.numeric(args[2])   # Get cms sample end of range
data_path <- args[3]   #Get cms data directory path
smoke_test <- toupper(args[4])

# Validate cms data directory path if it exists. Exit the program if the path does not exist
data_file_path <- file.path(data_path)
print(data_file_path)

#Raise error if cms data directory does not exist.
if(file.exists(data_file_path) == FALSE){
  q(save="no", status = 101)
}

# Load libraries and supress messages to get a clean output
load_libraries <- c("pryr","dplyr", "mgcv")
a <- lapply(load_libraries, function(x) suppressMessages( library(x, character.only = T)))

# Load supporting file for data analysis
source("cms_data_load.R")
source("cms_data_preprocess.R")
source("cms_utils.R")

#Set cms dataset path
setwd(data_file_path)

if(smoke_test == FALSE){
  # Gets sample range from command line
  # Create a sequence of sample from command line arguments, using arg_from and arg_to
  test_sample <- seq(from = args_from, to = args_to, by = 1)
  claims_sample <- character()
  for(i in test_sample){
    sample1 <- paste0(i, "A")
    sample2 <- paste0(i, "B")
    claims_sample <- c(claims_sample, sample1, sample2)
  }
} else{
  test_sample <- 1
  claims_sample <- "1A"
}
print(test_sample)
print(claims_sample)
#small_test_sample <- 2
#small_claims_sample <- c("2A")

years <- c(2008,2009,2010)
sample_id <-  test_sample     #    small_test_sample
claims_sample <- claims_sample  #  small_claims_sample

gc(F)

#---------------------------------------------
# Step 1: Load data.
#         Read cms medicare data, a public health care dataset.
#---------------------------------------------
load_time <- numeric(length = 5)
load_time <- rep(0.,5)

# Get patient data, also known as beneficiary summary 
patient_file_name <- "DE1_0_%s_Beneficiary_Summary_File_Sample_%s.csv"
load_time <- load_time + system.time(patient <- get_data_read_csv_patients(patient_file_name, sample_id, years))
patient <- data_pre_process(patient)

# Get Inpatient claims data
inpatient_file_name <- "DE1_0_2008_to_2010_Inpatient_Claims_Sample_%s.csv"
load_time <- load_time + system.time(inpatient <- get_data_read_csv(inpatient_file_name, sample_id, smoke_test))
  
# Get out patient claims data
outpatient_file_name <- "DE1_0_2008_to_2010_Outpatient_Claims_Sample_%s.csv"
load_time <- load_time + system.time(outpatient <- get_data_read_csv(outpatient_file_name, sample_id, smoke_test))
  
# Get carrier claims data
claims_file_name <- "DE1_0_2008_to_2010_Carrier_Claims_Sample_%s.csv"
load_time <- load_time + system.time(carrier_claims <- get_data_read_csv(claims_file_name, claims_sample, smoke_test))

# Get patient drugs data 
drug_file_name <- "DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_%s.csv"
load_time <- load_time + system.time(drug <- get_data_read_csv(drug_file_name, sample_id, smoke_test))

print_time("load time", load_time)
# The size of data frame objects in memory that contain data for patient, inpatient, outpatient, carrier claims, and drug
df_size <- capture.output(object_size(patient, inpatient, outpatient, carrier_claims, drug))
print(paste0("size of individual data frame ", df_size))

#-----------------------------------------------------------------------
# Step 2: Data processing step
# Merge patient data with inpatient, outpatient, claims, and drug data.
#-----------------------------------------------------------------------

gc(T)

join_time <- numeric(length = 5)
join_time <- rep(0.,5)

# Create a new column for year, using existing date column
inpatient <- add_year(inpatient, "clm_from_dt")
join_time <- join_time + system.time(cms_inpatient <- left_join(patient, inpatient, by = c("desynpuf_id", "year")))

# Create a new column for year, using existing date column
outpatient <- add_year(outpatient, "clm_from_dt")
join_time <- join_time + system.time(cms_outpatient <- left_join(patient, outpatient, by = c("desynpuf_id", "year")))

carrier_claims <- add_year(carrier_claims, "clm_from_dt")
join_time <- join_time + system.time(cms_claims_patient <- left_join(patient, carrier_claims, by = c("desynpuf_id", "year")))

drug <- add_year(drug, "srvc_dt")
join_time <- join_time + system.time(cms_drug_patient <- left_join(patient, drug, by = c("desynpuf_id", "year")))

print_time("join time", join_time)
# Print object size after merging patient data with inpatient, outpatient, carrier claims, and drugs
join_df_size <- capture.output(object_size(cms_inpatient, cms_outpatient, cms_claims_patient, cms_drug_patient, units = "GB"))
print(paste0("size of data frame after join ", join_df_size))

#-----------------------------------------------
# Step 3: Analyze data 
#         Create models and find best fit.
#-----------------------------------------------
# Formula for patient demographic which includes age, gender, and ethnicity/race 

# Generalized additive modeling 1

# Formula for to predict total inpatient expenses. 
# It includes patient demographic, chronic condition, and prescription drug covariates.
# Patient demographics varibales includes age, gender, and ethnicity/race.


# Generalized additive modeling 2
formula_gam1 <- (medreimb_ip + benres_ip + pppymt_ip) ~ s(age) + bene_sex_ident_cd + race_white + 
              race_black + race_others + race_hispanic + sp_alzhdmta + sp_chf + sp_chrnkidn + 
              sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + sp_osteoprs +  
              sp_ra_oa + sp_strketia + s(qty_dspnsd_num) + s(days_suply_num) + s(ptnt_pay_amt) + 
              s(tot_rx_cst_amt)

fit_gam1_time <- system.time(fit_gam1 <- gam(formula_gam1, 
                              family=gaussian(link=identity), data=cms_drug_patient, subset = (medreimb_ip > 1000)))

#library(ggplot2)
#graph_gam_hist_reimb_ip <- 
 # ggplot(cms_drug_patient, aes( x=medreimb_ip)) + 
#        geom_histogram(binwidth = 50000, colour = "black", fill = "white")

#summary(fit_gam1)

print_time("gam model", fit_gam1_time)

#----------------
# Genralized linear model
#----------------
# Formula for to predict total inpatient expenses. 
# It includes patient demographic, chronic condition, and prescription drug covariates.
# Patient demographics varibales includes age, gender, and ethnicity/race.
formula_glm1 <- (medreimb_ip + benres_ip + pppymt_ip) ~ age + bene_sex_ident_cd + race_white + 
                race_black + race_others + race_hispanic + sp_alzhdmta + sp_chf + sp_chrnkidn + 
                sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + sp_osteoprs +  
                sp_ra_oa + sp_strketia + qty_dspnsd_num + days_suply_num + ptnt_pay_amt + 
                tot_rx_cst_amt

fit_glm1_time <- system.time(fit_glm1 <- glm(formula_glm1, 
                                             family=gaussian, data=cms_drug_patient, subset = (medreimb_ip > 1000)))
#summary(fit_glm1)
print_time("glm model", fit_glm1_time)


#----------------------
# Support vector machines
#----------------------
#library(e1071)

formula_svm <- (medreimb_ip + benres_ip + pppymt_ip) ~ age + bene_sex_ident_cd + race_white + 
                race_black + race_others + race_hispanic + sp_alzhdmta + sp_chf + sp_chrnkidn + 
                sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + sp_osteoprs +  
                sp_ra_oa + sp_strketia + qty_dspnsd_num + days_suply_num + ptnt_pay_amt + 
                tot_rx_cst_amt
#seq(0.1,5, by = 0.05)
#fit_svm_time <- system.time(fit_svm <- svm(formula_svm, 
#                                           data=cms_drug_patient, subset = (medreimb_ip > 1000)))

#print_time("svm model 1", fit_svm_time)


