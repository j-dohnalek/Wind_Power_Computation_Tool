import math

# COEFICIENTS

RD = 287.05  # gas constant for dry air, J/(kg*degK)
RV = 461.495 # gas constant for water vapor, J/(kg*degK)
KELV_CONST = 273.15 # constant to convert from celsius to kelvin
ATM_PRESSURE = 101325 # atmospheric pressure in pascals
ESO = 6.1078 # SATURATION VAPOR RESSURE OVER LIQUID WATER AT 0C

# Source : http://wahiduddin.net/calc/density_algorithms.htm
# ----------------------------------------------------------------
# DATA BELOW ARE FOR THE SATURATION VAPOR PRESSURE ESW (MILLIBARS)
# OVER LIQUID WATER GIVEN THE TEMPERATURE T (CELSIUS). THE POLYNOMIAL
# APPROXIMATION BELOW IS DUE TO HERMAN WOBUS, A MATHEMATICIAN WHO
# WORKED AT THE NAVY WEATHER RESEARCH FACILITY, NORFOLK, VIRGINIA,
# BUT WHO IS NOW RETIRED. THE COEFFICIENTS OF THE POLYNOMIAL WERE
# CHOSEN TO FIT THE VALUES IN TABLE 94 ON PP. 351-353 OF THE SMITH-
# SONIAN METEOROLOGICAL TABLES BY ROLAND LIST (6TH EDITION). THE
# APPROXIMATION IS VALID FOR -50 < T < 100C.

C0 = 0.99999683
C1 = -0.90826951E-2
C2 = 0.78736169E-4
C3 = -0.61117958E-6
C4 = 0.43884187E-8
C5 = -0.29883885E-10
C6 = 0.21874425E-12
C7 = -0.17892321E-14
C8 = 0.11112018E-16
C9 = -0.30994571E-19

# Library functions
#-------------------

def dewpoint_temperature(t,rh):
    """
    :param t  :temperature in celsius
    :param rh :relative humidity in %
    :return float: dewpoint temperature in celsius
    """ 
    return math.pow(( rh /100.0), 1.0/8.0 )*(112.0+0.9 * t)+ 0.1*t-112.0


def saturation_vapor_pressure(t):
    """
    :param t : dewpoint temperature
    p = (c0+T*(c1+T*(c2+T*(c3+T*(c4+T*(c5+T*(c6+T*(c7+T*(c8+T*(c9)))))))))) 
    Es = eso * p^8
    :return saturation vapor pressure in pascal
    """
    
    p = (C0+t*(C1+t*(C2+t*(C3+t*(C4+t*(C5+t*(C6+t*(C7+t*(C8+t*(C9))))))))))
    return ESO / math.pow(p, 8) * 100

def dry_air_pressure(alt):
    """
    :param alt: altitude in meters above the sea level
    :return float: pressure in pascals of dry air in given altitude
    """
    return ATM_PRESSURE * math.pow(1- alt * 0.0000225577,5.2559)


def fluid_density(alt,t,rh):
    """
    :param t  :temperature in celsius
    :param rh :relative humidity in %
    :param alt: altitude in meters above the sea level
    D=(Pd/(287.05*(t+273.15)))+(Pv/(461.495*(t+273.15)))
    """
    Pd = dry_air_pressure(alt)
    Pv = saturation_vapor_pressure(dewpoint_temperature(t,rh))
    return (Pd /( RD *(t+KELV_CONST)))+( Pv /( RV *(t+KELV_CONST)))
