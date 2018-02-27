""" 
Follow codes convert S-parameter file to time-domain pulse response 

Original creator: Kunmo Kim 
Date: 02/26/2018 
""" 

# how to install skrf: pip install scikit-rf 
import skrf as rf
import numpy as np
import matplotlib.pyplot as plt 

# Channel S-parameter can be downloaded from http://www.ieee802.org/3/100GCU/public/channel.html
sparam = rf.Network('/home/kunmok/Programming/Python/link_design/FCI_CC_Short_Link_Pair_1_to_Pair_9_Through.s4p')
#sparam = rf.Network('/home/kunmok/Programming/Python/link_design/FCI_CC_Long_Link_Pair_15_to_Pair_7_Through.s4p')

# calculate sdd21 
s21=sparam.s[:,1,0]
s43=sparam.s[:,3,2]
s23=sparam.s[:,1,2]
s41=sparam.s[:,3,0]
sdd21 = (s21 - s23 - s41 + s43)/2
sdd21_mag = np.abs(sdd21)
sdd21_ang = np.angle(sdd21)
freq=sparam.f    # freq range: 50 MHz to 15 GHz for the given channel
sdd21_db= 20*np.log10(sdd21_mag)
#sparam.plot_s_db(1,0)
#plt.plot(freq,sdd21_db)

# find the max frequency of current s-parameter file
flen=len(freq)
fstep = freq[1]-freq[0]
# how to calculate the max freq? freq[0] + fstep*(flen-1)
ftarget=1000E9   # extend max frequency to 500 GHz 
freq_new = np.arange(freq[0],ftarget+fstep,fstep)

# extrapolate to find DC value & approximate phase information 
# without below steps, pulse response shows undershoot in the beginning
extra_index=np.int(freq[0]/fstep)
sdd21_new = np.zeros(len(freq_new)+extra_index,dtype=np.complex_)
sdd21_new[extra_index:flen+extra_index]=sdd21
sdd21_new[0]=1+0j
# approximate phase information (phase extrapolation)
if extra_index > 1: 
    for i in range(1,extra_index):
        sdd21_new[i]=(sdd21[1]/sdd21[0])**i

# reverse the array
sdd21_new_reverse = np.conjugate(sdd21_new[::-1])
#sdd21_new_reverse = sdd21_new[::-1]

# below is effectively the same as 'fftshift'
sdd21_new2 = np.concatenate([sdd21_new,sdd21_new_reverse])

# to verify the results:
pulse_resp = np.fft.ifft(sdd21_new2)
plt.plot(np.real(pulse_resp[1:15000]))
fft_check= np.fft.fft(pulse_resp)
fft_check_sdd21=fft_check[0:1496]
#plt.plot(freq,20*np.log10(fft_check_sdd21),freq,sdd21_db)
#plt.plot(freq,np.angle(fft_check[0:1496]),freq,sdd21_ang)

