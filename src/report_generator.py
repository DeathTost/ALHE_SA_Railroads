from matplotlib import pyplot
import datetime
import networkx as nx
import os.path

class ReportGenerator:

    def __init__(self):
        self.format = "%Y_%m_%d_%H_%M_%S_%f"

    def generate_diagram(self, costs, filename):
        pyplot.title('Przebieg dzialania algorytmu')
        pyplot.xlabel('Numer iteracji i')
        pyplot.ylabel('Wartosc funkcji celu q')

        iterations = range(1, len(costs) + 1)
        pyplot.plot(iterations, costs, 'ro', color='red', label='q(i)')

        pyplot.legend(bbox_to_anchor=(0.8, 1.08), loc=2, borderaxespad=0.)
        #pyplot.show()
        pyplot.savefig(filename + '_' + '_cost_diagram.png')
        pyplot.close()

    def generate_best_railroad(self, railTree, cities, electric_powers,cost_traction, cost_power_lines, filename, index):
        figure, axes = pyplot.subplots()
        g = nx.Graph()

        traction_len, powers_len = railTree.get_rails_and_electric_traction_length()

        cityNodes = {i: i for i in cities}
        nx.draw_networkx_nodes(g, cityNodes, cityNodes.keys(), node_color='blue', node_size=75,
                               label='City' + '\n' + 'Length: ' + str(format(traction_len, '.5f')) + '\n' + 'Cost: ' + str(cost_traction) + '\n', ax=axes)

        powerNodes = {i: i for i in electric_powers}
        nx.draw_networkx_nodes(g, powerNodes, powerNodes.keys(), node_color='red', node_size=25,
                               label='PowerStation' + '\n' + 'Length: ' + str(format(powers_len, '.5f')) + '\n' + 'Cost: ' + str(cost_power_lines) + '\n', ax=axes)

        nullNodes = {(0, 0): (0, 0)}
        nx.draw_networkx_nodes(g, nullNodes, nullNodes.keys(), node_color='white', node_size=0,
                               label='Goal function: ' + str(format(railTree.goal_function,".10f"))
                                     + '\n Final sum: ' + str(1 / railTree.goal_function) + '\n ', ax=axes)

        for seg in railTree.rail_segments:
            if seg.is_power_plant_connected is True:
                for power_seg in seg.power_plant_connection:
                    points_set = power_seg.cities.copy()
                    if len(points_set) == 2:
                        point1 = points_set.pop()
                        if point1 not in cityNodes and point1 not in powerNodes:
                            pos = {point1: point1}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='red', node_size=10, ax=axes)
                        point2 = points_set.pop()
                        if point2 not in cityNodes and point2 not in powerNodes:
                            pos = {point2: point2}
                            nx.draw_networkx_nodes(g, pos, pos.keys(), node_color='red', node_size=10, ax=axes)
                        pos = {point1: point1, point2: point2}
                        nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='red', ax=axes)
            points_set = seg.cities.copy()
            point1 = points_set.pop()
            point2 = points_set.pop()
            pos = {point1: point1, point2: point2}
            nx.draw_networkx_edges(g, pos, [(point1, point2)], edge_color='black', ax=axes)

        pyplot.gca().set_aspect('equal', adjustable='box')
        pyplot.xlabel('wspolrzedna x')
        pyplot.ylabel('wspolrzedna y')
        pyplot.title('Optymalna siec kolejowa')
        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, -0.1))
        legend.get_frame().set_alpha(0.5)
        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests'))
        file_out = filename +'_'+ str(index)+'_best_city_graph.png'
        pyplot.savefig(folder_path + "\\" + file_out, bbox_extra_artists=(legend,), bbox_inches='tight')
        pyplot.close(figure)

    def generate_average_diagram(self, min_val, max_val, avg_val, start_temp, alpha, filename):
        size = len(min_val)
        figure, axes = pyplot.subplots()

        x = range(1, size + 1)
        y = avg_val

        pyplot.xlabel('Numer iteracji i')
        pyplot.ylabel('Funkcja celu q')
        pyplot.title('Przebieg dzialania algorytmu')
        pyplot.errorbar(x, y, yerr=[min_val, max_val], capsize=2, color='black', label='O(i)')
        x = range(0)
        y = range(0)
        pyplot.plot(x, y, color='white', label='Iterations: ' + str(size) + '\n Start temperature: '+ str(start_temp) +'\n Alpha: '+str(alpha))
        handles, labels = axes.get_legend_handles_labels()
        legend = axes.legend(handles, labels, loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.1))
        legend.get_frame().set_alpha(0.5)

        folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests'))
        file_out = filename +'_'+datetime.datetime.today().strftime(self.format)+ '_avg_plot.png'
        pyplot.savefig(folder_path + "\\" + file_out, bbox_extra_artists=(legend,), bbox_inches='tight')
        pyplot.close(figure)