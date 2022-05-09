import yaml
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random

with open("config.yml", 'r') as stream:
    config=yaml.safe_load(stream)
    print(config)

v = arange(config['min'], config['max'], config['freq_gap'])

x = linspace(0, config['cavity_lenght'],1000, endpoint=True)

c = 3e8

mods = arange(33)+1
periods = []
phases = []
amplitudes = []
tmax = 1
for i in mods:
    periods.append(1/i)#random())
    phases.append(0)#random()*2*pi)
    amplitudes.append(1)
periods = array(periods)

t = linspace(0,max(periods)*2,1000)

# waves definition
def wave(mod,x,t):
    return amplitudes[mod-1]*sin(x/config['cavity_lenght']*pi*mod)*cos(2*pi*t/periods[mod-1] + phases[mod-1])

# Init plot
fig, (ax1, ax2) = plt.subplots(2,1)
ax1.set_ylim(-1, 1)
ax2.set_ylim(-len(mods), len(mods))
for ax in [ax1,ax2]:
    ax.set_xlim(0,config['cavity_lenght'])
    ax.grid()

# First plot at t=0
total = zeros(len(x))
lines = []
for i in mods:
    w = wave(i,x,0)
    lines.append(ax1.plot(x,w,label=f"mod {i}")[0])
    total += w
line_tot, = ax2.plot(x, total)

# Plotting for a given time
def run(T):
    total = zeros(len(x))
    for i in mods:
        w = wave(i,x,T)
        lines[i-1].set_data(x,w)
        total += w
    line_tot.set_data(x,total)

    return lines + [line_tot]

ani = animation.FuncAnimation(fig, run, t, blit=True, interval=10,
    repeat=True)
#ax1.legend()
ani.save(f"result.mp4")
plt.show()