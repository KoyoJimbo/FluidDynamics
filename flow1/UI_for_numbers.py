import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

import sys

class UIForNumbers:
    def __init__(self):
        pass

    #  例外処理 for imput
    def parrot_no_v(self, q):
        assert -1 <= q <= 1, Fore.RED + "x shulde be between -1 and 1"
    def parrot_positive_number(self, q):
        assert 0  <= q,      Fore.RED + "x shulde be a positive number"
    def parrot_precisely(self, q):
        assert 1  <= q, Fore.RED + "x shulde be 1 or more"
    def parrot_scheme(self, q):
        assert 0  <= q <= 4, Fore.RED + "x shulde be a between 0 and 4"
    def parrot_graph(self, q):
        assert 0  <= q <= 1, Fore.RED + "x shulde be a between 0 and 1"

    # input v
    def UI_v(self):
        try:
            v = float(input("クーラン数vを決めて下さい。(-1~1): "))
        except ValueError:
            print(Fore.RED + "[Error]:数値を入力して下さい")
            sys.exit()
        self.parrot_no_v(v)
        return v

    # input times
    def UI_times(self):
        try:
            times = int(input("計算回数を決めて下さい。: "))
        except ValueError:
            print(Fore.RED + "[Error]:数値を入力して下さい")
            sys.exit()
        self.parrot_positive_number(times)
        return times

    # input precisely
    def UI_precisely(self):
        try:
            precisely = int(input("精度(正数)を決めて下さい。: "))
        except ValueError:
            print(Fore.RED + "[Error]:数値を入力して下さい")
            sys.exit()
        self.parrot_precisely(precisely)
        return precisely

    # input scheme
    def UI_scheme(self):
        try:
            print("0---one_precisely")
            print("1---FTCS")
            print("2---Lax_Wendroff")
            print("3---Lax_friedrich")
            scheme = int(input("スキームを決めて下さい。: "))
        except ValueError:
            print(Fore.RED + "[Error]:数値を入力して下さい")
            sys.exit()
        self.parrot_scheme(scheme)
        return scheme

    # input scheme
    def UI_graph(self):
        try:
            print("0---点")
            print("1---折れ線")
            graph = int(input("グラフを決めて下さい。: "))
        except ValueError:
            print(Fore.RED + "[Error]:数値を入力して下さい")
            sys.exit()
        self.parrot_graph(graph)
        return graph
