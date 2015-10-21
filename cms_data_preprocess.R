options(warn=F)

data_pre_process <- function(patients){
  # Uses existing patient data to extract new columns and transform existing data for data analysis purposes.
  #
  # Args:
  # patients: Medicare patient data 
  #
  # Returns:
  # Patient data with new columns for age and race and data transformation on gender and chronic diseases.
  
  # Convert date of birth from integer type to date type
  patients$bene_birth_dt <- as.character(patients$bene_birth_dt)
  patients$bene_birth_dt <- as.Date(patients$bene_birth_dt, "%Y%m%d")
  
  # Graph
  # hist( patients$bene_birth_dt, breaks = "years", freq = T) 
  # Conclusion: The distribution of date of birth is skewed to the right
  
  # Convert date of death from integer type to date type
  patients$bene_death_dt <- as.character(patients$bene_death_dt)
  patients$bene_death_dt[(is.na(patients$bene_death_dt))] <- format(Sys.Date(), "%Y%m%d")
  patients$bene_death_dt <- as.Date(patients$bene_death_dt, "%Y%m%d")
  
  # Calculate patient age
  patients$age <- as.numeric(format(patients$bene_death_dt, "%Y")) - 
    as.numeric(format(patients$bene_birth_dt, "%Y"))
  # hist(patients$age, breaks = 20, freq = T)
  
  # In the next step convert gender to 0 and 1
  # In the beneficiary summary dataset the gender are: 
  # 1. Male
  # 2. Female
  
  # 1 Male convert to 0
  # 2 Female convert to 1
  patients$bene_sex_ident_cd[patients$bene_sex_ident_cd == 1] <- 0
  patients$bene_sex_ident_cd[patients$bene_sex_ident_cd == 2] <- 1
  
  # The dataset contains numeric value for diseases as follows:
  # 1. Yes
  # 2. No
  
  # We convert the values to represet 0 and 1
  # 0. No
  # 1. Yes
  
  # So we only convert the value 2 to 0 to represent No.
  patients$sp_alzhdmta[patients$sp_alzhdmta == 2] <- 0
  patients$sp_chf[patients$sp_chf == 2] <- 0
  patients$sp_chrnkidn[patients$sp_chrnkidn == 2] <- 0
  patients$sp_cncr[patients$sp_cncr == 2] <- 0
  patients$sp_copd[patients$sp_copd == 2] <- 0
  patients$sp_depressn[patients$sp_depressn == 2] <- 0
  patients$sp_diabetes[patients$sp_diabetes == 2] <- 0
  patients$sp_ischmcht[patients$sp_ischmcht == 2] <- 0
  patients$sp_osteoprs[patients$sp_osteoprs == 2] <- 0
  patients$sp_ra_oa[patients$sp_ra_oa == 2] <- 0
  patients$sp_strketia[patients$sp_strketia == 2] <- 0
  patients$total_inpatient_expense <- patients$medreimb_ip + 
                                      patients$benres_ip + 
                                      patients$pppymt_ip
  return(patients)
}

add_year <- function(data, col_name){
  # Creates a new variable for year using an existing date variable
  # 
  # Args:
  #   data: A data frame with at least 1 date column 
  #   col_name: Name of the date column
  # 
  # Returns:
  # A data frame with a new column for year
  
  data$year <- as.numeric(substr(as.character(data[, which(names(data) == col_name)]),1,4))
  return(data)
}

get_inpatient_drugs_data <- function(cms_inpatient, drug){
  # Get beneficiaries and prescription drug data, for patients who were admitted to the hospital atleast once. 
  # In technical terms, get patients who have atleast 1 inpatient record in inpatient data
  #
  # Args:
  # This function requires patient, inpatient and prescription drug event data.
  #
  # Returns:
  # A single data frame which contains beneficiary summary and prescription drugs data, 
  # for patients who were admitted to hostpital atleast once.
  
  inpatient_exp <- cms_inpatient  #  patient[patient$desynpuf_id %in% inpatient$desynpuf_id && patient$year == inpatient$year,]
  
  # Get summary of prescription drugs for each beneficiary
  drug_summary <- data.frame()
  drug_summary <- drug %>% group_by(desynpuf_id, year) %>% 
    summarise(tot_quantity = sum(qty_dspnsd_num), tot_days_supply = sum(days_suply_num),
              tot_patient_pay_amount = sum(ptnt_pay_amt), tot_drug_cost = sum(tot_rx_cst_amt))
  
  # Combine patient data, who have 1 inpatient record, with prescription drug summary
  inpatient_drug <- left_join(inpatient_exp, drug_summary, by = c("desynpuf_id", "year"))
  
  # Data pre-processing to handle NA values introduced by left join
  inpatient_drug[is.na(inpatient_drug$tot_quantity),"tot_quantity"] <- 0
  inpatient_drug[is.na(inpatient_drug$tot_days_supply),"tot_days_supply"] <- 0
  inpatient_drug[is.na(inpatient_drug$tot_patient_pay_amount), "tot_patient_pay_amount"] <- 0
  inpatient_drug[is.na(inpatient_drug$tot_drug_cost), "tot_drug_cost"] <- 0
  
  return(inpatient_drug)
}

cms_data_graphs <- function(patient){
  # Create graphs to give more insights into cms data
  #
  # Args:Patient data with age and total inpatient expense
  #
  # Return: Outputs grpahs in PDF file
  
  #----
  # plots
  #---
  library(ggplot2)
  #pdf("cms_data_graphs.pdf")
  cms_plots <- vector(length = 11)
  cms_plots[1] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_alzhdmta) + geom_point()
  cms_plots[2] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_ischmcht) + geom_point()
  cms_plots[3] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_diabetes) + geom_point()
  cms_plots[4] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_chrnkidn) + geom_point()
  cms_plots[5] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_cncr) + geom_point()
  cms_plots[6] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_chf) + geom_point()
  cms_plots[7] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_copd) + geom_point()
  cms_plots[8] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_depressn) + geom_point()
  cms_plots[9] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_osteoprs) + geom_point()
  cms_plots[10] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_ra_oa) + geom_point()
  cms_plots[11] <- ggplot(patient) + aes(x = age, y = total_inpatient_expense, color = sp_strketia) + geom_point()
  
  #dev.off()
}