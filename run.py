import yaml
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random

"""
  _   _ _   _ _     
 | | | | |_(_) |___ 
 | | | | __| | / __|
 | |_| | |_| | \__ \
  \___/ \__|_|_|___/
                    
"""

with open("config.yml", 'r') as stream:
    config=yaml.safe_load(stream)
    print("⚙️ Configuration:")
    for key, value in config.items(): print(f"   {key}: {value}")

def gauss(v,m,s):
    return exp(-0.5*((v-m)/s)**2)  # gaussian distribution wth max value = 1

# waves definition
def wave(mode,x,t):
    return (
        amplitudes[mode]                          # Amplitude
        *sin(x/cavity_lenght*pi*(mode+1))             # Space dependence
        *exp(-1j*(t*2*pi*v[mode]+phases[mode]))   # Time dependence
    )


"""
  ___       _ _   _       _ _          _   _             
 |_ _|_ __ (_) |_(_) __ _| (_)______ _| |_(_) ___  _ __  
  | || '_ \| | __| |/ _` | | |_  / _` | __| |/ _ \| '_ \ 
  | || | | | | |_| | (_| | | |/ / (_| | |_| | (_) | | | |
 |___|_| |_|_|\__|_|\__,_|_|_/___\__,_|\__|_|\___/|_| |_|
                                                         
"""

def phase_distrib(i):     return eval(config['phase_distrib'    ])
def amplitude_distrib(i): return eval(config['amplitude_distrib'])
def gain_distrib(i):      return eval(config['gain_distrib'     ])

fgap    = config['fgap']
modes   = config['modes']
dispMax = min(modes,config['display_modes'])

c             = 3e8
cavity_lenght = c/fgap

v = arange(fgap, fgap*(modes+1), fgap)
x = linspace(0, cavity_lenght,1000, endpoint=True)
t = linspace(0,max(1/v)*2,1000)

phases     = []
amplitudes = []
gain       = []

for i in arange(modes):
    phases.append(phase_distrib(i+1))
    amplitudes.append(amplitude_distrib(i+1))
    gain.append(gain_distrib(i+1))

amplitudes               = array(amplitudes)
amplitudes               = amplitudes/max(amplitudes)
phases                   = array(phases)
gain                     = array(gain)

if config['fixed_total_intensity']:
    amplitudes = amplitudes * 100 / sum(amplitudes)
    gain = gain / mean(gain)

initial_amplitudes = copy(amplitudes)
amplitudes *= gain

print("🧮 Computing...")
total_evol = []
waves_evol = []
for i, T in enumerate(t):
    waves_evol.append([])
    total = zeros(len(x)).astype(complex)

    for m in arange(modes):
        w = wave(m,x,T)
        waves_evol[i].append(w)
        total += w
    total_evol.append(total)

waves_evol = array(waves_evol)
total_evol = array(total_evol)

real_max = amax(real(total_evol))
abs_max = amax(abs(total_evol))
print("  -> Maximum pulse amplitude :",round(real_max,2))

"""
  ____                        __ _          _      __                          
 |  _ \ _ __ __ ___      __  / _(_)_ __ ___| |_   / _|_ __ __ _ _ __ ___   ___ 
 | | | | '__/ _` \ \ /\ / / | |_| | '__/ __| __| | |_| '__/ _` | '_ ` _ \ / _ \
 | |_| | | | (_| |\ V  V /  |  _| | |  \__ \ |_  |  _| | | (_| | | | | | |  __/
 |____/|_|  \__,_| \_/\_/   |_| |_|_|  |___/\__| |_| |_|  \__,_|_| |_| |_|\___|
                                                                               
"""

# __________________________________________________
# Init plot
fig, (ax1, ax2, ax3) = plt.subplots(3,1,figsize=(16,9))

# __________________________________________________
# First subplot : input data
lines1 = []
lines1.append(ax1.plot(  v, gain /max(gain),  c='0.55',  label=f"Laser gain (/{round(max(gain),3)})"    ))
ax1.vlines(v[0],ymin=0,ymax=amplitudes[0]/max(amplitudes), color='r', label=f"Modes (/{round(max(amplitudes),3)})")
for i in range(modes)[1:]: ax1.vlines(v[i],ymin=0,ymax=amplitudes[i]/max(amplitudes), color='r')
lines1.append(ax1.plot(  v,  initial_amplitudes   /max(initial_amplitudes), 'y',       label=f"Initial modes amplitudes (/{round(max(initial_amplitudes),3)})" ))
lines1.append(ax1.plot(  v,  phases%(2*pi)        /(2*pi),                  'g',       label='Phases (/2*Pi)'                                                  ))

#  Plot properties
ax1.set_ylim(ymin=0)
ax1.grid()
ax1.legend()
ax1.set_title("Laser parameters",loc='left')
ax1.set_xlabel("Frequency (Hz)")
ax1.set_ylabel("Normalized Gain/Amplitude/Phase/Period")

# __________________________________________________
# Second and third subplot : waves and sum
total = zeros(len(x)).astype(complex)
lines = []
lines_tot = []
for i in arange(modes):
    w = waves_evol[0][i]
    if i < dispMax: lines.append(ax2.plot(x,real(w)/max(amplitudes[:dispMax]),label=f"mode {i}")[0]) # Plot the 10 first modes
total = total_evol[0]
lines_tot.append(ax3.plot(x, real(total)/real_max,    label=f"Amplitude (real part) (/{round(real_max,2)})")[0])
lines_tot.append(ax3.plot(x, (abs(total)/abs_max)**2, label=f"Instensity (/{round(real_max**2,2)})")[0])

# Plot properties
ax2.set_title("Laser waves",loc='left')
ax3.set_title("Sum of waves",loc='left')
ax3.legend()
ax2.set_ylabel(f"Normalized amplitude (/{round(max(amplitudes[:dispMax]),2)})")
ax3.set_ylabel("Normalized amplitude")
for ax in [ax2,ax3]:
    ax.set_ylim(-1,1)
    ax.set_xlim(0,cavity_lenght)
    ax.grid()
    ax.set_xlabel("Distance (m)")

"""
     _          _                 _   _             
    / \   _ __ (_)_ __ ___   __ _| |_(_) ___  _ __  
   / _ \ | '_ \| | '_ ` _ \ / _` | __| |/ _ \| '_ \ 
  / ___ \| | | | | | | | | | (_| | |_| | (_) | | | |
 /_/   \_\_| |_|_|_| |_| |_|\__,_|\__|_|\___/|_| |_|
                                                    
"""

# __________________________________________________
# Plotting for a given time
def run(T):
    global amplitudes
    print(f"🎞️ Generating animation... {round((T+1)/len(t)*100,2)} %",end="\r")

    total = zeros(len(x)).astype(complex)
    
    for i in arange(modes):
        if i < dispMax: lines[i].set_data(x,real(waves_evol[T][i])/max(amplitudes[:dispMax]))
    
    total = total_evol[T]
    lines_tot[0].set_data(x,(real(total)/real_max))
    lines_tot[1].set_data(x,(abs(total)/abs_max)**2)

    return lines + lines_tot

ani = animation.FuncAnimation(fig, run, arange(len(t)), blit=True, interval=10, repeat=True)

try: ani.save(f"result.mp4")
except: print("⚠️ [WARNING] Cannot save the file. Please install ffmpeg to save the animation as a video. https://ffmpeg.org")
plt.show()