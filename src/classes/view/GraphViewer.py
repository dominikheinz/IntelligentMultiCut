from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as Tk

from src.classes.controllers.SmoothController import SmoothController


class GraphViewer(Tk.Frame):
    __graph_width = 11
    __graph_height = 5
    __algo_data = None
    __title = ""

    def __init__(self, parent, algo_data, smooth, title):
        self.__title = title
        Tk.Frame.__init__(self, parent)
        self.__do_smooth = smooth
        self.__algo_data = algo_data
        self.parent = parent
        self.fig = self.show_algorithm_graphs()
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        self.pack(fill=Tk.BOTH, expand=1)


    def show_algorithm_graphs(self):
        fig = Figure()
        fig.suptitle(self.__title)
        fig.set_size_inches(self.__graph_width, self.__graph_height)

        axes = fig.add_subplot(111)
        axes.set_xlabel('Frame')
        axes.set_ylabel('Score')

        for k in range(0, len(self.__algo_data)):
            x_val = list(range(len(self.__algo_data[k])))
            y_val = self.__algo_data[k]

            if self.__do_smooth:
                SC = SmoothController(x_val, y_val)
                y_val_smooth = SC.smooth()
                axes.plot(x_val, y_val_smooth)
            else:
                axes.plot(x_val, y_val)

        return fig
