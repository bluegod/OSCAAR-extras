import numpy as np
from matplotlib import pyplot as plt
import oscaar
from scipy import optimize
from numpy.random import shuffle
import transiterFit
from oscaar.extras.knownSystemParameters import returnSystemParams

#Load in the data from OSCAAR output. 
#sampleData = oscaar.load('sampleOutput/oscaarDataBase.pkl')
#NormFlux=sampleData.lightCurve
#timeObs=sampleData.times
#flux_error=sampleData.lightCurveError

#Get parameters from exoplanet.org to use as initial guesses. 
#planet = 'GJ 1214 b'
#[p,ap,P,P_err,inc,ecc] = returnSystemParams.transiterParams(planet)
#gamma1,gamma2 = ???

#Planetary Parameters to create fake data. 
fk_RpRs=0.122
fk_aRs=12.7
fk_per=1.58
fk_inc=89.5
fk_t0=2454344.30867
fk_gam1=0.23
fk_gam2=0.30
fk_ecc=0.0
fk_argper=0.0
stddev=0.0005 #Standard Deviation of data. 

#Creating fake dataset, including flux, time, and uncertainty
timeObs,NormFlux=transiterFit.fake_data(stddev,fk_RpRs,fk_aRs,fk_per,fk_inc,fk_t0,fk_gam1,fk_gam2,fk_ecc,fk_argper)
flux_error=stddev*np.ones(np.size(timeObs))

#Initial Guess for Planetary Parameters by pulling them from the exoplanet website.
#For this example we're using GJ 1214 b
RpOverRs= 0.117
aOverRs = 13.0
inclination = 89.6
epoch = 2454344.30767
gamma1 = 0.22
gamma2 = 0.40
period = 1.58
eccentricity = 0.0
longPericenter = 0.0

#RpOverRs = returnSystemParams.exoplanetDB[planet]['PER']
#aOverRs =  ap #returnSystemParams.exoplanetDB[planet]['PER']

#Run the intial fit with input parameters stated above. 
fit,success = transiterFit.run_LMfit(timeObs,NormFlux,flux_error,RpOverRs,aOverRs,inclination,epoch,
                                     gamma1,gamma2,period,eccentricity,longPericenter,
                                     fitLimbDark='quadratic',
                                     plotting=True)

#Run MC fit to estimate uncertainty
n_iter = 1000 #Number of random datasets to fit to. 
transiterFit.run_MCfit(n_iter,timeObs,NormFlux,flux_error,fit,success,
                       period,eccentricity,longPericenter,plotting=True)

