
spec = 0.86
sens = c(0.75,0.85,0.95)   ### sensitivity for small, medium, large polyps
prob_s = c(0,0,0,0,0,0,0)
prob_m = c(0,0,0,0,0,0,0)
prob_l = c(0,0,0,0,0,0,0)
prob = array(0,c(7,7,7))
calc_prob <- function(ns, nm, nl){
  l_ns = 6#-ns +1
  l_nm = 6#-nm +1 
  l_nl = 6#-nl +1
  if (ns > 0){              
    for (i in ns:(l_ns)){   
      
      prob_s [i+1] = dbinom(i-ns,i, 1- sens[1]) # dbinom(i-2,i, 0.25)
    }
  }else{
    prob_s[1] = spec
    for (i in 1:l_ns){
      prob_s [i+1] = dbinom(i,i, 1- sens[1])
    } 
  }
  #print(prob_s)
  
  if (nm > 0){
    for (i in nm:(l_nm)){
      prob_m [i+1] = dbinom(i-nm,i, 1- sens[2])
    }
  }else{
    prob_m[1] = spec
    for (i in 1:l_nm){
      prob_m [i+1] = dbinom(i,i, 1- sens[2])
    } 
  }
  
  if (nl > 0){
    for (i in nm:(l_nl)){
      prob_l [i+1] = dbinom(i-nl,i, 1- sens[3])
    }
  }else{
    prob_l[1] = spec
    for (i in 1:l_nl){
      prob_l [i+1] = dbinom(i,i, 1- sens[3])
    } 
  }
  #prob_s = prob_s / sum(prob_s)
  #prob_m = prob_m / sum(prob_m)
  #prob_l = prob_l / sum(prob_l)
  for (i in 1:7){
    for (j in 1:7){
      for (k in 1:7){
        prob[i,j,k] = prob_s [i] * prob_m [j] * prob_l [k] 
      }
    }
  }
  prob = prob / sum(prob)
  return (prob)#, prob_s,prob_m,prob_l))
}

#a = calc_prob(3,3,3) ### a[i+1,j+1,k+1] give prob of being in state i,j,k
#calc_prob(0,1,0)