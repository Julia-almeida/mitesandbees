import math

from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

# all times are in hours
larval_max_age_hr = 35*24
hours_to_leave_after_infection = 10*24
base_infection_rate = 0.25
# base_infection_rate = 0.05

def compute_infected(model):
    n_infected = 0
    for agent in model.schedule.agents:
        if agent.critter_type == "bee" and agent.infected:
            n_infected += 1
    return n_infected

def remove_all_mites_on_bee(bee_agent):
    """Find all the mite agents that are on this bee, and remove them."""
    model = bee_agent.model
    schedule = model.schedule
    kill_list = []
    for agent_id in schedule._agents:
        agent = schedule._agents[agent_id]
        if agent.critter_type == "mite":
            if agent.bee_host.unique_id == bee_agent.unique_id:
                print('#MITE_TO_KILL_LIST:', agent_id)
                kill_list.append(agent)
    for kill_candidate_agent in kill_list:
        schedule.remove(kill_candidate_agent) # these two instructions kill it off
        model.grid.remove_agent(kill_candidate_agent)


def seasonal_infection_prob(base_rate, t_days):
    """Try simulating the fact that infections rise in the hot seasons.
    In this first stab assume that we start in April when temperature is
    at the annual average, and then use a sin() function to reach max
    at the height of summer.
    """
    temp_boost_factor = 1.0     # tunable from 0 to 1
    prob = base_rate * (1 + temp_boost_factor * math.sin(2*math.pi * t_days / 365.25))
    # print('PROB:', base_rate, t_days, prob)
    return prob

class BeeAgent(Agent):
    def __init__(self, unique_id, model, infected):
        super().__init__(unique_id, model)
        self.critter_type = "bee"
        self.age_hr = 0
        self.damaged_as_larva = False
        self.infected = infected
        self.hours_since_infected = 0

    def move(self):
        x, y = self.pos
        x_offset = self.random.randint(-1, 1)
        y_offset = self.random.randint(-1, 1)
        new_position = (x + x_offset, y + y_offset)
        # print(f'MOVING: bee {self.unique_id} from', self.pos, '->', new_position)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()
        # we just got an hour older
        self.age_hr += 1
        # for bees we track how long they have been infected, so we update that parameter
        if self.infected:
            self.hours_since_infected += 1
            # if the bee has been infected for more than 10 days, it
            # leaves the nest so we remove it
            if self.hours_since_infected > hours_to_leave_after_infection:
                remove_all_mites_on_bee(self)
                self.model.schedule.remove(self) # these two instructions kill it off
                self.model.grid.remove_agent(self)
                return
                
        # if it was damaged as a larva then it dies withing 2 days
        # of exiting larval stage
        if self.damaged_as_larva and self.age_hr > larval_max_age_hr + 2:
            remove_all_mites_on_bee(self)
            self.model.schedule.remove(self) # these two instructions kill it off
            self.model.grid.remove_agent(self)
            return

        # print(f"agent {self.unique_id}; infected {self.infected}; pos {self.pos}")


class MiteAgent(Agent):
    def __init__(self, unique_id, model, bee_host):
        super().__init__(unique_id, model)
        self.bee_host = bee_host
        self.critter_type = "mite"
        # self.days_since_infected = 0

    def move(self):
        # x, y = self.pos
        # x_offset = self.random.randint(-1, 1)
        # y_offset = self.random.randint(-1, 1)
        # new_position = (x + x_offset, y + y_offset)
        new_position = self.bee_host.pos # move with your bee
        if new_position != self.pos:
            # print(f'MOVING: mite {self.unique_id} with bee_host {self.bee_host.unique_id}',
            #       self.pos, '->', new_position)
            self.model.grid.move_agent(self, new_position)
        # else:
        #     print(f'NOT_MOVING: mite {self.unique_id} with bee_host {self.bee_host.unique_id}')

    def infect_neighbors(self):
        neighbors = self.model.grid.get_neighbors(self.pos,
                                                  moore=True,
                                                  include_center=True)
        for neighbor in neighbors:
            if neighbor.unique_id == self.unique_id:
                continue
            if neighbor.unique_id == self.bee_host.unique_id:
                continue
            if neighbor.critter_type != "bee":
                continue
            # mites infect bee neighbors by jumping to them
            infection_prob = seasonal_infection_prob(base_infection_rate,
                                                     self.model.global_t_hours / 24.0)
            if self.random.random() < infection_prob:
                prev_bee_id = self.bee_host.unique_id
                # print(f'INFECTION: mite {self.unique_id} jumps from bee {prev_bee_id}'
                #       + f'_{self.pos} to bee {neighbor.unique_id}_{self.pos}')
                neighbor.infected = True
                # now for some specific logic: if a bee is infected
                # when it is very young, it will be damaged and not
                # live long
                if neighbor.age_hr < larval_max_age_hr:
                    self.damaged_as_larva = True
                self.bee_host = neighbor
                self.model.grid.move_agent(self, neighbor.pos) # jump to that bee's position

    def step(self):
        self.move()
        self.infect_neighbors() # mites can always infect neighboring bees
        # FIXME: also insert reproduction here

class InfectionModel(Model):
    def __init__(self, N, width, height):
        self.random.seed(123456) # FIXME: remove this after debugging
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(width, height, torus=True)
        self.running = True
        self.datacollector = DataCollector(
            model_reporters = {"Infected": compute_infected})
        self.global_t_hours = 0  # start at day 0, each step will increase by 1
        for i in range(self.num_agents):
            infected = True if (i == 0) else False
            if i < 0.2*N:
                # first 20% are bees
                a = BeeAgent(i, self, infected)
                if i == 0:      # save the first bee
                    first_bee = a
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.grid.place_agent(a, (x, y))
                self.schedule.add(a)
            else:
                # the rest are mites
                a = MiteAgent(i, self, first_bee)
                x = first_bee.pos[0]
                y = first_bee.pos[1]
                self.grid.place_agent(a, (x, y))
                self.schedule.add(a)

    def set_all_mites_on_bees(self):
        """Make sure all mites are placed on bees.  The ordinary model
        dynamics don't guarantee this because each agent takes its
        step in random order, so this method can be called at the end
        of a time period to sync all the positions.
        """
        for (agentlist, (x, y)) in self.grid.coord_iter():
            for agent in agentlist:
                # if it's a mite find its bee and move it there
                if agent.critter_type == "mite" and agent.bee_host.pos != agent.pos:
                    new_bee_pos = agent.bee_host.pos
                    # print(f'UPDATED: mite from {agent.pos} to new bee pos {new_bee_pos}')
                    agent.model.grid.move_agent(agent, new_bee_pos)

    def step(self):
        self.schedule.step()
        #self.set_all_mites_on_bees()
        self.datacollector.collect(self)
        self.global_t_hours += 1 # each step is 1 day

