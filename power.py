import math
import meteo


def swept_area(r):
    """
    :param r: length of blade in meters
    :return float swept area of the turbine (m/s2)
    """
    return math.pi * math.pow(r, 2)


def turbine_power(v, r, alt, t, rh, cp, d=None):
    """
    :param v  : wind velocity
    :param r  : length of blade in meters
    :param alt: altitude in meters above the sea level
    :param t  : temperature in celsius
    :param rh : relative humidity in %
    :param cp : coefficient of power 0.35-0.45
    :param d  : density of fluid 
    """
    a = swept_area(r)
    
    # Manual entry for the fluid density
    if d is None:
        _d = meteo.fluid_density(alt, t, rh)
    else:
        _d = d
        
    return (1.0/2.0)* _d * a * math.pow(v, 3) * cp


"""
Generators:
50% for car alternator
80% or possibly more for a permanent magnet generator
or grid-connected induction generator
"""
    

class Generator:

    generator_efficiency = None  # efficiency of gearbox

    def __init__(self):

        pass

    def efficiency(self, efficiency):
        """
        :param efficiency: gearbox efficiency

        """
        self.generator_efficiency = efficiency


"""
Gear ratios:
You may want to attach a gear system to your generator.
"""


class GearBox:

    gearbox_efficiency = None  # efficiency of gearbox

    def __init__(self):

        pass

    def efficiency(self, efficiency):
        """
        :param efficiency: bearings efficiency in percentage
        """
        self.gearbox_efficiency = efficiency


"""
Turbine Blade:
without blades, your turbine would not produce any electricity.
Some factors to consider:

Size, Shape, Number, Pitch ,Weight ,Material

Wing lift = 

"""


class TurbineBlade:

    radius = None  # length of blade in meters

    def __init__(self):
        pass


    def blade_length(self, radius, unit='m'):
        """
        :param radius  : length of blade in meters
        """
        if unit == 'm':
            self.radius = float(radius)
        elif unit == 'cm':
            self.radius = float(radius / 100)
        elif unit == 'ft':
            self.radius = float(radius * 0.3048)


    def swept_area(self):
        """
        :return turbine swept area
        """
        return math.pi * math.pow(self.radius, 2)


"""
Wind power efficiency

P = 0.5 x rho x A x Cp x V3(cubed) x Ng x Nb

P = power in watts (746 watts = 1 hp) (1,000 watts = 1 kilowatt)
rho = air density (about 1.225 kg/m3 at sea level, less higher up)
A = rotor swept area, exposed to the wind (m2)
Cp = Coefficient of performance (0.59 Betz limit is the maximum theoretically possible, .35 for a good design)
V = wind speed in meters/sec
Ng = generator efficiency - 50% for car alternator, 80% or possibly more for a permanent magnet generator or
grid-connected induction generator
Nb = gearbox/bearings efficiency (depends, could be as high as 95% if good)
"""


class MathematicalModel(TurbineBlade, Generator, GearBox):

    humidity = None
    temperature = None
    altitude = None
    speed = None
    betz_limit = None
    density = None

    def __init__(self):
        TurbineBlade.__init__(self)
        Generator.__init__(self)
        GearBox.__init__(self)

    def calculate(self, var='p'):
        """
        :param var: calculate variable

        t = temperature
        a = altitude
        c = power coefficient
        s = wind speed
        d = fluid density
        l = length of blade
        :return: value based on the requested calculation
        """
        p = self.power
        d = self.density
        a = self.swept_area()
        v = self.speed
        c = self.betz_limit
        g = self.generator_efficiency
        b = self.gearbox_efficiency

        # p = power
        if v == 'p':
            return (1.0/2.0)* d * a * v**3 * c * g * b

        # c = power coefficient
        elif var == 'c':
            if a != 0 and d != 0 and b != 0 and g != 0 and v != 0:
                return (2 * p) / (a * d * b * g * v**3)
            else:
                raise ZeroDivisionError("Power coefficient calculation error, a b d g v!=0")

        # s = wind speed
        elif var == 's':
            if a != 0 and d != 0 and b != 0 and g != 0 and c != 0:
                return (2.0**(1.0/3) * p**(1.0/3))/(a**(1.0/3) * b**(1.0/3) * c**(1.0/3) * d**(1.0/3) * g**(1.0/3))
            else:
                raise ZeroDivisionError("Wind speed calculation error,  a b c d g!=0")
        # d = fluid density
        elif var == 'd':
            if a != 0 and b != 0 and c != 0 and g != 0 and v != 0:
                return (2 * p)/(a * b * c * g * v**3)
            else:
                raise ZeroDivisionError("Fluid density calculation error, a b c g v!=0")

        # l = blade length
        elif var == 'l':

            if b != 0 and c != 0 and d != 0 and g != 0 and v != 0:
                a = (2 * p)/(b * c * d * g * v**3)
                return (a**(1.0/2))/(math.pi**(1.0/2))

            else:
                raise ZeroDivisionError("Blade length calculation error, b c d g v!=0")

    def wind_speed(self, s, unit='mps'):
        """
        :param s: wind speed
        :param unit: SI Unit
        """
        
        if unit == 'mph':
            # 1 mile/hour = 0.44704 meters/second 
            self.speed = float(s * 0.44704)

        elif unit == 'kmph' or unit == 'kph':
            # 1 kilometer/hour = 0.277777777777778 meters/second
            self.speed = float(s * 0.277777777777778)

        elif unit == 'mps':
            # meters per second
            self.speed = float(s)

        else:
            raise TypeError("Unsuported speed unit! Supported units are 'mph', 'mps', 'kph'")

    def altitude_above_sea(self, alt, unit='m'):
        """
        :param alt: altitude in meters above the sea level
        :param unit: SI Unit
        """
        if unit == 'm':
            self.altitude = float(alt)
        
        elif unit == 'ft':
            self.altitude = alt * 0.3048

        else:
            raise TypeError("Unsupported altitude unit! Supported units are 'm' or 'ft'.")

    def ambient_temperature(self, t, unit):
        """
        :param t  : temperature in celsius
        :param unit: SI Unit
        """
        if unit == 'F':
            self.temperature = float((t - 32.0) / 1.8)
        elif unit == 'C':
            self.temperature = float(t)
        else:
            raise TypeError("Unsupported temperature unit! Supported units are F or C.")

    def relative_humidity(self, rh):
        """
        :param rh : relative humidity in %
        """
        self.humidity = rh

    def performance_coefficient(self, cp):
        """
        :param cp: Coefficient of performance, Betz limit
        """
        self.betz_limit = cp

    def fluid_density(self, density):
        """
        :param density: density of fluid
        """
        self.density = density

    def power(self, pwr):
        """
        :param pwr: power in watts
        """
        self.power = pwr


"""
Wind Turbine:
-------------

1) Blades
2) Generator
3) Gear Box

"""


class Turbine(MathematicalModel):

    def __init__(self):

        pass


