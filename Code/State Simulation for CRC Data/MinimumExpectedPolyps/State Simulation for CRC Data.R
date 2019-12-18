library(dplyr)





#-----------------------------------------------

updateStateForAllPaitents <-function(){
  
                    newStates = NULL
                    
                    for (i in 1:nrow(paitent_State)){  # paitent_State is the dataset
                      

                      
                      newState = updateState(indices[1],indices[2],indices[3])
                      
                      #print(paste0("i: ",toString(i)," state: ",toString(paitent_State[i,"State"])," newState: ",newState ))
                      #print("------------")
                      newStates = append(newStates,newState)
                    
                    }
                    newStates
}    

paitent_State["New-State"] <- updateStateForAllPaitents()


write.csv(paitent_State,"./paitent_State1.csv", row.names = FALSE)



