import skrf as rf
# how to install skrf: pip install scikit-rf 
import numpy as np
import matplotlib.pyplot as plt 

# get s-parameter file from local drive 
#sparam = rf.Network('snm_c_tu862_retimer.s4p')
sparam = rf.Network('/home/kunmok/Programming/Python/link_design/peters_01_0605_B1_thru.s4p')

# calculate sdd21 
s21=sparam.s[:,1,0]
s43=sparam.s[:,3,2]
s23=sparam.s[:,1,2]
s41=sparam.s[:,3,0]
sdd21 = (s21 - s23 - s41 + s43)/2
#sdd21_mag = np.abs(sdd21)
#sdd21_ang = np.angle(sdd21)
freq=sparam.f    # freq range: 50 MHz to 15 GHz for the given channel
#sdd21_db= 20*np.log10(sdd21_mag)
#sparam.plot_s_db(1,0)
#plt.plot(freq,sdd21_db)

# find the max frequency of current s-parameter file
flen=len(freq)
fstep = freq[1]-freq[0]
# how to calculate the max freq? freq[0] + fstep*(flen-1)
ftarget=500E9   # extend max frequency to 500 GHz 
freq_new =  np.arange(freq[0],ftarget+fstep,fstep)

sdd21_new = np.zeros(len(freq_new),dtype=np.complex_)
for x in range(0,len(sdd21_new)):
    if x < flen:
        sdd21_new[x] = sdd21[x]
                 
# reverse the array
sdd21_new_reverse = np.conjugate(sdd21_new[::-1])

# below is effectively the same as 'fftshift'
sdd21_new2 = np.concatenate([sdd21_new,sdd21_new_reverse])

# to verify the results:
pulse_resp = np.fft.ifft(sdd21_new2)
plt.plot(pulse_resp[1:4000])
fft_check= np.fft.fft(pulse_resp)
fft_check_sdd21=fft_check[0:1496]
#plt.plot(freq,20*np.log10(fft_check_sdd21),freq,sdd21_db)


