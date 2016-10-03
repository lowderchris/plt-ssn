import pandas
import os
import brewer2mpl
import matplotlib
from matplotlib import pyplot

# Define a color palatte for later use
cols = (brewer2mpl.get_map('RdBu', 'Diverging', 11)).mpl_colors

# Grab current sunspot number data from the SILSO dataset
os.system('curl -O http://sidc.oma.be/silso/DATA/SN_m_tot_V2.0.txt')
os.system('curl -O http://sidc.oma.be/silso/DATA/SN_m_hem_V2.0.txt')
os.system('curl -O http://sidc.oma.be/silso/FORECASTS/KFprediCM.txt')

# Define column headers, and read in the data!
dcols = ['yy', 'mm', 't', 'tsn', 'snsd', 'nobs', 'def']
dcolsh = ['yy', 'mm', 't', 'tsn', 'nsn', 'ssn', 'mmsd', 'mmsdn', 'mmsds', 'nobs', 'nobsn', 'nobss']

d = pandas.read_csv('SN_m_tot_V2.0.txt', sep='\s+',header=None, names=dcols)
dh = pandas.read_csv('SN_m_hem_V2.0.txt', sep='\s+',header=None, names=dcolsh)

## Toggle keynote mode on and off
#keynote_figs()

#####
# Plot the entire range of sunspot data

# Generate a figure
f1, (ax0) = pyplot.subplots(1, figsize=[10,5])

# Plot full range of historical sunspot number data
ax0.plot(d['t'], d['tsn'], 'k', label='Total')

# Plot hemispheric sunspot number
ax0.plot(dh['t'], dh['nsn'], color=cols[2], label='Northern hemisphere')
ax0.plot(dh['t'], dh['ssn'], color=cols[8], label='Southern hemisphere')

# Tidy up the plot ranges, and label
ax0.set_ylim([0,420])
ax0.set_xlim([1740,2020])
ax0.legend()
ax0.set_xlabel('Year')
ax0.set_ylabel('Sunspot number')

# Save figures to disk
pyplot.savefig('ssn_full.pdf')
pyplot.savefig('ssn_full.png', transparent='True')

#####
# Plot the range of hemispheric sunspot data

# Generate a figure
f2, (ax0) = pyplot.subplots(1, figsize=[10,5])

# Plot hemispheric sunspot number
ax0.plot(dh['t'], dh['nsn'], color=cols[2], label='Northern hemisphere')
ax0.plot(dh['t'], dh['ssn'], color=cols[8], label='Southern hemisphere')

# Fill between to indicate dominant hemisphere
ax0.fill_between(dh['t'], dh['nsn'], dh['ssn'], where=dh['nsn']>dh['ssn'], facecolor=cols[2], interpolate=True)
ax0.fill_between(dh['t'], dh['nsn'], dh['ssn'], where=dh['ssn']>dh['nsn'], facecolor=cols[8], interpolate=True)

# Tidy up the plot ranges, and label
ax0.set_ylim([0,150])
ax0.set_xlim([1991,2016])
ax0.legend()
ax0.set_xlabel('Year')
ax0.set_ylabel('Sunspot number')

# Save figures to disk
pyplot.savefig('ssn_hemi.pdf')
pyplot.savefig('ssn_hemi.png', transparent='True')

#####
# Plot the range of hemispheric sunspot data, on a smaller scale

# Generate a figure
f3, (ax0) = pyplot.subplots(1, figsize=[5,2.5])

# Plot hemispheric sunspot number
ax0.plot(dh['t'], dh['nsn'], color=cols[2], label='Northern hemisphere')
ax0.plot(dh['t'], dh['ssn'], color=cols[8], label='Southern hemisphere')

# Fill between to indicate dominant hemisphere
ax0.fill_between(dh['t'], dh['nsn'], dh['ssn'], where=dh['nsn']>dh['ssn'], facecolor=cols[2], interpolate=True)
ax0.fill_between(dh['t'], dh['nsn'], dh['ssn'], where=dh['ssn']>dh['nsn'], facecolor=cols[8], interpolate=True)

# Tidy up the plot ranges, and label
ax0.set_ylim([0,150])
ax0.set_xlim([1991,2016])
ax0.set_xlabel('Year')
ax0.set_ylabel('Sunspot number')

# Save figures to disk
pyplot.savefig('ssn_hemi_sm.pdf')
pyplot.savefig('ssn_hemi_sm.png', transparent='True')
