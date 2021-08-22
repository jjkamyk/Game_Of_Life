from lattice_draw_from_txt import LatticeDrawFromTxt
import matplotlib.patches as patch
import numpy as np


# GameOfLife - class representing our implementation of Conway's Game Of Life
class GameOfLife:

    def __init__(self, states_matrix):
        self.states_matrix = states_matrix  # initial states of matrix read from .txt file
        self.size = self.matrix_shape()
        self.drawing_machine = LatticeDrawFromTxt(self.size[::-1])  # creating lattice of corresponding size
        self.size_x = self.size[1]
        self.size_y = self.size[0]
        self.game_state = {}  # creating an initial state of game
        for x in range(0, self.size_x):
            for y in range(0, self.size_y):
                if states_matrix[y][x] == 1:
                    self.game_state[(x, self.size_y - y - 1)] = 'Alive Cell'
                elif states_matrix[y][x] == 0:
                    self.game_state[(x, self.size_y - y - 1)] = 'Dead Cell'
        self.period = 0

    # this method allows us to read .txt file with initial pattern
    # it can adjust any given symbols representing state of cells (alive/dead) to matrix filled with 1 and 0
    # it returns object of GameOfLife class with read initial state
    @staticmethod
    def read_states_from_txt(file, alive_cell_symbol='o', dead_cell_symbol='.'):
        file = open(file)
        states_string = file.read()
        states_rows = states_string.split('\n')
        states_matrix = []
        for i in range(len(states_rows)):
            states_matrix.append(list(states_rows[i]))
        states_matrix = np.array(states_matrix)
        states_matrix[states_matrix == alive_cell_symbol] = 1
        states_matrix[states_matrix == dead_cell_symbol] = 0
        states_matrix = states_matrix.astype(int)
        return GameOfLife(states_matrix)

    # this method returns shape of matrix from .txt
    def matrix_shape(self):
        return self.states_matrix.shape

    # returns two lists of alive and dead cells, respectively
    def get_states(self):
        alive_cells = []
        dead_cells = []
        for cell, state in self.game_state.items():
            if state == 'Alive Cell':
                alive_cells.append(cell)
            elif state == 'Dead Cell':
                dead_cells.append(cell)
        return alive_cells, dead_cells

    def setup_pictures(self, underpopulation=2, overpopulation=3, rebirth=3,
                       boundary_conditions='traditional'):
        self.drawing_machine.create_directory()
        self.drawing_machine.draw_lines()
        self.drawing_machine.ax.set_xlabel(
            'Parameters: underpopulation={0}, overpopulation={1}, rebirth={2},\nboundary_conditions={3}'.format(
                underpopulation, overpopulation, rebirth, boundary_conditions))
        self.drawing_machine.ax.get_xaxis().set_ticks([])
        self.drawing_machine.ax.get_yaxis().set_ticks([])
        custom_lines = [patch.Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='k', facecolor='blue'),
                        patch.Rectangle((0, 0), 1, 1, linewidth=1, edgecolor='k', facecolor='w')]
        self.drawing_machine.fig.legend(custom_lines, ['Alive Cell', 'Dead Cell'], 'center right')
        self.drawing_machine.fig.subplots_adjust(left=0.05, right=0.75, top=0.90, bottom=0.1)

    def update_pictures(self, stop_option, t):
        alive_cells, dead_cells = self.get_states()
        self.drawing_machine.remove_squares()
        self.drawing_machine.color_squares(alive_cells, 'blue')
        self.drawing_machine.ax.set_title('Game of Life with stop option={0}, t={1}'.format(stop_option, t))
        self.drawing_machine.save()

    # returns number of alive neighbors
    # we consider two types of boundary_conditions: 'traditional', 'toroidal'
    def alive_neighbors_count(self, cell, boundary_conditions='traditional'):
        x = cell[0]
        y = cell[1]
        possible_neighbors = [(cell[0], cell[1] + 1),
                              (cell[0] + 1, cell[1]),
                              (cell[0], cell[1] - 1),
                              (cell[0] - 1, cell[1]), (cell[0] + 1, cell[1] + 1),
                              (cell[0] + 1, cell[1] - 1),
                              (cell[0] - 1, cell[1] - 1),
                              (cell[0] - 1, cell[1] + 1)]
        neighbors = [neighbor for neighbor in possible_neighbors if neighbor in self.game_state.keys()]
        if boundary_conditions == 'toroidal':
            possible_neighbors = [(x, (y - 1) % self.size_y),
                                  (x, (y + 1) % self.size_y),
                                  ((x - 1) % self.size_x, y),
                                  ((x + 1) % self.size_x, y),
                                  ((x - 1) % self.size_x, (y - 1) % self.size_y),
                                  ((x - 1) % self.size_x, (y + 1) % self.size_y),
                                  ((x + 1) % self.size_x, (y - 1) % self.size_y),
                                  ((x + 1) % self.size_x, (y + 1) % self.size_y)]
            neighbors = possible_neighbors
        alive_neighbors_counter = 0
        for neighbor in neighbors:
            if self.game_state[neighbor] == 'Alive Cell':
                alive_neighbors_counter += 1
        return alive_neighbors_counter

    # this method returns lists of alive and dead cells
    # available arguments:
    # underpopulation, overpopulation, rebirth - constants in game of life rules:
    # 1. alive cell dies if len(neighbors) < underpopulation or len(neighbors) > overpopulation
    # 2. dead cell rebirths if len(neighbors) == rebirth
    # boundary_conditions: 'traditional', 'toroidal'
    def simulation_step(self, underpopulation, overpopulation, rebirth, boundary_conditions='traditional'):
        new_alive_cells = []
        new_dead_cells = []
        for cell in self.game_state.keys():
            alive_neighbors_counter = self.alive_neighbors_count(cell, boundary_conditions)
            if self.game_state[cell] == 'Dead Cell':
                if alive_neighbors_counter == rebirth:
                    new_alive_cells.append(cell)
                else:
                    new_dead_cells.append(cell)
            else:
                if alive_neighbors_counter < underpopulation or alive_neighbors_counter > overpopulation:
                    new_dead_cells.append(cell)
                else:
                    new_alive_cells.append(cell)
        return new_alive_cells, new_dead_cells

    # this method simulates game
    # it also produces additional attribute - period (period = 0 means that period was not detected)
    # available arguments:
    # N - number of iterations
    # stop-option: 'iterations' - simulation stops only after given number of iterations,
    #              'steady-state' - simulation stops after steady-state is achieved or after given number of iterations,
    #              'period' - simulation stops after one period (when grid is equal to the initial one) or after given
    #                        number of iterations
    # underpopulation, overpopulation, rebirth - constants in game of life rules:
    # 1. alive cell dies if len(neighbors) < underpopulation or len(neighbors) > overpopulation
    # 2. dead cell rebirths if len(neighbors) == rebirth
    # boundary_conditions: 'traditional', 'toroidal'
    def simulation(self, N, stop_option='iterations', underpopulation=2, overpopulation=3, rebirth=3,
                   boundary_conditions='traditional'):
        self.setup_pictures(underpopulation=underpopulation, overpopulation=overpopulation,
                            rebirth=rebirth, boundary_conditions=boundary_conditions)
        initial_alive_cells, initial_dead_cells = self.get_states()
        self.period = 0
        set_period = True
        for i in range(N):
            alive_cells, dead_cells = self.get_states()
            self.update_pictures(stop_option, i)
            if not alive_cells:
                break
            new_alive_cells, new_dead_cells = self.simulation_step(underpopulation, overpopulation, rebirth,
                                                                   boundary_conditions)
            if set_period:
                if set(initial_alive_cells) == set(new_alive_cells):
                    self.period = i + 1
                    set_period = False
                    if stop_option == 'period':
                        break
            if stop_option == 'steady-state':
                if set(alive_cells) == set(new_alive_cells):
                    break
            for cell in new_alive_cells:
                self.game_state[cell] = 'Alive Cell'
            for cell in new_dead_cells:
                self.game_state[cell] = 'Dead Cell'
        self.drawing_machine.gif(fps=10)


