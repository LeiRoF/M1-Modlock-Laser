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
mods = config['mods']
c = 3e8
cavity_lenght = c/fgap

tmp = 0
while tmp < fmin or tmp == 0:
    tmp += fgap


v = arange(fmin, fmin+fgap*mods, fgap)
x = linspace(0, cavity_lenght,1000, endpoint=True)

periods = []
phases = []
amplitudes = []
tmax = 1

for i in arange(mods)+1:
    periods.append(1/i)#random())
    phases.append(0)#random()*2*pi)
    amplitudes.append(1)#sqrt(i))
periods = array(periods)
amplitudes = array(amplitudes)
amplitudes = amplitudes/max(amplitudes)

t = linspace(0,max(periods)*2,1000)

# waves definition
def wave(mod,x,t):
    return amplitudes[mod-1]                        \
        *sin(x/cavity_lenght*pi*mod)                \
        *cos(2*pi*t/periods[mod-1] + phases[mod-1])

# Init plot
fig, (ax3, ax1, ax2) = plt.subplots(3,1)
ax1.set_ylim(-max(amplitudes[:10]), max(amplitudes[:10]))
ax2.set_ylim(-1, 1)
for ax in [ax1,ax2]:
    ax.set_xlim(0,cavity_lenght)
    ax.grid()

ax3.bar(v,amplitudes)
ax3.plot(v,gain_distrib(v),'r--')

# First plot at t=0
total = zeros(len(x))
lines = []
for i in arange(mods)+1:
    w = wave(i,x,0)
    if i<10: lines.append(ax1.plot(x,w,label=f"mod {i}")[0])
    total += w
line_tot, = ax2.plot(x, total)

# Plotting for a given time
def run(T):
    total = zeros(len(x))
    for i in arange(mods)+1:
        w = wave(i,x,T)
        if i<10: lines[i-1].set_data(x,w)
        total += w
    line_tot.set_data(x,total/max(abs(total)))

    return lines + [line_tot]

ani = animation.FuncAnimation(fig, run, t, blit=True, interval=10,
    repeat=True)
#ax1.legend()
ani.save(f"result.mp4")
plt.show()