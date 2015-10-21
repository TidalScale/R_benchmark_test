
print_time <- function(message, sys_time){
  # This function prints system time messages

  print(paste0(message, " user time ", sys_time[1]))
  print(paste0(message," system time ", sys_time[2]))
  print(paste0(message," elapse time ", sys_time[3]))
  print(paste0(message," user child ", sys_time[4]))
  print(paste0(message," sys child ", sys_time[5]))
}

print_mem_used <- function(message_print){
  # Gets and prints memory used.
  total_mem_used <- capture.output(mem_used())
  print(paste0(message_print, " ", total_mem_used))
}

print_value <- function(message, value){
  # Prints a message with value
  print(paste0(message, value))
}

set_cores <- function(){
  # Creates a cluster with available cores.

  # Find out how many cores are available
  cores <- detectCores()

  registerDoParallel(cores)
  return(cores)
}