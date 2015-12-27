import matplotlib.pyplot as plt
import simulation

def study1():
    """
    Data consist of forecasted values from the BBC weather for a particular part of UK
    Place can be selected using the http://www.xcweather.co.uk/ which shows forecast wind
    for the UK.
    By using the equation to calculate the power output we can display visually how the 
    different weather affects the wind turbine output.
    
    [0 => Hour of the day , 1=> Temperature, 2=> Humidity, 3=> Wind Speed]
    
    To complete the excercise we will need to know the altitude of the place where we are
    sourcine the data from.
    """
	
    cp = 0.35 # power coefficinet 0.35-0.45
    
	# Warrington 14 April 2015 BBC Weather
	# Wind speed is in miles per hour 
	data = [ # hr,  t, rh, ws
			[ 0 , 10, 83,  7 ],
			[ 1 , 10, 83,  7 ],
			[ 2 , 10, 83,  6 ],
			[ 3 ,  9, 84,  7 ],
			[ 4 ,  9, 86,  7 ],
			[ 5 ,  9, 86,  8 ],
			[ 6 ,  9, 87,  8 ],
			[ 7 ,  9, 87,  9 ],
			[ 8 ,  9, 86,  9 ],
			[ 9 , 10, 86,  9 ],
			[10 , 11, 76, 10 ],
			[11 , 12, 70, 10 ],
			[12 , 13, 65, 10 ],
			[13 , 14, 59,  9 ],
			[14 , 15, 57, 10 ],
			[15 , 16, 54, 10 ],
			[16 , 16, 53, 10 ],
			[17 , 15, 55,  9 ],
			[18 , 15, 58,  9 ],
			[19 , 14, 63,  8 ],
			[20 , 12, 69,  7 ],
			[21 , 11, 76,  7 ],
			[22 , 10, 82,  6 ],
			[23 ,  9, 85,  6 ]
		   ]
	
	settings = [ 5 , 50 , 'Warrington 14.April.2015']
	simulation.plot_day_graph(data,settings, 30000 ,cp)
	
	# Aberdaron 14 April 2015 BBC Weather
	# Wind speed is in miles per hour
	data = [ # hr,  t, rh, ws
			[ 0 ,  8,100, 23 ],
			[ 1 ,  8,100, 21 ],
			[ 2 ,  8,100, 20 ],
			[ 3 ,  8,100, 21 ],
			[ 4 ,  8, 99, 21 ],
			[ 5 ,  8, 98, 21 ],
			[ 6 ,  8, 99, 20 ],
			[ 7 ,  8, 98, 20 ],
			[ 8 ,  8, 96, 20 ],
			[ 9 ,  9, 93, 20 ],
			[10 ,  9, 91, 19 ],
			[11 , 10, 90, 19 ],
			[12 , 10, 90, 19 ],
			[13 , 10, 89, 18 ],
			[14 , 10, 90, 18 ],
			[15 , 10, 92, 19 ],
			[16 , 10, 93, 20 ],
			[17 ,  9, 93, 19 ],
			[18 ,  9, 93, 19 ],
			[19 ,  9, 95, 19 ],
			[20 ,  8, 96, 19 ],
			[21 ,  8, 98, 19 ],
			[22 ,  8, 98, 20 ],
			[23 ,  8, 98, 20 ]
		   ]
	
	settings = [ 5 , 30 , 'Aberdaron 14.April.2015']
	simulation.plot_day_graph(data,settings, 30000 ,cp)

	plt.show()


def study2():
    """
    The study models mathematically the relation between changing variables of the
    wind turbine power equation
    
    Power = (1/2) * p * A * v3 * Cp
    
    There is possibility of plotting the other variables manualy to see the relations of 
    two or more variables.
    """

    cp = 0.35 # power coefficinet 0.35-0.45

	#study = ['r', 'Blade Lenght (m)', 0, 10, 0.1 ,cp ]
	#study = ['w', 'Wind Speed (m/s)', 0, 25, 0.1 ,cp ]
	study = ['a', 'Altitute above sea leve (m)', 10, 1000, 10 ,cp ]
	#study = ['t', 'Ambient Temperature (C)', 0, 40, 0.1 ,cp ]
	#study = ['h', 'Relative Humidity (%)', 40, 100, 0.1 ,cp ]
	#study = ['c', 'Power Coefficient', 0.35, 0.45, 0.01 ,cp ]

	# data set 1
	default = [ 10, 1 ,100,20,60 ,cp]
	#simulation.variable_study(study, default)
	
	# data set 2
	default = [ 10, 5 ,100,20,60,cp]
	simulation.variable_study(study, default)
	
	# data set 3
	default = [ 10, 10 ,100,20,60,cp]
	#simulation.variable_study(study, default)
	
	plt.show()


def water_study():
    """
    Marine turbines are designed using the same
    principles as wind turbines. However, they are
    used in the different conditions and the variables
    used in the power equation.
    As the marine turbine works in water rather than
    air, we will use density of water instead of air:
    Density of water, density = 1000 kg/m3
    The average power coefficient, Cp , for marine
    turbines is also different than that of wind
    turbines. Currently, the technology for marine
    turbines is not that much developed to reach the
    same levels of results as wind turbines. However,
    the theoretical maximum for marine turbines is
    still defined by Betz Law with a limit of 0.59 and
    we will use the following value of this coefficient:
    Power Coefficient Marine Turbine, Cpm = 0.35
    Given this information, rearrange the power
    equation using marine turbine variables to
    calculate the length of blade that would be
    needed to produce the same power by marine
    turbine as produced by the wind turbine in the
    example above. Assume v = 2.5m/s, which is the
    typical rated tidal flow speed.
    """
    
    # parameters => [start, end , increment]
    parameters = [ 0.1 , 10 , 0.1 ]
    # data => [wind speed, radius, altitude, temperature, humidity, power coefficient]
    data = [ 2.5 , 10 , 100 , 20, 60 , 0.35]

    water_turbine = study('r' , 'Blade Lenght (m)' )
    water_turbine.set_parameters( parameters , data )
    water_turbine.set_fluid_density( water_density = 1000 )
    water_turbine.execute()
    
    plt.show()
    
    
def study4():
    """
    The power coefficient is not a static value as
    defined in the main question; it varies with the tip
    speed ratio of the turbine. Tip speed ratio is
    defined as:
    
    lambda = blade tip speed / wind speed
    
    The blade tip speed can be calculated from the
    rotational speed of the turbine and the length of
    the blades used in the turbine using the following
    equation:
    
    blade tip speed = rotational speed ( rpm) * pi * D
    where D is the diameter of the turbine.
    
    Given that the rotational speed of the turbine is
    15rpm, calculate "lambda" using the above two
    equations and fill it in the following table. Then
    read the corresponding value of Cp using the
    graph below. This Cp value can then be used to
    calculate the power at that wind speed using
    appropriate form of equation (5). Finally, calculate
    the energy using the following equation and
    complete the table:
    
    Energy = Power × Time
    
    Please note, there are crosses in the following
    table where the wind turbine would not operate
    due to the wind speed being too high or too low.
    
    """
    pass


def main():
    water_study()


    
if __name__ == "__main__":
    main()
