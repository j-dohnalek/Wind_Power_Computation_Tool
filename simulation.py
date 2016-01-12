import power
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerLine2D


def plot_day_graph(data,settings, y_max, cp):
	
	"""
	Comparance of one days worth of 24 hour data from two locations
	around UK
	"""
	# Size of the graph
	plt.axes(xlim=(0, 23), ylim=(0, y_max))
	
	
	r = settings[0]
	alt = settings[1]
	x,y = [],[]
	total_pwr = 0
	
	for h in range(24):
		
		# Wind speed is in miles per hour on BBC Website
		# To convert miles/hour to meters/second we user
		# 1 mile/hour = 0.44704 meters/second 
		mps = data[h][3] * 0.44704
		# Power output
		w = power.turbine_power( mps, r, alt, data[h][1], data[h][2], cp)
		total_pwr += w
		y.append(w)
		x.append(h)

	label = settings[2] + " Output: %.2f Watts" % total_pwr
	line1, = plt.plot(x, y, label = label, linewidth=2)
	plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})

	plt.ylabel('Power Output (Watts)')
	plt.xlabel('Hours of Day')
	plt.title('Wind turbine power generation from turbine radius %s m' % r)
	
	return plt


def variable_study(study, default=None, legend=True , density=None):
	"""
	study   [study type, label title, start, end , increment]
	default [wind speed, radius, altitude, temperature, humidity, power coefficient]
	"""
	# VARIABLES
	x, y = [], []
	var = study[2]  # starting value
	plt.xlabel( study[1] )
	plt.ylabel('Power output (Watts)')

	if default is None:
		df = [ 10 , 0.5 , 100 , 19 , 80 , 0.4 ]
	else:
		df = default
	
	while var < study[3]: # study[3] = end
				
		if study[0]   == 'w':
			df[0] = var
		elif study[0] == 'r': 
			df[1] = var
		elif study[0] == 'a':
			df[2] = var
		elif study[0] == 't':
			df[3] = var
		elif study[0] == 'h':
			df[4] = var
        elif study[0] == 'c':
            df[5] = var

		x.append(var)
        
        if density is None:
            y.append(power.turbine_power( df[0], df[1], df[2], df[3], df[4], df[5]))
        else:
            y.append(power.turbine_power( df[0], df[1], df[2], df[3], df[4], df[5] , density))
            
		var += study[4] # study[4] = increment

	if study[0]   == 'r':
		text = "Constants: v = %sm/s; alt = %sm; t = %sC; RH = %s%%; Cp = %s" % (df[0],df[2],df[3],df[4],df[5])
		plt.title('Variable Radius Study')
	elif study[0] == 'w':
		text = "Constants: r = %sm; alt = %sm; t = %sC; RH = %s%%; Cp = %s" % (df[1],df[2],df[3],df[4],df[5])
		plt.title('Variable Wind Speed Study')
	elif study[0] == 'a':
		text = "Constants: v = %sm/s; r = %sm; t = %sC; RH = %s%%; Cp = %s" % (df[0],df[1],df[3],df[4],df[5])
		plt.title('Variable Altitude Study')
	elif study[0] == 't':
		text = "Constants: v = %sm/s; r = %sm; a = %sm; RH = %s%%; Cp = %s" % (df[0],df[1],df[2],df[4],df[5])
		plt.title('Variable Temperature Study')
	elif study[0] == 'h':
		text = "Constants: v = %sm/s; r = %sm; a = %sm; t = %sC; Cp = %s" % (df[0],df[1],df[2],df[3],df[5])
		plt.title('Variable Humidity Study')
    elif study[0] == 'c':
		text = "Constants: v = %sm/s; r = %sm; a = %sm; t = %sC; RH = %s%%" % (df[0],df[1],df[2],df[3],df[4])
		plt.title('Variable Coefficient of Power Study')
		
	line1, = plt.plot(x, y, label = text, linewidth=2)

	if legend:
		plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
		
	return plt

