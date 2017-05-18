class SimulatedAnnealing

    def run_algorithm(self):
        history = []
        history.append(start_point)
        working_point = self.select_best(history)

        while self.loop_end_condition():
            y = self.select_random(self.generate_neighbours(working_point))
            if self.q(y) > self.q(working_point):
                working_point = y
            else
                p_a = self.calculate_pa_parameter(self.q(y), self.q(working_point), temperature)
                if rand() < p_a
                    working_point = y
            history.append(y)
        return working_point

    def select_best(self, history):

    def loop_end_condition(self):

    def select_random(self, neighbours):

    def generate_neighbours(self, working_point):

    def q(self, point):

    def calculate_pa_parameter(q_y, q_working_point, temperature):
