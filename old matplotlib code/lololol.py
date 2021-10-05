import numpy as np
import matplotlib.pyplot as plt 
import json

from numpy.lib.npyio import load #what why is this hereee

#variables
period = 10
total_mass = 120
radius = 1.6

sample_duration = .01
##


# H is from the ground

def dump_json(data):
    return json.dumps(data, indent=4, sort_keys=True)

def create_masses(mass_number):
    masses = []

    indiv_mass = total_mass / mass_number

    for i in range(mass_number):
        theta0 = i / mass_number * 2 * np.pi
        h = getHeight(theta0)

        if i < mass_number / 2:
            mass = indiv_mass
        else:
            mass = 0

        d = getpDist(theta0)
        masses.append({
            "mass":mass,
            "deg":theta0,
            "h":h,
            "d":d
        })

    return masses

def getpDist(theta):
    return 1.6 * np.sin(theta)

def getHeight(theta):
    return 1.6 * np.cos(theta) + 1.6

def simulate(mass_number):
    indiv_mass = total_mass / mass_number
    mass_number = mass_number
    dur = np.linspace(0, period, int(period / sample_duration))
    
    torque_array = np.zeros(1,)
    masses = create_masses(mass_number)

    for t in dur:
        torque = 0
        for i in range(mass_number):
            mass_info = masses[i]
            theta = i / mass_number * 2 * np.pi + (2 * np.pi / period * t)
            h = getHeight(theta)
            d = getpDist(theta)

            #not loading properly
            if - 0.01 < d < 0.01:
                if h > radius:
                    mass = indiv_mass
                elif h < radius:
                    mass = 0
            else:
                mass = mass_info["mass"]

            
            torque_indiv = mass * 9.81 * d

            masses[i] = {
                "mass":mass,
                "deg":theta,
                "h":h,
                "d":d,
                "t":torque_indiv
            }
            torque += torque_indiv


        torque_array = np.append(torque_array, torque)

    if len(torque_array) > len(dur):
        torque_array = torque_array[1:]

    return dur, torque_array


def main():

    dur, ta1 = simulate(4)
    dur, ta2 = simulate(12)
    

    plt.title("Torque thing") 
    plt.xlabel("time/s") 
    plt.ylabel("torque/Nm") 
    #
    plt.plot(dur, ta1, color ="red") 
    plt.plot(dur, ta2, color ="blue") 
    plt.show()

if __name__ == "__main__":
    main()