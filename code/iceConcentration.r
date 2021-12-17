df<-read.csv('E:/MooredEchosounders/code/d1.csv')
df <- df[complete.cases(df),]
library(nlme)
library(mgcv)
library(dplyr)
df2 = distinct(df,julian,.keep_all=TRUE)
mod1<-gls(logsA ~ ice*julian, data=df2, correl = corCAR1(form = ~julian)) # whether I use the survey as cetegorical or continuous
summary(mod1)