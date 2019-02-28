#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from scipy.stats import binned_statistic

datapath = 'bitcoin_crypto_economyUNION.csv'

data = pd.read_csv(datapath)


#%%

#plot out-degree as a function of in-degree

fig1=plt.figure()
ax1 = fig1.add_subplot(111)

ax1.plot(data['indegree'],data['outdegree'],'.')


#%%

#some mean values from previous plot

nbins=9
fig2=plt.figure()
ax2=fig2.add_subplot(111)
f,_,_ = binned_statistic(data["indegree"],data["outdegree"],statistic='mean',bins=nbins)
c,_,_ = binned_statistic(data["indegree"],data["indegree"],statistic='mean',bins=nbins)


ax2.scatter(c,f)

#%%

#Plot in-degree and out-degree distribution on loglog scale

nbins = 20
x=data["indegree"]
vali = np.array([1,max(x)])
logvali = np.log(vali)
logbins = np.logspace(np.log10(1),np.log10(max(x)),num=nbins)
bincenters,_,_ = binned_statistic(x,x,statistic='mean',bins=logbins)

hist = np.histogram(x,bins=logbins)
fig3 = plt.figure(figsize=(7,7))
ax3 = fig3.add_subplot(211)
ax3.loglog(bincenters,hist[0],'.')
ax3.set_xlabel('in-degree')
ax3.set_ylabel('frequency')

x=data["outdegree"]
vali = np.array([1,max(x)])
logvali = np.log(vali)
logbins = np.logspace(np.log10(1),np.log10(max(x)),num=nbins)
bincenters,_,_ = binned_statistic(x,x,statistic='mean',bins=logbins)

hist = np.histogram(x,bins=logbins)

ax32 = fig3.add_subplot(212)
ax32.loglog(bincenters,hist[0],'.')
ax32.set_xlabel('out-degree')
ax32.set_ylabel('frequency')
#fig3.savefig('in ja outdegree.pdf')


#%%

#Plot some centrality measures as a function of degree

fig5 = plt.figure(figsize=(7,7))
ax = fig5.add_subplot(111)
ax.plot(data['Degree'], data['closnesscentrality'],'.')
ax.set_xscale('log')
ax.plot(data['Degree'], data['betweenesscentrality']/max(data['betweenesscentrality']),'.')

ax.plot(data['Degree'], data['clustering'],'.')

ax.set_xlabel('degree')
ax.set_ylabel('centralty masure')
ax.legend(loc=0)

