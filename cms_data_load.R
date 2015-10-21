# Contains methods for loading data from csv files 

get_data_read_csv <- function(file_name_template, samples, smoke_test){
  # Gets data from csv files for samples
  
  # Get a list of file names
  file_names <- get_file_names(file_name_template, samples)
  
  # Load files in parallel using all available cores and export functions required for foreach loop execution
  df <- foreach(file_name = file_names, .combine = rbind, .export=c("file_exists", "load_data")) %do% {
      if(file_exists( file_name = file_name)){
          # Keep the character columns as charaters, avoid coercing to factors.
          df <- load_data(data_file_name = file_name, smoke_test = smoke_test)
          df
      }
  } 
  #df <- na.omit(df)     # Remove incomplete rows with NAs and null values
  # Convert the column names to lower case for easier data manipulation
  names(df) <- tolower(names(df))
  return(df)
}

get_data_read_csv_patients <- function(file_name_template, samples, years){
  # Gets data from csv files for patients for samples
  
  # Load patient data in parallel and export functions and packages to the execution environment
  df <- foreach(sample = samples, .combine = rbind, .export=c("file_exists", "load_data"), 
                .packages=c("doParallel")) %do% {
            foreach(year = years, .combine = rbind) %do% {
                str_file_name <- sprintf(file_name_template, year, sample) 
                data_file_name <- str_file_name
                
                if(file_exists(file_name = data_file_name)){                
                    # Keep the character columns as charaters, avoid coercing to factors.
                    p_df <- load_data(data_file_name = data_file_name)
                    p_df$YEAR <- year
                    p_df
                }
            }
        }
  # Convert the column names to lower case for easier data manipulation
  names(df) <- tolower(names(df))
  return(df)
}

load_data <- function(data_file_name, smoke_test = FALSE){
  # Reads data from CSV files.
  
  # For smoke test:
  # 1,800,000 rows uses 3.51 GB memory at max and takes 296.918 seconds to execute
  # 2,000,000 rows uses 4.20 GB memory at max and takes 323.974 seconds to execute
  # 2,000,000 rows uses 4.84 GB memory at max and takes 344.037 seconds/5.73 minutes to execute
  if(smoke_test == TRUE & length(grep("carrier_claims|Prescription_Drug", data_file_name, ignore.case = TRUE)) == 1){
      data <- read.csv( file = data_file_name, header = T, stringsAsFactors = F, nrow=2150000)
  } else{
      data <- read.csv( file = data_file_name, header = T, stringsAsFactors = F) 
  }
  
  return(data)
}


file_exists <- function(file_name){
  # Verifies whether a file exist, else raises an error
  
  result = FALSE
  
  if(file.exists(file_name) == FALSE){
    result = FALSE
    stop(cat("File not found!", file_name))
    q(save="no", status = 101)
  }
  else
    result = TRUE
  return(result)
}

get_file_names <- function(file_name_template, samples){
  # Creates a list of file names
  
  file_names <- foreach(sample = samples, .combine=c) %dopar% {
      str_file_name <- sprintf(file_name_template, sample) 
      data_file_name <- str_file_name
      data_file_name
  }
  return(file_names)
}
