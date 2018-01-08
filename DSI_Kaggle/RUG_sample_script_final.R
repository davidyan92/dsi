#
# Authior: Garrett Teoh Hor Keong
# for RUG presentation "Using R in Kaggle Competition" on 25th Jan 2017
#
setwd("D:\\Kaggle\\BNP Paribas")

# load packages
library(readr);library(xgboost);library(dplyr);library(caret);library(binr);library(Matrix);library(MLmetrics)
library(ggplot2);options(scipen=10);set.seed(794);library(glmnet)

# special functions
# ------------------------------------------------------------------
# Make equal sized bins
binCode <- function(tmp, nbin) {
  a=bins(tmp,nbin,nbin)
  print(bins.merr(a$binct,nbin))
  return(.bincode(tmp,as.numeric(bins.getvals(a))))
}

# Make distribution plot for categorical/integer with bin resp
plot.cat.dist <- function(feature,y,flag=0.1) {
  tmp=table(feature,y)
  ydist=sum(y)/length(y)
  plot.col=rep("grey",nrow(tmp))
  freq=tmp[,2]/apply(tmp,1,sum)
  plot.col[which((freq-ydist)>=flag)]="red"
  plot.col[which((ydist-freq)>=flag)]="blue"
  barplot(freq,main=paste("threshold = +/-",flag,sep=''),names.arg=paste(rownames(tmp),"(",apply(tmp,1,sum),")",sep=''),col=plot.col)
  abline(h=ydist, lty=2)
}

# ------------------------------------------------------------------
# reading input files downloaded from Kaggle
tr=data.frame(read_csv("./data/train.csv"));te=data.frame(read_csv("./data/test.csv"))
sub=data.frame(read_csv("./data/sample_submission.csv"))

cat("\nDimensions of Train: ",dim(tr));cat("\nDimensions of Test: ",dim(te))

# make features set list
features=intersect(colnames(tr),colnames(te));features=features[-1]
features

# store target as y, train and test set IDs
y=tr$target;tr.id=tr$ID;te.id=te$ID

# ------------------------------------------------------------------
# Features exploration

# combine train and test set data for features exploration/summary
dat=rbind(tr[,features],te[,features]);rm(tr,te);dat$ID=NULL;gc()

# replace NA by flag
NA.flag=-1
dat[is.na(dat)]=NA.flag

# check data type and uniqueness
class.type=NULL;n_uniq=NULL
for (i in 1:length(features)) {
  class.type[i]=class(dat[,i])
  n_uniq[i]=n_distinct(dat[,i])
}
cat("\nTypes of Features: ");table(class.type)

# create features list for character, numerical, integer
cat.feat=features[class.type=="character"]
int.feat=features[class.type=="integer"]
num.feat=features[class.type=="numeric"]

# run summary stats on all numerical/integer features
num.feat.summary=NULL
for (f in num.feat) {num.feat.summary=rbind(num.feat.summary,summary(dat[,f]))}
rownames(num.feat.summary)=num.feat
int.feat.summary=NULL
for (f in int.feat) {int.feat.summary=rbind(int.feat.summary,summary(dat[,f]))}
rownames(int.feat.summary)=int.feat

int.feat.summary;num.feat.summary[1:10,]

# ------------------------------------------------------------------
# Caret NZV run
feat.info=nearZeroVar(dat,saveMetrics=T)
feat.info=data.frame(read_csv("feat.csv"))
feat.info=data.frame(feat.info,class.type,n_uniq);feat.info[1:10,]

feat.info[feat.info$zeroVar,]
feat.info[feat.info$nzv,]

feat.info[feat.info$class.feat=="character",]

# plot proportion of each category, separated by y
f="v47" #v74,v38,v47
plot.cat.dist(dat[1:length(y),f],y,flag = 0.2)

# ------------------------------------------------------------------
# create a GGPLOT2 histogram on variable distributions given y
plot.feat="v50"     #v14, v50
tmp=data.frame('y'=as.factor(y),plot.feat=dat[1:length(y),plot.feat])
m=ggplot(tmp,aes(x=plot.feat))+geom_histogram((aes(fill=y)),binwidth=0.05);m

# ------------------------------------------------------------------
# Features Engineering

