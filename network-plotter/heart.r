source("http://bioconductor.org/biocLite.R")
#install.packages('NeuralNetTools',repos = "http://cran.us.r-project.org")
#Add this if you need to install neural network tools ^

#install.packages('reshape',repos = "http://cran.us.r-project.org")
library(NeuralNetTools)
library(rhdf5)
library(neuralnet)
data_in<-read.csv("heartFix.csv");


library(nnet)
mod_in <- nnet(Disease ~ age + sex + cp + trestbps + chol + fbs + restecg + thalach + exang + oldpeak + slope + ca + thal, data_in,size=63,maxit=1000,decay=0.05)

#mod_in <- nnet(X1 + X2 + X3 + X4 + X5 + X6 + X7 + X8 + X9 + X10 + X11 + X12 + X13 ~ Y1,data = data_in,size=100)

olden(mod_in)

xvars<-c(c('age'),c('sex'),c("cp"),c("trestbps"),c("chol"),c("fbs"),c("restecg"),c("thalach"),c("exang"),c("oldpeak"),c("slope"),c("ca"),c("thal"))
for (x in xvars){
   lekprofile(mod_in,xsel=x,group_vals = seq(0,1,by=0.2),grp_nms = c('0.0','0.2','0.4','0.6','0.8','1.0'))
}

lekprofile(mod_in,xsel=c('age','chol'),group_vals = seq(0,1,by=0.2),grp_nms = c('0.0','\
0.2','0.4','0.6','0.8','1.0'))


lekprofile(mod_in,xsel=c('age'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('sex'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('cp'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('trestbps'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('chol'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('fbs'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('restecg'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('thalach'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('exang'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('oldpeak'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('slope'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('ca'),group_vals = c(0.5),grp_nms=c("0.5"))
lekprofile(mod_in,xsel=c('thal'),group_vals = c(0.5),grp_nms=c("0.5"))


