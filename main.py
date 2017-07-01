"""
Python Wind Computation tool
Copyright (C) 2017  Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# coding=utf-8
import matplotlib.pyplot as plt
import simulation
import scrape_bbc


def study1():

    """
    Data consist of forecasted values from the BBC weather for a particular
    part of UK. Place can be selected using the http://www.xcweather.co.uk/
    which shows forecast wind for the UK. By using the equation to calculate
    the power output we can display visually how the different weather affects
    the wind turbine output.

    [0 => Hour of the day , 1=> Temperature, 2=> Humidity, 3=> Wind Speed]

    To complete the excercise we will need to know the altitude of the place
    where we are sourcine the data from.
    """

    max_y_axis = 300000

    # power coefficinet 0.35-0.45
    cp = 0.35

    blade_radius = 3

    # Set figure width to 12 and height to 9
    #fig = plt.figure(figsize=(13, 7), dpi=100)

    bbc_weather = scrape_bbc.BBCScraper()
    bbc_weather.set_day(1)
    bbc_weather.set_location_id(2634739)

    data = bbc_weather.get_data()
    location = bbc_weather.get_location_name()

    # Setting List decomposition
    # settings[0] = radius of the blade
    # settings[1] = altitude above sea level
    # settings[2] = legend label
    settings = [blade_radius, 30, location]
    simulation.plot_day_graph(data, settings, max_y_axis, cp)

    bbc_weather = scrape_bbc.BBCScraper()
    bbc_weather.set_day(1)
    bbc_weather.set_location_id(2657834)

    data = bbc_weather.get_data()
    location = bbc_weather.get_location_name()

    # settings[0] = radius of the blade
    # settings[1] = altitude above sea level
    # settings[2] = legend label
    settings = [blade_radius, 30, location]
    simulation.plot_day_graph(data, settings, max_y_axis, cp)

    plt.show()


def study2():
    """
    The study models mathematically the relation between changing variables of
    the wind turbine power equation

    Power = (1/2) * p * A * v3 * Cp

    There is possibility of plotting the other variables manualy to see the
    relations of two or more variables.
    """

    cp = 0.35  # power coefficinet 0.35-0.45

    study = ['r', 'Blade Lenght (m)', 0, 10, 0.1, cp]
    # study = ['w', 'Wind Speed (m/s)', 0, 25, 0.1 ,cp ]
    # study = ['a', 'Altitute above sea leve (m)', 10, 1000, 10, cp]
    # study = ['t', 'Ambient Temperature (C)', 0, 40, 0.1, cp]
    # study = ['h', 'Relative Humidity (%)', 40, 100, 0.1, cp]
    # study = ['c', 'Power Coefficient', 0.35, 0.45, 0.01, cp]

    # data set 1
    default = [10, 1, 100, 20, 60, cp]
    # simulation.variable_study(study, default)

    # data set 2
    default = [10, 5, 100, 20, 60, cp]
    simulation.variable_study(study, default)

    # data set 3
    default = [10, 10, 100, 20, 60, cp]
    # simulation.variable_study(study, default)

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
    parameters = [0.1, 10, 0.1]
    # data =
    # [wind speed, radius, altitude, temperature, humidity, power coefficient]
    data = [2.5, 10, 100, 20, 60, 0.35]

    water_turbine = study('r', 'Blade Length (m)')
    water_turbine.set_parameters(parameters, data)
    water_turbine.set_fluid_density(water_density=1000)
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
    study1()


if __name__ == "__main__":
    main()
