setwd("C:/Users/salma/Desktop/State Simulation for CRC Data")
library(readr)
library(dplyr)
source("calc_prob.R")
source("getRealState.R")

paitent_State <- read_csv("./paitent_State.csv")


getRealStateFirstRow <- function(dt,...){
  
            states = getStates(dt[1,"State"])
            dt[1,"RealState"]= getRealState(states[1],states[2],states[3])
            #dt[1,"RemainingPolyps"] = getRemainingStates(dt[1,"State"],dt[1,"RealState"])
            dt
}


library(dplyr)
paitent_State <- paitent_State %>% 
                      group_by(patient_ID) %>% 
                      arrange(year, month) %>% 
                      group_modify(getRealStateFirstRow ) %>%
                      ungroup %>%
                      arrange(patient_ID)


write.csv(paitent_State,"./paitent_State1.csv", row.names = FALSE)



