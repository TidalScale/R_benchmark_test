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
  
  # The dataset contains 4 kinds of race.
  # 1. White
  # 2. Black
  # 3. Others
  # 5. Hispanic
  # create new columns for each race 
  
  # New column for white race
  patients$race_white <- 0 
  patients$race_white[patients$bene_race_cd == 1] <- 1
  
  # New column for black race
  patients$race_black <- 0 
  patients$race_black[patients$bene_race_cd == 2] <- 1
  
  # New column for others race
  patients$race_others <- 0 
  patients$race_others[patients$bene_race_cd == 3] <- 1
  
  # New column for hispanic race
  patients$race_hispanic <- 0 
  patients$race_hispanic[patients$bene_race_cd == 5] <- 1
  
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
