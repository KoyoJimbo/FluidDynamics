import matplotlib.pyplot as plt

class PlotModules:
    def graph_call(self, graph, x, u):
        if   graph == 0:
            plt.plot(x, u, "o", markersize=2)
        elif graph == 1:
            plt.plot(x, u)


    # plot.titleの決定
    def plot_title_call(self, scheme, v):
        # 1次精度風上差分
        if   scheme == 0:
            self.one_preci_title(v)
        # FTCS
        elif scheme == 1:
            self.FTCS_title(v)
        # Lax-wendroff
        elif scheme == 2:
            self.LW_title(v)
        # Lax-Friedrich
        elif scheme == 3:
            self.lax_friedrich_title(v)


    def FTCS_title(self, v):
        plt.title("FTCS($ν = {:.3f}$)".format(v))
    def LW_title(self, v):
        plt.title("Lax-Wendroff($ν = {:.3f}$)".format(v))
    def one_preci_title(self, v):
        plt.title("1-order upwind($v = {:.3f}$)".format(v))
    def lax_friedrich_title(self, v):
        plt.title("Lax-Friedrich($v = {:.3f}$)".format(v))

