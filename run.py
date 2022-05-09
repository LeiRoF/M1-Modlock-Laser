import yaml
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random

with open("config.yml", 'r') as stream:
    config=yaml.safe_load(stream)
    print(config)

def gauss(v,m,s):
    return 1/(s*sqrt(2*pi))*exp(-0.5*((v-m)/s)**2)  # gaussian distribution

fmin = config['fmin']
fgap = config['fgap']
Nmods = config['mods']
def gain_distrib(v):
    return eval(config['gain_distrib'])

first_mod = 0
while first_mod < fmin or first_mod == 0:
    first_mod += fgap

c = 3e8
x = linspace(0, c/fgap,1000, endpoint=True)
v = linspace(fmin, first_mod+Nmods*fgap, 1000, endpoint=True)

mods = arange(Nmods)+1
mods_freq = arange(first_mod, first_mod+Nmods*fgap, fgap)

periods = []
phases = []
amplitudes = []
for i in mods:
    periods.append(1/i)#random())
    phases.append(0)#random()*2*pi)
    amplitudes.append(sqrt(i))
periods = array(periods)
phases = array(phases)
amplitudes = array(amplitudes)

t = linspace(0,max(periods)*2,1000)

# waves definition
def wave(mod,x,t):
    return amplitudes[mod-1]                        \
        *sin(x/x[-1]*pi*mod)                        \
        *cos(2*pi*t/periods[mod-1] + phases[mod-1])

# Init plot
plt.figure(figsize=[15,20])
fig, (ax1, ax2, ax3) = plt.subplots(3,1)

ax2.set_ylim(-max(amplitudes[:10]), max(amplitudes[:10]))
ax3.set_ylim(-1, 1)
for ax in [ax2,ax3]:
    ax.set_xlim(x[0],x[-1])
    ax.grid()

ax3.text(0.5, 1.100, "y=sin(x)", bbox={'facecolor': 'white','alpha': 0.5, 'pad': 5}, transform=ax.transAxes, ha="center")


# First plot at t=0

ax1.vlines(x=mods_freq, ymin=0, ymax=amplitudes, color='b')
ax1.plot(v,gain_distrib(v))

total = zeros(len(x))
lines = []
for i in mods:
    w = wave(i,x,0)
    if i<10: lines.append(ax2.plot(x,w,label=f"mod {i}")[0])
    total += w
line_tot, = ax3.plot(x, total)


# Plotting for a given time
def run(T):
    global amplitudes
    total = zeros(len(x))
    #amplitudes *= gain_distrib(mods_freq)
    for i in mods:
        # modlines[i-1].set_height(amplitudes[i-1])
        w = wave(i,x,T)
        if i<10: lines[i-1].set_data(x,w)
        total += w
    line_tot.set_data(x,total/max(abs(total)))
    ax.text(0.5, 1.100, f"y=sin(x), frame: {round(T,3)}s",
            bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 5},
            transform=ax.transAxes, ha="center")
    # ttl.set_text(f"Total normalized (Max intensity = {max(abs(total))})")

    return lines + [line_tot]

ani = animation.FuncAnimation(fig, run, t, blit=True, interval=10,
    repeat=True)
#ax1.legend()
ani.save(f"result.mp4")
plt.show()