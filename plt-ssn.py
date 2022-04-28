import numpy as np
import pandas
import os
from datetime import datetime
import sunpy.coordinates
import palettable
import matplotlib
from matplotlib import pyplot

# Define a color palatte for later use
cols = palettable.colorbrewer.diverging.RdBu_11.mpl_colors

# Grab current sunspot number data from the SILSO dataset
os.system('curl -O https://wwwbis.sidc.be/silso/DATA/SN_m_tot_V2.0.txt')
os.system('curl -O https://wwwbis.sidc.be/silso/DATA/SN_m_hem_V2.0.txt')
os.system('curl -O https://wwwbis.sidc.be/silso/FORECASTS/KFprediCM.txt')

# Define column headers, and read in the data!
dcols = ['yy', 'mm', 't', 'tsn', 'snsd', 'nobs', 'def']
dcolsh = ['yy', 'mm', 't', 'tsn', 'nsn', 'ssn', 'mmsd', 'mmsdn', 'mmsds', 'nobs', 'nobsn', 'nobss', 'prov']
dcolsp = ['yy', 'mm', 't', 'junk', 'tsn', 'unc']

d = pandas.read_csv('SN_m_tot_V2.0.txt', sep='\s+',header=None, names=dcols)
dh = pandas.read_csv('SN_m_hem_V2.0.txt', sep='\s+',header=None, names=dcolsh)
dp = pandas.read_csv('KFprediCM.txt', sep='\s+', header=None, names=dcolsp)

# Generate some time arrays
td = []
for i in np.arange(len(d['yy'].values)) : td.append(datetime(d['yy'].values[i], d['mm'].values[i], 1))

tdh = []
for i in np.arange(len(dh['yy'].values)) : tdh.append(datetime(dh['yy'].values[i], dh['mm'].values[i], 1))

tdp = []
for i in np.arange(len(dp['yy'].values)) : tdp.append(datetime(dp['yy'].values[i], dp['mm'].values[i], 1))

# Generate an array of corresponding CR numbers
crd = sunpy.coordinates.sun.carrington_rotation_number(td)
crdh = sunpy.coordinates.sun.carrington_rotation_number(tdh)
crdp = sunpy.coordinates.sun.carrington_rotation_number(tdp)

## Toggle keynote mode on and off
keynote_figs()
lc = 'w'
# lc = 'k'

#####
# Plot the entire range of sunspot data

# Generate a figure
f1, (ax0) = pyplot.subplots(1, figsize=[10,4])

# Plot full range of historical sunspot number data
ax0.plot(d['t'], d['tsn'], lc, label='Total')

# Plot hemispheric sunspot number
ax0.plot(dh['t'], dh['nsn'], color=cols[2], label='Northern hemisphere')
ax0.plot(dh['t'], dh['ssn'], color=cols[8], label='Southern hemisphere')

# Tidy up the plot ranges, and label
ax0.set_ylim(0)
ax0a = ax0.twiny()
ax0a.set_xlim(crd[0], crd[-1])
ax0.legend()
ax0.set_xlabel('Date')
ax0a.set_xlabel('Carrington Rotation')
ax0.set_ylabel('Sunspot number')

pyplot.tight_layout()

# Save figures to disk
pyplot.savefig('ssn_full.pdf')
pyplot.savefig('ssn_full.png', transparent='True')

#####
# Plot the range of hemispheric sunspot data

# Generate a figure
f1, (ax0) = pyplot.subplots(1, figsize=[10,4])

# Plot hemispheric sunspot number
ax0.plot(dh['t'], dh['nsn'], color=cols[2], label='Northern hemisphere')
ax0.plot(dh['t'], dh['ssn'], color=cols[8], label='Southern hemisphere')

# Fill between to indicate dominant hemisphere
ax0.fill_between(dh['t'], dh['nsn'], dh['ssn'], where=dh['nsn']>dh['ssn'], facecolor=cols[2], interpolate=True)
ax0.fill_between(dh['t'], dh['nsn'], dh['ssn'], where=dh['ssn']>dh['nsn'], facecolor=cols[8], interpolate=True)

# Tidy up the plot ranges, and label
ax0.set_ylim(0)
ax0a = ax0.twiny()
ax0a.set_xlim(crdh[0], crdh[-1])
ax0.legend()
ax0.set_xlabel('Date')
ax0a.set_xlabel('Carrington Rotation')
ax0.set_ylabel('Sunspot number')

pyplot.tight_layout()

# Save figures to disk
pyplot.savefig('ssn_hemi.pdf')
pyplot.savefig('ssn_hemi.png', transparent='True')

#####
# Plot the past few cycles, and an outlook on the future...

# Generate a figure
f1, (ax0) = pyplot.subplots(1, figsize=[10,4])

# Plot full range of historical sunspot number data
ax0.plot(d['t'], d['tsn'], lc, label='Total')

ax0.fill_between(dp['t'], dp['tsn']+dp['unc'], dp['tsn']-dp['unc'], color=cols[6])
ax0.plot(dp['t'], dp['tsn'], color=cols[8], label='KF CM Pred.')

# Tidy up the plot ranges, and label
ax0a = ax0.twiny()
ax0a.set_xlim(crdh[0], crdh[-1])

ax0.legend()
ax0.set_xlabel('Date')
ax0.set_ylabel('Sunspot number')

pyplot.tight_layout()

# Save figures to disk
pyplot.savefig('ssn_pred.pdf')
pyplot.savefig('ssn_pred.png', transparent='True')
