from cProfile import label
from tkinter import Label
import yaml
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random

with open("config.yml", 'r') as stream:
    config=yaml.safe_load(stream)
    print(config)

def gauss(v,m,s):
    return exp(-0.5*((v-m)/s)**2) #1/(s*sqrt(2*pi))*  # gaussian distribution

def gain_distrib(v):
    global config
    return eval(config['gain_distrib'])

fmin = config['fmin']
fgap = config['fgap']
modes = config['modes']
dispMax = min(modes,config['display_modes'])
c = 3e8
cavity_lenght = c/fgap

tmp = 0
while tmp < fmin or tmp == 0:
    tmp += fgap


v = arange(fmin, fmin+fgap*modes, fgap)
x = linspace(0, cavity_lenght,1000, endpoint=True)

periods = []
phases = []
amplitudes = []
tmax = 1

for i in arange(modes)+1:
    periods.append(v[i-1])#/i)#random())
    phases.append(random()*2*pi)
    amplitudes.append(1)#sqrt(i))
periods = array(periods)
amplitudes = array(amplitudes)
amplitudes = amplitudes/max(amplitudes)
phases = array(phases)

t = linspace(0,max(periods)*2,1000)

# waves definition
def wave(mod,x,t):
    return amplitudes[mod-1]                        \
        *sin(x/cavity_lenght*pi*mod)                \
        *cos(2*pi*t/periods[mod-1] + phases[mod-1])

# Init plot
fig, (ax1, ax2, ax3) = plt.subplots(3,1)


# ax1.vlines(x=v,ymin=0,ymax=amplitudes/max(amplitudes))
lines1 = []
for i in v: ax1.axvline(i, color='k', linestyle='--')
lines1.append(ax1.plot(  v,  gain_distrib(v) /max(gain_distrib(v)),  c='0.55',  label=f"Laser gain (*{round(max(gain_distrib(v)),3)})"    ))
lines1.append(ax1.plot(  v,  amplitudes      /max(amplitudes),       'y',       label=f"Amplitudes (*{round(max(amplitudes),3)})"        ))
lines1.append(ax1.plot(  v,  phases%(2*pi)   /(2*pi),                'g',       label='Phases (*2*Pi)'                                  ))
lines1.append(ax1.plot(  v,  periods         /max(abs(periods)),     'b',       label=f"Periods (*{round(max(abs(periods)),3)})"         ))

ax1.set_ylim(0,1)
ax1.grid()
ax1.legend()
ax1.set_title("Laser parameters",loc='left')
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Normalized Gain/Amplitude/Phase/Period")

total = zeros(len(x))
lines = []
for i in arange(modes)+1:
    w = wave(i,x,0)
    if i<=dispMax: lines.append(ax2.plot(x,w,label=f"mod {i}")[0])
    total += w
line_tot, = ax3.plot(x, zeros(len(x)), label="Total")

ax2.set_ylim(-max(amplitudes[:dispMax]), max(amplitudes[:dispMax]))
ax3.set_ylim(-sum(amplitudes), sum(amplitudes))
ax2.set_title("Laser waves",loc='left')
ax3.set_title("Sum of waves",loc='left')
ax2.set_ylim(-max(amplitudes[:dispMax]), max(amplitudes[:dispMax]))
for ax in [ax2,ax3]:
    ax.set_xlim(0,cavity_lenght)
    ax.grid()
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Amplitude")


im3, = ax3.plot([], [], color=(0,0,1))

# Plotting for a given time
def run(T):
    global amplitudes
    print(f"Progress: {round(T/t[-1]*100,2)} %",end="\r")

    total = zeros(len(x))
    
    for i in arange(modes)+1:
        w = wave(i,x,T)
        total += w

        if i<=dispMax:
            lines[i-1].set_data(x,w)
    line_tot.set_data(x,total)

    return lines + [line_tot]

ani = animation.FuncAnimation(fig, run, t, blit=True, interval=10,
    repeat=True)

ani.save(f"result.mp4")
plt.show()