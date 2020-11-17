args <- commandArgs(TRUE)
filename<-args[1]


# load sample ARG table
argtable1 <- read.table(filename,sep='\t', header=T,row.names=1,check=F,comment='')
argtable2 <- as.data.frame(t(argtable1))
argtable <- ceiling(1000000*argtable2)

# load SourceTracker package
source('/home/lg209ws3/argoap_18.05/galaxy/tools/MST/SourceTracker_LLG.r')
st_20170401<-readRDS(file="/home/lg209ws3/argoap_18.05/galaxy/tools/MST/st_20170401.RData")


# Estimate source proportions in test data
results <- predict(st_20170401,argtable, alpha1=0.001, alpha2=0.001)

# Value: A list containing:
# draws - an array of dimension (ndraws X nenvironments X nsamples),
#     containing all draws from gibbs sampling （吉布斯采样）
# proportions - the mean proportions over all Gibbs draws for each sample
# proportions_sd - standard deviation of the mean proportions for each sample
# train.envs - the names of the source environments
# samplenames - the names of the test samples

### add by YXL
write.table(results$proportions,file=paste(filename,"source_proportions.txt",sep="."),quote=F,sep="\t",row.names=T,col.names=T)
write.table(results$proportions_sd,file=paste(filename,"source_proportions_sd.txt",sep="."),quote=F,sep="\t",row.names=T,col.names=T)