# create a (total sum of NA) feature
dat$sumNA=apply(dat,1,function(x) {length(which(x==NA.flag))})
int.feat=c(int.feat,"sumNA")

# ------------------------------------------------------------------
# Splitting back to tr and te set, clean up environmental garbages
# changing categorical features to factors
tmp=dat
for (f in cat.feat) {tmp[,f]=as.factor(tmp[,f])}

# split dataset into train/test
tr=tmp[1:length(y),];te=tmp[(length(y)+1):nrow(tmp),]
rm(list=setdiff(ls(),c("dat","y","te.id","tr.id","sub","tr","te","feat.info","plot.cat.dist","binCode")));gc()

# ------------------------------------------------------------------
# Building basic raw 3 models 

# regression based model
# alpha=1 for lasso and alpha=0 for ridge, or adjust alpha for L1/L2 regularization
glmmod=glmnet(x = data.matrix(tr),y,alpha=0.5,family="binomial")
glmpred=predict(glmmod,s=0.001,data.matrix(te),type="response")

# random forest model
library(rpart)
rfmod=rpart(y~.,data=data.frame(y,tr),method="class",control=rpart.control(minsplit=8,cp=0.001,maxsurrogate=0)) 
rfpred=predict(rfmod,data.frame(te),type = "prob")

# xgb model
param=list(objective="binary:logistic",booster="gbtree",eval_metric="auc",eta=0.3)
dtrain=xgb.DMatrix(data.matrix(tr),label=y)
xgbmod=xgb.train(data=dtrain,params=param,nrounds=200,maximize=T,verbose=1,watchlist=list(val=dtrain))
xgb.impt=xgb.importance(feature_names=colnames(tr),model=xgbmod)
xgb.plot.importance(xgb.impt[1:30,])
feat.info=data.frame(feat.info,xgb.impt[match(rownames(feat.info),xgb.impt$Feature),])
feat.info=feat.info[order(feat.info$Gain,decreasing=T),];feat.info[1:10,]
xgbpred=predict(xgbmod,data.matrix(te))

# check prediction probabilities for all 3 models
tmp=data.frame(model=rep(c("rf","xgb","glm"),each=nrow(sub)),prob=c(as.numeric(rfpred[,2]),as.numeric(xgbpred),as.numeric(glmpred[,1])))
m=ggplot(tmp,aes(x=prob))+geom_histogram((aes(fill=model)),binwidth=0.001)+ylim(0,1500);m

# ------------------------------------------------------------------
# Make submissions (raw)

cat("Submission ID matched test set ID:",sum(te.id==sub$ID),"\nNumber of Sub rows:",nrow(sub))
write_csv(data.frame('ID'=sub$ID,'PredictedProb'=glmpred[,1]),"glm-pred-raw.csv") 
write_csv(data.frame('ID'=sub$ID,'PredictedProb'=rfpred[,2]),"rf-pred-raw.csv") 
write_csv(data.frame('ID'=sub$ID,'PredictedProb'=xgbpred),"xgb-pred-raw.csv") 

# Dark art example (weighted averaging)
write_csv(data.frame('ID'=sub$ID,'PredictedProb'=0.53*xgbpred+0.38*glmpred[,1]+0.09*rfpred[,2]),"blended-sub-raw.csv")

# ------------------------------------------------------------------
# Performing a CV with xgboost

#auc or logloss
param=list(objective="binary:logistic",booster="gbtree",eval_metric="logloss",eta=0.3) 
dtrain=xgb.DMatrix(data.matrix(tr),label=y)

# cv=3, # cv=7, # cv=10,
xgb.cv(params=param,data=dtrain,nrounds=500,watchlist=list(val=dtrain),nfold=10)

# ------------------------------------------------------------------
# Features Engineering (basic)

# one hot encoding
one.hot.names=rownames(feat.info)[which(feat.info$class.type=="character")]
one.hot.names=c(one.hot.names,"sumNA")
one.hot.names=one.hot.names[-which(one.hot.names=="v22")]
onehot.fr=sparse.model.matrix(~.-1,data=dat[,one.hot.names])

