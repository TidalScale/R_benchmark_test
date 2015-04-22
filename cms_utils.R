# install.packages("ggplot2", dependencies = T)

# This function prints system time messages
print_time <- function(message, sys_time){
  print(paste0(message, " user time ", sys_time[1]))
  print(paste0(message," system time ", sys_time[2]))
  print(paste0(message," elapse time ", sys_time[3]))
  print(paste0(message," user child ", sys_time[4]))
  print(paste0(message," sys child ", sys_time[5]))
}
