# bearing = SKF 61914
# (https://www.skf.com/group/products/bearings-units-housings/ball-bearings/deep-groove-ball-bearings/deep-groove-ball-bearings/index.html?designation=61914)
# https://www.skf.com/group/products/bearings-units-housings/ball-bearings/deep-groove-ball-bearings/loads/index.html

# simulation.....of the simulation :) Judges like to know you understand the tool, not just know how to use it
# if you cannot build it, you do not understand it. If you cannot program it, you do no understand it.
# https://www.skfbearingselect.com/#/size-lubrication/single-bearing
from bisect import bisect_left

class Interpolate(object):
    def __init__(self, x_list, y_list):
        if any(y - x <= 0 for x, y in zip(x_list, x_list[1:])):
            raise ValueError("x_list must be in strictly ascending order!")
        x_list = self.x_list = map(float, x_list)
        y_list = self.y_list = map(float, y_list)
        intervals = zip(x_list, x_list[1:], y_list, y_list[1:])
        self.slopes = [(y2 - y1)/(x2 - x1) for x1, x2, y1, y2 in intervals]

    def __getitem__(self, x):
        i = bisect_left(self.x_list, x) - 1
        return self.y_list[i] + self.slopes[i] * (x - self.x_list[i])
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dimensions
d = 70  # [mm]
D = 100  # [mm]
B = 16  # [mm]
d1 = 79.8  # [mm]
D2 = 92.9  # [mm]
r1_2 = 1  # [mm]
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# Calculation Data
C = 23.8  # basic dynamic load rating in [kN]
C0 = 18.3  # basic static load rating [kN]
Pu = 0.9  # fatigue load limit [kN]
kr = 0.02  # calculation factor
f0 = 14.1  # calculation factor
mass = 0.34  # mass in [kg]

Fa = 4.3  # axial load in [kN]
Fr = 1.5  # axial load in [kN]
dm = 0.5 * (d + D)  # bearing mean diameter in [mm]
v = 28  # actual operating viscosity of the lubricant in [mm^2/s]
n = 1680  # rotational speed [r/min]
Frm = kr*((v*n/1000)**(2/3)*(dm/100)**2) # minimum radial load [kN]
calcFactor = f0*Fa/C0
# C3 and C4 are not required for the relatively slow spinning tires of an FSAE car, therefore, e is derived from single row deep groove ball bearing
calcFactor_list = [0.172, 0.345, 0.689, 1.03, 1.38, 2.07, 3.45, 5.17, 6.89]
e_list = [0.19, 0.22, 0.26, 0.28, 0.3, 0.34, 0.38, 0.42, 0.44]

X_list = [0.56, 0.560001, 0.560002, 0.560003, 0.560004, 0.560005, 0.560006, 0.560007, 0.560008]  # radial load factor for deep groove ball bearings
Y_list = [2.3, 1.99, 1.71, 1.55, 1.45, 1.31, 1.15, 1.04, 1]  # axial load factor for deep groove ball bearings depending on the relationship f0 Fa/C0

# calcFactor_x vs e_y
i1 = Interpolate(calcFactor_list, e_list)
e = i1[calcFactor] # limit for load depending on relationship f0 Fa/C0

# e_x vs x_y
i2 = Interpolate(calcFactor_list, X_list)
X = i2[calcFactor]

# e_x vs y_y
i3 = Interpolate(calcFactor_list, Y_list)
Y = i3[calcFactor]

if Fa/Fr <= e:
    P = Fr # equivalent dynamic bearing load [kN]
elif Fa/Fr > e:
    P = (X*Fr) + (Y*Fa) # equivalent dynamic bearing load [kN

load_ratio = C/P # load ratio
#add Axial load carrying capacity
#add Load carrying capacity of matched bearing pairs

P0 = 0.6*Fr + 0.5*Fa  # equivalent static bearing load [kN]1.5
if P0 < Fr:
    P0 = Fr
else:
    P0 = P0

S0 = C0/P0 # safety factor
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# only will need this once we get into multiple bearing sims. KISS for now
Y1=0 # calculation factors for the axial load depending on the relationship f0 Fa/C0
Y2=0 # calculation factors for the axial load depending on the relationship f0 Fa/C0
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
# Outputs
print (Frm)
print (P)
print (load_ratio)
print (P0)
print (S0)
