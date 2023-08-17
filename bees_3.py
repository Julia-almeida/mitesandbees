import random
import simpy
import statistics
import numpy
import matplotlib
import matplotlib.pyplot as plt

# Define the parameters of the simulation
SIM_TIME = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct'] # Simulation time in month
INIT_BEES = 50000  # Initial number of bees in the colony
INFECTION_RATE = 0.5  # Probability of a bee getting infected each month
MORTALITY_RATE = 0.02  # Probability of an infected bee dying each month

# Initialize the colony
bees = [{'status': 'healthy'} for i in range(INIT_BEES)]

# Initialize the counters
num_infected = 0
num_dead = 0
num_healthy = INIT_BEES
num_infected_lastmonth = 0
num_dead_lastmonth = 0
num_healthy_lastmonth = INIT_BEES
num_reproduced = 0

# Run the simulation
infected_bees = 1
infected_bees_per_month = []
dead_bees_per_month = []

for month in SIM_TIME:
    if month == "Apr or month May and Jun":
        infection_rate = 0.025


for month in SIM_TIME:
    if month == "Jul":
        infection_rate = 0.05

for month in SIM_TIME:
    if month == "Jul or month Aug":
        infection_rate = 0.1

for month in SIM_TIME:
    if month == "Aug or month Sept":
        infection_rate = 0.75

for month in SIM_TIME:
    if month == "Sept or month Oct":
        infection_rate = 0.50 
    


    # Infect some bees
    num_reproduced += 1000
    for bee in bees:
    	if bee['status'] == 'healthy' and random.random() < INFECTION_RATE:
            bee['status'] = 'infected'
            num_infected += 1
            num_healthy -= 1
    # Kill some infected bees
    dead_bees = [bee for bee in bees if bee['status'] == 'infected' and
             	 random.random() < MORTALITY_RATE]
    for bee in dead_bees:
    	bees.remove(bee)
    	num_dead += 1
    	num_infected -= 1
    infected_bees_per_month.append(num_infected)
    dead_bees_per_month.append(num_dead)


    # Print the number of infected, dead, and healthy bees
    print("Month {}: {} bees infected (+{}), {} bees dead (+{}), {} bees healthy (-{})".format(month,
                                                                                             num_infected, num_infected
                                                                                             - num_infected_lastmonth,
                                                                                             num_dead, num_dead - num_dead_lastmonth,
                                                                                             num_healthy, num_healthy_lastmonth - num_healthy))
    # Update the counters for the next day
    num_infected_lastmonth = num_infected
    num_dead_lastmonth = num_dead
    num_healthy_lastmonth = num_healthy
                
# Print the total number of dead, infected, and healthy bees
print("Total number of infected bees: {}".format(num_infected))
print("Total number of dead bees: {}".format(num_dead))
print("Total number of healthy bees: {}".format(num_healthy))


# infected bees graph
plt.plot(infected_bees_per_month)
plt.xlabel('Month (April-October)')
plt.ylabel('Infected bees')
plt.title('Number of infected bees over time')
plt.show()

# dead bees graph
plt.plot(dead_bees_per_month)
plt.xlabel('Month (April-October)')
plt.ylabel('Dead bees')
plt.title('Number of deaths in bees over time')
plt.show()