# binarized important variables
bin.fr=NULL
bin.fr$v50.binCode=binCode(dat$v50,50)#80)
bin.fr$v12.binCode=binCode(dat$v12,50)#46)
bin.fr$v10.binCode=binCode(dat$v10,50)#73)
bin.fr$v14.binCode=binCode(dat$v14,50)
bin.fr$v114.binCode=binCode(dat$v114,50)

# make train and test set again with engineered features
tmp=data.frame(dat[,-which(colnames(dat)%in%one.hot.names)],as.matrix(onehot.fr),bin.fr)
tmp=tmp[,-which(colnames(tmp)=="v22")]
tr=tmp[1:length(y),];te=tmp[(length(y)+1):nrow(tmp),]

# get a glimpse of current model accuracy by cv=3
dtrain=xgb.DMatrix(data.matrix(tr),label=y)
xgb.cv(params=param,data=dtrain,nrounds=500,watchlist=list(val=dtrain),nfold=3)

# make a prediction and test ranking

# make a submission to test effect of simple features engineering
xgbmod=xgb.train(data=dtrain,params=param,nrounds=50,maximize=T,verbose=1,watchlist=list(val=dtrain))
xgbpred=predict(xgbmod,data.matrix(te))
write_csv(data.frame('ID'=sub$ID,'PredictedProb'=xgbpred),"xgb-pred-simple-FR.csv") 

# examine the importance of new features
xgb.impt=xgb.importance(feature_names=colnames(tr),model=xgbmod)
xgb.plot.importance(xgb.impt[1:30,])

# ------------------------------------------------------------------
# Tuning model (properly tuned)

param=list(objective="binary:logistic"
          ,booster="gbtree"
          ,eval_metric="logloss"
          ,subsample=0.80
          ,colsample_bytree=0.60
          ,max_depth=10
          ,gamma=1.076
          ,min_child_weight=5
          ,base_score=0.55
          #,alpha=0.1
          ,eta=0.01)
#xgb.cv(params=param,data=dtrain,nrounds=2000,watchlist=list(val=dtrain),nfold=3)

# With early stopping (proportion of stopping samples = 5%)
h=sample(1:nrow(tr),0.05*nrow(tr)) #same as: h=createDataPartition(y=y,p=0.05),length(h$Resample1)
dtrain=xgb.DMatrix(data.matrix(tr[-h,]),label=y[-h])
dtest=xgb.DMatrix(data.matrix(tr[h,]),label=y[h])
earlystopxgb.mod=xgb.train(params=param,data=dtrain,nrounds=10000,watchlist=list(val=dtest),early.stop.round=10)
xgbpred=predict(earlystopxgb.mod,xgb.DMatrix(data.matrix(te)),ntreelimit=earlystopxgb.mod$bestInd)
write_csv(data.frame('ID'=sub$ID,'PredictedProb'=xgbpred),"xgb-pred-simple-FR-tuned-early10.csv")

# ------------------------------------------------------------------
# Ensemble - Dark Art, simple averaging over 3 CV

#creating 3 subs of slightly differing params - colsample
colsam=c(0.4,0.6,0.8)
eta=c(0.01,0.05,0.1)
md=c(4,6,8)
enspred=rep(0,nrow(sub))
for (i in 1:3) {
  param=list(objective="binary:logistic"
          ,booster="gbtree"
          ,eval_metric="logloss"
          ,subsample=0.80
          ,colsample_bytree=colsam[i]
          ,max_depth=md[i]
          ,gamma=1.076
          ,min_child_weight=5
          ,base_score=0.55
          ,alpha=0.1
          ,eta=eta[i])
  h=sample(1:nrow(tr),0.05*nrow(tr))
  dtrain=xgb.DMatrix(data.matrix(tr[-h,]),label=y[-h])
  dtest=xgb.DMatrix(data.matrix(tr[h,]),label=y[h])
  earlystopxgb.mod=xgb.train(params=param,data=dtrain,nrounds=10000,watchlist=list(val=dtest),early.stop.round=10)
  xgbpred=predict(earlystopxgb.mod,xgb.DMatrix(data.matrix(te)),ntreelimit=earlystopxgb.mod$bestInd)
  enspred=enspred+xgbpred
}

write_csv(data.frame('ID'=sub$ID,'PredictedProb'=enspred/3),"xgb-pred-simple-FR-tuned-early10-ens-avg3.csv")