"""
Class Study
-----------
Enables to study the interactions between variables of the power equation.
The results are displayed in graph for the user.

"""
    
class study:
    
    _type  = ''      # type of the study represented by one letter
    _label = ''      # title of the study 
    _params = []     # [start, end , increment]
    _data = []       # [wind speed, radius, altitude, temperature, humidity, power coefficient]
    _density = None  # density of fluid

    def __init__(self,type,label):
        """
        :param type: type of the study represented by one letter
        :param title: title of the study 
        """
        available_study = ['r','w','a','t','h','c']
        
        if type in available_study:
            self._type = type
            self._label = label
    
    def set_fluid_density(self, density):
        """
        :param density: fluid density
        for special cases when we are not dealing with fluid as air
        """
        self._density = float(density)
        
    def set_parameters(self, parameters, data=None):
        """
        :param parameters: study parameters 
        parameters => [start, end , increment]
        :param data: study variables
        data => [wind speed, radius, altitude, temperature, humidity, power coefficient]
        """
        self._params = parameters
        
        if self._data is None:
            self._data = [ 10 , 0.5 , 100 , 19 , 80 , 0.4 ]
        else:
            self._data = data

    
    
    def execute(self):
    	"""
    	Execute the simulation and display the result on graph
    	"""
    	
        # VARIABLES
        x, y = [], []
        var = self._params[0]  # starting value
        plt.xlabel( self._label )
        plt.ylabel('Power output (Watts)')
        
        df = self._data
	
	# Select the study variable
        while var < self._params[1]: # _params[3] = end
                    
            if self._type   == 'w':
                df[0] = var
            elif self._type == 'r': 
                df[1] = var
            elif self._type == 'a':
                df[2] = var
            elif self._type == 't':
                df[3] = var
            elif self._type == 'h':
                df[4] = var
            elif self._type == 'c':
                df[5] = var

            x.append(var)
            
            if self._density is None:
                y.append(power.turbine_power( df[0], df[1], df[2], df[3], df[4], df[5]))
            else:
                y.append(power.turbine_power( df[0], df[1], df[2], df[3], df[4], df[5] , self._density))
                
            var += self._params[2] # self._params[2] = incrementation value
            
        if self._type   == 'r':
            text = "Constants: v = %sm/s; alt = %sm; t = %sC; RH = %s%%; Cp = %s" % (df[0],df[2],df[3],df[4],df[5])
            plt.title('Variable Radius Study')
        elif self._type == 'w':
            text = "Constants: r = %sm; alt = %sm; t = %sC; RH = %s%%; Cp = %s" % (df[1],df[2],df[3],df[4],df[5])
            plt.title('Variable Wind Speed Study')
        elif self._type == 'a':
            text = "Constants: v = %sm/s; r = %sm; t = %sC; RH = %s%%; Cp = %s" % (df[0],df[1],df[3],df[4],df[5])
            plt.title('Variable Altitude Study')
        elif self._type == 't':
            text = "Constants: v = %sm/s; r = %sm; a = %sm; RH = %s%%; Cp = %s" % (df[0],df[1],df[2],df[4],df[5])
            plt.title('Variable Temperature Study')
        elif self._type == 'h':
            text = "Constants: v = %sm/s; r = %sm; a = %sm; t = %sC; Cp = %s" % (df[0],df[1],df[2],df[3],df[5])
            plt.title('Variable Humidity Study')
        elif self._type == 'c':
            text = "Constants: v = %sm/s; r = %sm; a = %sm; t = %sC; RH = %s%%" % (df[0],df[1],df[2],df[3],df[4])
            plt.title('Variable Coefficient of Power Study')
            
        line1, = plt.plot(x, y, label = text, linewidth=2)

        if legend:
            plt.legend(handler_map={line1: HandlerLine2D(numpoints=4)})
            
        return plt
