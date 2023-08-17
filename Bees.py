import random
import simpy
import statistics
import numpy
import matplotlib
import matplotlib.pyplot as plt

# Define the parameters of the simulation
SIM_TIME = 30  # Simulation time in days
INIT_BEES = 50000  # Initial number of bees in the colony
INFECTION_RATE = 0.5  # Probability of a bee getting infected each day
MORTALITY_RATE = 0.02  # Probability of an infected bee dying each day
init_mites = 1

# Initialize the colony
bees = [{'status': 'healthy'} for i in range(INIT_BEES)]

# Initialize the counters
num_infected = 0
num_dead = 0
num_healthy = INIT_BEES
num_infected_yesterday = 0
num_dead_yesterday = 0
num_healthy_yesterday = INIT_BEES
num_reproduced = 0
num_reproduced_yesterday = 0
num_mites = init_mites

# Run the simulation
infected_bees = 1
infected_bees_per_day = []
dead_bees_per_day = []

for day in range(SIM_TIME):

    # Infect some bees
    num_reproduced += random.randint(10,1500)
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
    infected_bees_per_day.append(num_infected)
    dead_bees_per_day.append(num_dead)


    # Print the number of infected, dead, and healthy bees
    print("Day {}: {} bees infected (+{}), {} bees dead (+{}), {} bees healthy (-{})".format(day,
                                                                                             num_infected, num_infected
                                                                                             - num_infected_yesterday,
                                                                                             num_dead, num_dead - num_dead_yesterday,
                                                                                             num_healthy, num_healthy_yesterday - num_healthy))
    # Update the counters for the next day
    num_infected_yesterday = num_infected
    num_dead_yesterday = num_dead
    num_healthy_yesterday = num_healthy
    num_reproduced_yesterday = num_reproduced
                
# Print the total number of dead, infected, and healthy bees
print("Total number of infected bees: {}".format(num_infected))
print("Total number of dead bees: {}".format(num_dead))
print("Total number of healthy bees: {}".format(num_healthy))


# infected bees graph
plt.plot(infected_bees_per_day)
plt.xlabel('Day')
plt.ylabel('Infected bees')
plt.title('Number of infected bees over time')
plt.show()

# dead bees graph
plt.plot(dead_bees_per_day)
plt.xlabel('Day')
plt.ylabel('Dead bees')
plt.title('Number of deaths in bees over time')
plt.show()

# mites multiplying graph
#plt.plot(mites_multiplying)
#plt.xlabel('Day')
#plt.ylabel('Number of mites')
#plt.title('Reproducing mites')
#plt.show()


   

    

    

    
