# Clear the memory before running
rm(list= ls())

#options(echo=FALSE) # Hides R commands in output file
args <- commandArgs(trailingOnly = TRUE) # trailingOnly=TRUE means that only your arguments are returned
args_from <- as.numeric(args[1])   # Get cms sample start of range
args_to <- as.numeric(args[2])   # Get cms sample end of range
data_path <- args[3]   #Get cms data directory path
smoke_test <- toupper(args[4])  # Get smoke test parameter, it can contain logical values i.e. true or false

# Validate cms data directory path if it exists. Exit the program if the path does not exist
data_file_path <- file.path(data_path)
print(data_file_path)

#Raise error if cms data directory does not exist.
if(file.exists(data_file_path) == FALSE){
  q(save="no", status = 101)
}

# Load libraries and supress messages to get a clean output
load_libraries <- c("pryr","dplyr", "mgcv", "rpart", "randomForest", "FNN", "doParallel", "foreach")
a <- lapply(load_libraries, function(x) suppressMessages( library(x, character.only = T)))

# Allows to generate same random values each time.
set.seed(pi)

# Load supporting file for data analysis
source("cms_data_load.R")
source("cms_data_preprocess.R")
source("cms_utils.R")

#Set cms dataset path
setwd(data_file_path)
gc(F)     # Disable garbage collection before data load

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

years <- c(2008,2009,2010)
sample_id <-  test_sample     
claims_sample <- claims_sample  

# For loading data in parallel
cluster = set_cores()
print_value("Number of cores in use ", get_cores())

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

# Delete cluster
reset_cores(cluster)

print_time("load time", load_time)
# The size of data frame objects in memory that contain data for patient, inpatient, outpatient, carrier claims, and drug
df_size <- capture.output(object_size(patient, inpatient, outpatient, carrier_claims, drug))
print(paste0("size of individual data frame ", df_size))
print_mem_used("mem_used after data load")

#-----------------------------------------------------------------------
# Step 2: Data processing step
# Merge patient data with inpatient, outpatient, claims, and drug data.
#-----------------------------------------------------------------------

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

# Get beneficiary summary and prescription drugs data, of patients who were admitted to the hospital atleast once.
join_time <- join_time + system.time(tree_inpatient_drug <- get_inpatient_drugs_data(cms_inpatient, drug))

print_time("join time", join_time)
# Print object size after merging patient data with inpatient, outpatient, carrier claims, and drugs
join_df_size <- capture.output(object_size(cms_inpatient, cms_outpatient, cms_claims_patient, cms_drug_patient, units = "GB"))
print(paste0("size of data frame after join ", join_df_size))
print_mem_used("mem_used after data join")

# Do garbage collection before executing data analytics
gc(T)

#-----------------------------------------------
# Step 3: Analyze data 
#         Create models and find best fit.
#-----------------------------------------------
# Formula for patient demographic which includes age and gender

# Formula for to predict total inpatient expenses. 
# It includes patient demographic, chronic condition, and prescription drug covariates.
# Patient demographics varibales includes age and gender

# Generalized additive modeling 2
formula_gam1 <- total_inpatient_expense ~ s(age) + bene_sex_ident_cd + sp_alzhdmta + 
              sp_chf + sp_chrnkidn + sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + 
              sp_osteoprs + sp_ra_oa + sp_strketia + s(qty_dspnsd_num) + s(days_suply_num) + 
              s(ptnt_pay_amt) + s(tot_rx_cst_amt)

fit_gam1_time <- system.time(fit_gam1 <- gam(formula_gam1, 
                              family=gaussian(link=identity), data=cms_drug_patient, subset = (medreimb_ip > 1000)))

print_time("gam model", fit_gam1_time)
print_mem_used("mem_used after executing gam model")

#-------------------------
# Genralized linear model
#-------------------------
# Formula for to predict total inpatient expenses. 
# It includes patient demographic, chronic condition, and prescription drug covariates.
# Patient demographics varibales includes age and gender.
formula_glm1 <- total_inpatient_expense ~ age + bene_sex_ident_cd + 
                sp_alzhdmta + sp_chf + sp_chrnkidn + sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + 
                sp_osteoprs + sp_ra_oa + sp_strketia + qty_dspnsd_num + days_suply_num + 
                ptnt_pay_amt + tot_rx_cst_amt

