
getNewState <- function(probabilityMatrix){
  
  indices = arrayInd(sample(1:343,1,prob = probabilityMatrix),c(7,7,7))
  indices =indices - 1
  indices = isStateMoreThan6(indices)
  buildState(indices[1],indices[2],indices[3])
} 

getNewState(a)

#-----------------------------------------------
buildState <-function(small,medium,large){
  
  paste(toString(small),toString(medium),toString(large),sep = "_")  
  
}
#-----------------------------------------------
isStateMoreThan6<-function(indices){
  if(sum(indices)>6)
    indices = c(6,6,6)
  indices
  
}

#-----------------------------------------------   Get Real State based on 

getRealState <- function(smalls,mediums,largs){

  prob = calc_prob(smalls,mediums,largs)
  newState = getNewState(prob)
  newState
}

getRealState(1,3,5)

#-----------------------------------------------

getStates<-function(States){

      as.integer(unlist(strsplit(unlist(States), "_")))  
}

#------------------------------------------
getRemainingStates<-function(observedStates, realStates  ){
  
  polyps = getStates(realStates) - getStates(observedStates)
  polyps = isStateMoreThan6(polyps)
  buildState(polyps[1],polyps[2],polyps[3])
  
}

#---------------------------------------------
