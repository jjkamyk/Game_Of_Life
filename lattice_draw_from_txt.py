from lattice_draw import LatticeDraw


# LatticeDrawFromTxt - class built upon the previous class LatticeDraw, responsible for visualization purposes
# (drawing lattices, coloring the cells, saving graphics, creating gifs)
class LatticeDrawFromTxt(LatticeDraw):

    # super() function allows us to execute __init__ from the upper class
    # we get all of the attributes from the upper class and we can proceed with them
    # 5 represents an arbitrary L, which has to be given, but it is not used anywhere further
    def __init__(self, size):
        super().__init__(5)
        self.size = size

    # this method is overwritten since the draw_lines from LatticeDraw is no longer sufficient
    # (LatticeDraw.draw_lines creates only square lattices, while the new method produces also rectangular lattices)
    def draw_lines(self):
        size_x = self.size[0]
        size_y = self.size[1]
        self.ax.set_xlim(-0.5, size_x + 0.5)
        self.ax.set_ylim(-0.5, size_y + 0.5)
        for step in range(0, size_x + 1):
            self.ax.axvline(x=step, ymin=0.5 / (size_y + 1), ymax=1.0 - 0.5 / (size_y + 1), linewidth=0.75,
                            color='k')
        for step in range(0, size_y + 1):
            self.ax.axhline(y=step, xmin=0.5 / (size_x + 1), xmax=1.0 - 0.5 / (size_x + 1), linewidth=0.75,
                            color='k')


if __name__ == '__main__':
    # Example - creating rectangular lattice using new method draw_lines
    test_lattice = LatticeDrawFromTxt((4, 5))
    test_lattice.draw_lines()
    test_lattice.show()
    # Example - creating square lattice using old method
    test_lattice_2 = LatticeDraw(4)
    test_lattice_2.draw_lines()
    test_lattice_2.show()