if __name__ == '__main__':
    # Example 1 - glider, toroidal boundary conditions
    # test_lattice = GameOfLife.read_states_from_txt('glider.txt', alive_cell_symbol='o', dead_cell_symbol='.')
    # test_lattice.simulation(100, stop_option='iterations', underpopulation=2, overpopulation=3, rebirth=3,
    #                         boundary_conditions='toroidal')

    # Example 2 - pulsar, periodical pattern
    test_lattice = GameOfLife.read_states_from_txt('pulsar.txt', alive_cell_symbol='o', dead_cell_symbol='.')
    test_lattice.simulation(20, stop_option='iterations', underpopulation=2, overpopulation=3, rebirth=3,
                            boundary_conditions='traditional')
    print('Period:\n', test_lattice.period)

    # Example 3 - pattern with changed rules of game
    # test_lattice = GameOfLife.read_states_from_txt('changed_rules.txt', )
    # test_lattice.simulation(100, stop_option='iterations', underpopulation=4, overpopulation=3, rebirth=2,
    #                         boundary_conditions='toroidal')

    # Example 4 - pattern with customized signs of cells, steady-state
    # test_lattice = GameOfLife.read_states_from_txt('different_signs.txt', alive_cell_symbol='a', dead_cell_symbol='d')
    # test_lattice.simulation(1000, stop_option='steady-state', underpopulation=2, overpopulation=3, rebirth=3,
    #                         boundary_conditions='traditional')

    ###################################################################################################################
    # stop-option: 'iterations' - simulation stops only after given number of iterations,
    #              'steady-state' - simulation stops after steady-state is achieved or after given number of iterations,
    #              'period' - simulation stops after one period (when grid is equal to the initial one) or after given
    #                        number of iterations
    #
    # underpopulation, overpopulation, rebirth - constants in game of life rules:
    # 1. alive cell dies if len(neighbors) < underpopulation or len(neighbors) > overpopulation
    # 2. dead cell rebirths if len(neighbors) == rebirth
    #
    # boundary_conditions: 'traditional', 'toroidal'
    ###################################################################################################################
