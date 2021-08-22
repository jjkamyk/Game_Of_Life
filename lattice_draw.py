import matplotlib.pyplot as plt
import matplotlib.patches as patch
import shutil
import os
import imageio as img


# LatticeDraw - class responsible for visualization purposes
# (drawing lattices, coloring the cells, saving graphics, creating gifs)

class LatticeDraw:

    def __init__(self, L):
        self.size = L
        self.fig, self.ax = plt.subplots()
        self.number_of_images = 0
        self.directory = "Results"
        self.file_names = []

    # this method draws basic lattice of size L
    def draw_lines(self):
        self.ax.set_xlim(-0.5, self.size + 0.5)
        self.ax.set_ylim(-0.5, self.size + 0.5)
        for step in range(0, self.size + 1):
            self.ax.axhline(y=step, xmin=0.5 / (self.size + 1), xmax=1.0 - 0.5 / (self.size + 1), linewidth=0.75,
                            color='k')
            self.ax.axvline(x=step, ymin=0.5 / (self.size + 1), ymax=1.0 - 0.5 / (self.size + 1), linewidth=0.75,
                            color='k')

    # this method colors square of given coordinates (x, y) and color
    def color_square(self, x, y, color):
        rect = patch.Rectangle((x, y), 1, 1, linewidth=0, edgecolor='none', facecolor=color)
        self.ax.add_patch(rect)

    # this method uses method color_square on a list of coordinates
    def color_squares(self, cells_to_color, color):
        for coordinates in cells_to_color:
            x_coordinate = coordinates[0]
            y_coordinate = coordinates[1]
            self.color_square(x_coordinate, y_coordinate, color)

    # to speed up the process of generating graphics we decided to remove patches before (clearing the lattice)
    def remove_squares(self):
        squares = list(self.ax.patches)
        for square in squares:
            square.remove()

    def show(self):
        plt.figure(self.fig.number)
        plt.show()

    # this method creates a directory for results
    def create_directory(self):
        try:
            shutil.rmtree(self.directory)
        except FileNotFoundError:
            pass
        os.mkdir(self.directory)

    def save(self):
        path = os.path.join(self.directory, 'step_{0:0>4}.png'.format(self.number_of_images))
        self.fig.savefig(path)
        self.number_of_images += 1
        self.file_names.append(path)

    def gif(self, fps=2):
        images = []
        path = os.path.join(self.directory, 'simulation.gif')
        for file_name in self.file_names:
            images.append(img.imread(file_name))
        img.mimsave(path, images, fps=fps)