fit_glm1_time <- system.time(fit_glm1 <- glm(formula_glm1, 
                                             family=gaussian, data=cms_drug_patient))
print_time("glm model", fit_glm1_time)
print_mem_used("mem_used after executing glm model")

#------------------------
# Decision trees
#----------------------
# Predict response variable total inpatient expenses using beneficiary demographic, chronic condition, 
# and prescription drug as predictors.
formula_tree <- total_inpatient_expense ~ age + bene_sex_ident_cd + sp_alzhdmta + 
              sp_chf + sp_chrnkidn + sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + 
              sp_osteoprs + sp_ra_oa + sp_strketia + tot_quantity + tot_days_supply + 
              tot_patient_pay_amount + tot_drug_cost

fit_decision_tree_time <- numeric(length = 5)
fit_decision_tree_time <- rep(0., 5)

# Create decision tree with cross validation 10 and cp 0.002 for regression
fit_decision_tree_time <- system.time(fit_tree <- rpart( formula_tree, data = tree_inpatient_drug,  
                                      method = "anova",
                                      control = rpart.control(cp = 0.001, xval =10, maxdepth = 30)))

# Prune trees back to avoid overfitting the data
fit_decision_tree_time <- fit_decision_tree_time + 
                    system.time(fit_tree_prune <- prune(fit_tree, cp=fit_tree$cptable[which.min(fit_tree$cptable[,"xerror"]), "CP"]))
print_time("decision trees", fit_decision_tree_time)
print_mem_used("mem_used after executing decision trees model")

#---------------------------
# Random forest
#---------------------------
formula_rf <- total_inpatient_expense ~ age + bene_sex_ident_cd + sp_alzhdmta + 
  sp_chf + sp_chrnkidn + sp_cncr + sp_copd + sp_depressn + sp_diabetes + sp_ischmcht + 
  sp_osteoprs + sp_ra_oa + sp_strketia + tot_quantity + tot_days_supply + 
  tot_patient_pay_amount + tot_drug_cost

fit_random_trees_time <- numeric(length = 5)
fit_random_trees_time <- rep(0., 5)

# No. of trees for random forest, allows to grow n number of trees
rf_n <- 50
fit_random_trees_time <- system.time(fit_rf <- randomForest(formula_rf, data = tree_inpatient_drug, nodesize = 1, maxnodes = 10,
                                                           importance = T, ntree = rf_n))

print_time("random forest", fit_random_trees_time)
print_mem_used("mem_used after executing random forest model")

#---------------------------
# K - Nearest neighbours
#---------------------------
# Predict response variable total inpatient expenses using beneficiary demographic, chronic condition, 
# and prescription drug as predictors.
knn_cols <- c("total_inpatient_expense", "age", "bene_sex_ident_cd", "sp_alzhdmta", 
          "sp_chf", "sp_chrnkidn", "sp_cncr", "sp_copd", "sp_depressn", "sp_diabetes", "sp_ischmcht", 
          "sp_osteoprs", "sp_ra_oa", "sp_strketia", "tot_quantity", "tot_days_supply", 
            "tot_patient_pay_amount", "tot_drug_cost")

fit_knn_time <- numeric(length = 5)
fit_knn_time <- rep(0., 5)

# Using K-fold cross validation method with k = 10, we create training and test datasets
cv <- 10
n <- nrow(tree_inpatient_drug)
i_test <- which(1:n%%cv == 0)
train <- tree_inpatient_drug[-i_test , knn_cols]
test <- tree_inpatient_drug[i_test , knn_cols]
test_labels <- test[,1]

# K nearest neighbors for KNN
# k = 4. We take k as the square root of total number of rows/observation in training data
knn_k <- floor(sqrt( nrow(train))) 

# Impelements knn regression model to predit total inpatient expense.
fit_knn_time <- system.time( knn_test_pred <- knn.reg(train[, -1], test[, -1], 
                                                 train[, "total_inpatient_expense"], k = knn_k))
# Calculate regression error using euclidean distance
err <- sum((knn_test_pred$pred - test_labels)^2)

print_time("K nearest neighbors", fit_knn_time)
print_mem_used("mem_used after executing knn model")

# Graphs to get more insights into the data
# cms_data_graphs(patient)

