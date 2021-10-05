import numpy as np 
import matplotlib.pyplot as plt 

########### MAKE IT SOME SORT OF FUNCTIONS SYSTEM WITH MU

## ALSO ATMOS DENSITY

u = 1000

## AP Mk8 stats
diam = 10 #in
As = np.pi * ( (diam/ 2) * 2.54 / 100 ) ** 2
m = 600
Cd = 0.41
g = 9.81 # for all calculations just do as negative g 
 # put in the bracket as degress, calcs to radians for you
rho = 1.225 # km/cbm, sl right now

def air_density(h): ##below 11km https://en.wikipedia.org/wiki/Barometric_formula
    return 1.2250 * ( 288.15 / (288.15 - 0.0065 * h )) ** -4.2557877405521705 ##(1 + (9.80665 * 0.0289644 / 8.3144598 / -0.0065))

def graph_projectile(As, m, Cd, theta0, g = 9.81):

    ### In miliseconds # linspace uses sample sizes
    lengthSeconds = 120
    milisecondsPerSample = 200 # 10 samples per second
    t = np.linspace(0, lengthSeconds, int(lengthSeconds * (1000 / milisecondsPerSample))) #end is exclusive ( [start, end) ).
    #print(int(lengthSeconds * (1000 / milisecondsPerSample)))

    theta0 = ( theta0 ) / 180 * np.pi

    ## Basic calcs
    ux = u * np.cos(theta0)
    uy = u * np.sin(theta0)
    #print(ux, uy)

    ## dragless projectile motion
    #sx = ux * t
    #sy = uy * t - 1/2 * g * np.square(t)

    sx = np.zeros(1,)
    sy = np.zeros(1,)
    sx0, sy0 = 0, 0

    ## THE FUN PART FUN PART
    aaaaaa = False


    ##Will use iteration because well I dont know any other way to do so
    for t0 in t:

        ## air pressure code as well

        dt = milisecondsPerSample / 1000
        theta1 = np.arctan( uy / ux )
        
        v = np.sqrt( uy ** 2 + ux ** 2 )
        FD = 0.5 * air_density(sy0) * v ** 2 * As * Cd
        print(FD)
        FDx = FD * np.cos(theta1)
        FDy = FD * np.sin(theta1)

        ax = FDx / m
        ay = FDy / m + g

        dsx = ux * dt - 1/2 * ax * dt ** 2
        dsy = uy * dt - 1/2 * ay * dt ** 2
        #print(sy1, uy * dt, 1/2 * g * dt ** 2)

        sx1 = sx0 + dsx
        sy1 = sy0 + dsy

        vx = ux - ax * dt
        vy = uy - ay * dt

        if aaaaaa:
            print("""Variables Calculated for {t0}s.
    theta1 = {theta1}
    ux = {ux}, uy = {uy}
    vx = {vx}, vy = {vy}
    ax = {ax}, ay = {ay}
    sx = {sx1}, sy = {sy1}
    dsx = {dsx}, dsy = {dsy}
    """.format(t0 = t0, ux = ux, uy = uy, vx = vx, vy = vy, ax = ax, ay = ay, theta1 = theta1 / np.pi * 180, sx1 = sx1, sy1 = sy1, dsx = dsx, dsy = dsy))

        sx = np.append(sx, sx1)
        sy = np.append(sy, sy1)

        sx0 = sx1
        sy0 = sy1

        #print(sy1)

        if sy1 < 0:
            break

        ux, uy = vx, vy

    ## remove negative ys


    ### Final params
    vf = np.sqrt( vx ** 2 + vy ** 2)
    thetaf = np.arctan( vy / vx )


    #sy = sy [sy >= 0]

    #print(sy)
    t = t[:len(sy)]
    #print(len(sy), len(t))

    


    sx = sx[:len(t)]

    ##bosh
    if len(sy) > len(sx):
        sy = sy[:-1]

    print("""
Range at {}°: {:.2f}km  |  Time to target: {:.2f}s""".format(theta0 / np.pi * 180, sx[-1] / 1000, t[-1], ))
    print("""Final angle: {:.2f}° | Final velocity: {:.2f}ms-1""".format(thetaf / np.pi * 180, vf))
    print("Impact kinetic energy: {:.2f}MJ".format(0.5 * m * vf * vf / 1000000))

    #print("FInal Velocity: {:.2f}ms⁻¹\nFinal Angle: {:.2f}°\n".format(vf, thetaf / np.pi * 180))


    return sx, sy

##
#print(sx, sy)


### starting stats
print("""
Now simulating trajectories for a {}in/{:.1f}mm, {}kg shell (Cd: {})
Muzzle velocity: {}ms-1 | Muzzle kinetic energy: {:.2f}MJ
""".format(
    diam,
    diam*25.4,
    m,
    Cd,
    u,
    0.5 * m * u * u / 1000000
))


plt.title("Shell trajectory") 
plt.xlabel("X/m") 
plt.ylabel("Y/m") 
#
sx_array, sy_array = graph_projectile(As, m, Cd, 10)
plt.plot(sx_array, sy_array, color ="red") 
#
#sx_array, sy_array = graph_projectile(As, m, Cd, 15)
#plt.plot(sx_array, sy_array, color ="blue") 

sx_array, sy_array = graph_projectile(As, m, Cd, 20)
plt.plot(sx_array, sy_array, color ="orange") 

#sx_array, sy_array = graph_projectile(As, m, Cd, 25)
#plt.plot(sx_array, sy_array, color ="green") 

sx_array, sy_array = graph_projectile(As, m, Cd, 30)
plt.plot(sx_array, sy_array, color ="brown") 

plt.gca().set_aspect("equal")
plt.show()

input()