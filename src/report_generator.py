from matplotlib import pyplot
import datetime

class ReportGenerator:

    def __init__(self, file_to_write):
        self.filename = file_to_write
        fig = pyplot.figure()
        self.ax = fig.add_axes([0.1, 0.1, 0.55, 0.75])
        self.ax.set_title('Przebieg dzialania algorytmu')
        self.ax.set_xlabel('Numer iteracji i')
        self.ax.set_ylabel('Wartosc funkcji celu q')
        self.data = []

    def set_params(self, max_iterations_, rail_cost_, electric_cost_, given_final_temperature_, given_starting_temperature_, alpha_):
        self.max_iterations = max_iterations_
        self.rail_cost = rail_cost_
        self.electric_cost = electric_cost_
        self.given_final_temperature = given_final_temperature_
        self.given_starting_temperature = given_starting_temperature_
        self.alpha = alpha_

    def add_graph_point(self, value):
        self.data.append(value)

    def add_graph_points(self, points):
        self.data = points

    def generate_graph(self):

        iterations = range(1, len(self.data) + 1)
        self.ax.plot(iterations, self.data, 'ro', color='red', label='q(i)')

        self.ax.plot(range(0), range(0), color='white', label='\nParams: '
                                               + '\nMax_iter: ' + str(self.max_iterations)
                                               + '\nRail_cost: ' + str(self.rail_cost)
                                               + '\nElectric_cost: ' + str(self.electric_cost)
                                               + '\nFinal_temp: ' + str(self.given_final_temperature)
                                               + '\nStart_temp: ' + str(self.given_starting_temperature)
                                               + '\nAlpha: ' + str(self.alpha) )

        self.ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
       # pyplot.show()
        pyplot.savefig(self.filename + '_' + datetime.datetime.today().strftime('%Y_%m_%d_%H_%M_%S') + '_iterations.png')