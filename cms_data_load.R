#dir_path <- file.path("data", "cms_medicare")
#setwd(dir_path)


get_data_read_csv <- function(file_name_template, samples, smoke_test){
  df <- data.frame()
  
  for(sample in samples)
  {
    str_file_name <- sprintf(file_name_template, sample) 
    data_file_name <- str_file_name
    file_exists(data_file_name)
    
    # Keep the character columns as charaters, avoid coercing to factors.
    df <- rbind(df, load_data(data_file_name, smoke_test))
  }

  df <- na.omit(df)     # Remove incomplete rows with NAs and null values
  # Convert the column names to lower case for easier data manipulation
  names(df) <- tolower(names(df))
  return(df)
}


get_data_read_csv_patients <- function(file_name_template, samples, years){
  df <- data.frame()
  
  for(sample in samples)
  {
    for(year in years){
      
      str_file_name <- sprintf(file_name_template, year, sample) 
      data_file_name <- str_file_name
      file_exists(data_file_name)
      
      # Keep the character columns as charaters, avoid coercing to factors.
      p_df <- load_data(data_file_name)
      p_df$YEAR <- year
      df <- rbind(df, p_df)
    }
  }
  # Convert the column names to lower case for easier data manipulation
  names(df) <- tolower(names(df))
  return(df)
}

load_data <- function(data_file_name, smoke_test = FALSE){
  # 
  # 1,800,000 rows uses 3.51 GB memory at max and takes 296.918 seconds to execute
  # 2,000,000 rows uses 4.20 GB memory at max and takes 323.974 seconds to execute
  # 2,000,000 rows uses 4.84 GB memory at max and takes 344.037 seconds/5.73 minutes to execute
  if(smoke_test == TRUE & length(grep("carrier_claims|Prescription_Drug", data_file_name, ignore.case = TRUE)) == 1){
  data <- read.csv( file = data_file_name, header = T, stringsAsFactors = F, nrow=2150000)
  } else{
    print(paste0("Loading ",data_file_name))
    data <- read.csv( file = data_file_name, header = T, stringsAsFactors = F)
  }
  return(data)
}

# This method checks and raises error if a file does not exist
file_exists <- function(file_name){
  result = FALSE
  if(file.exists(file_name) == FALSE){
    result = FALSE
    q(save="no", status = 101)
  }
  else
    result = TRUE
  return(result)
}

