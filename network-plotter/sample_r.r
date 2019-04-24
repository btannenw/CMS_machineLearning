source("http://bioconductor.org/biocLite.R")
install.packages('NeuralNetTools',repos = "http://cran.us.r-project.org")
#Add this if you need to install neural network tools ^

args <- commandArgs(TRUE)

input_weights_file <-args[1]
input_struct_file <-args[2]


library(NeuralNetTools)
#library(rhdf5)
data(neuraldat)

#source("lek.r")

#mydata <- h5read("myModel.hdf5","dense_37")
#print(h5ls("myModel.hdf5"))
#str(mydata)

library(nnet)


my_weights <- c(scan(input_weights_file,double(),sep=","))

struct <- c(scan(input_struct_file,integer(),sep=","))

x_names_in <- c("Mass","Momentum")
y_names_in <- c("Electron","Muon")

plotnet(my_weights,struct,x_names=x_names_in,y_names=y_names_in)

wts_in <- neuralweights(my_weights, struct = struct)
wts_struct <- wts_in$struct
wts_in <- wts_in$wts

for (out in y_names_in){
    print(out)
    olden(wts_in,x_names=x_names_in,y_names=y_names_in,out_var=out)
}
olden(wts_in,struct,x_names=x_names_in,y_names=y_names_in,out_var="Electron",y_lab="Electron Importance")
olden(wts_in,x_names=x_names_in,y_names=y_names_in,out_var="Muon",y_lab="Muon Importance")


#lekprofile(my_weights,matrix(c("A","B"),ncol=2,nrow=1))
