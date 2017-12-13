import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

import matplotlib.pyplot as plt

from tqdm import tqdm

import numpy as np     #結果表示に使いました。

_ryki = 8

#============================================
#       線形の計算法から非線形の計算法へ
#
#           1.陽的な数値粘性項の付加         < 今回使っていません
#
#           2.高解像度風上法                 < 今回使いました
#============================================

class Schemes:
    def __init__(self):
        pass

    def scheme_call(self, scheme, v, u, unew, times, fminus, fplus):
        if  (scheme == 0):
            self.minus_one_preci(v, u, times, fminus)
            self.plus_one_preci(v, u, times, fplus)
        elif(scheme == 1):
            self.minus_ftcs(v, u, times, fminus)
            self.plus_ftcs(v, u, times, fplus)
        elif(scheme == 2):
            self.minus_lax_wendroff(v, u, times, fminus)
            self.plus_lax_wendroff(v, u, times, fplus)
        elif(scheme == 3):
            self.minus_lax_friedrich(v, u, times, fminus)
            self.plus_lax_friedrich(v, u, times, fplus)
        unew[times] = u[times] - v * (fplus[times] - fminus[times])
        return unew[times]

    # ==== １次精度風上 ====
    # f(j - 1 / 2)
    def minus_one_preci(self, v, u, j, fminus):
        # if v > 0 : f[j] = 0.5 * u[j - 1] ** 2
        # if v < 0 : f[j] = 0.5 * u[  j  ] ** 2
        key_left   = 0.5 * (v + abs(v)) / abs(v) # 左から来るとき
        key_right  = 0.5 * (v - abs(v)) / abs(v) # 右から来るとき
        left       = 0.5 * u[j - 1] ** 2
        right      = 0.5 * u[  j  ] ** 2
        fminus[j]  = 0.5 * (key_right * right + key_left * left)

    # f(j + 1 / 2)
    def plus_one_preci(self, v, u, j, fplus):
        # if v > 0 : f[j] = 0.5 * u[  j  ] ** 2
        # if v < 0 : f[j] = 0.5 * u[j + 1] ** 2
        key_left   = 0.5 * (v + abs(v)) / abs(v)
        key_right  = 0.5 * (v - abs(v)) / abs(v)
        left       = 0.5 * u[  j  ] ** 2
        right      = 0.5 * u[j + 1] ** 2
        fplus[j]   = 0.5 * (key_right * right + key_left * left)


    # ==== Lax-Wendroff ====
    # f(j - 1 / 2)
    def minus_lax_wendroff(self, v, u, j, fminus):
        key_left   = 0.5 * (v + abs(v)) / abs(v)
        key_right  = 0.5 * (v - abs(v)) / abs(v)
        # f[  j  ] = 0.5 * u[  j  ] ** 2
        # f[j - 1] = 0.5 * u[j - 1] ** 2
        key_up     = 1 - v
        key_down   = 1 + v
        up         = 0.5 * u[  j  ] ** 2
        down       = 0.5 * u[j - 1] ** 2
        fminus[j]  = 0.5 * (key_up * up + key_down * down)
        fminus[j]  =  key_left * 0.5 * (key_up * up + key_down * down) + key_right * 0.5 * (key_up * down + key_down * up)

    # f(j + 1 / 2)
    def plus_lax_wendroff(self, v, u, j, fplus):
        key_left   = 0.5 * (v + abs(v)) / abs(v)
        key_right  = 0.5 * (v - abs(v)) / abs(v)
        # f[j + 1] = 0.5 * u[j + 1] ** 2
        # f[  j  ] = 0.5 * u[  j  ] ** 2
        key_up     = 1 - v
        key_down   = 1 + v
        up         = 0.5 * u[j + 1] ** 2
        down       = 0.5 * u[  j  ] ** 2
        fplus[j]   = key_left * 0.5 * (key_up * up + key_down * down) + key_right * 0.5 * (key_up * down + key_down * up)



    # === Lax-Friedrich ====
    # f(j - 1 / 2)
    def minus_lax_friedrich(self, v, u, j, fminus):
        key_left   = 0.5 * (v + abs(v)) / abs(v)
        key_right  = 0.5 * (v - abs(v)) / abs(v)
        # f[j - 1] = 0.5 * u[j - 1] ** 2
        # f[  j  ] = 0.5 * u[  j  ] ** 2
        key_up     = 1 - 1/v
        key_down   = 1 + 1/v
        up         = 0.5 * u[  j  ] ** 2
        down       = 0.5 * u[j - 1] ** 2
        fminus[j]  =  key_left * 0.5 * (key_up * up + key_down * down) + key_right * 0.5 * (key_up * down + key_down * up)


    # f(j + 1 / 2)
    def plus_lax_friedrich(self, v, u, j, fplus):
        key_left   = 0.5 * (v + abs(v)) / abs(v)
        key_right  = 0.5 * (v - abs(v)) / abs(v)
        # f[  j  ] = 0.5 * u[  j  ] ** 2
        # f[j + 1] = 0.5 * u[j + 1] ** 2
        key_up     = 1 - 1/v
        key_down   = 1 + 1/v
        up         = 0.5 * u[j + 1] ** 2
        down       = 0.5 * u[  j  ] ** 2
        fplus[j]   =  key_left * 0.5 * (key_up * up + key_down * down) + key_right * 0.5 * (key_up * down + key_down * up)


    # ======== FTCS ========
    # f(j - 1 / 2)
    def minus_ftcs(self, v, u, j, fminus):
        # f[j - 1] = 0.5 * u[j - 1] ** 2
        # f[  j  ] = 0.5 * u[  j  ] ** 2
        up         = 0.5 * u[  j  ] ** 2
        down       = 0.5 * u[j - 1] ** 2
        fminus[j]  = 0.5 * (up + down)


    # f(j + 1 / 2)
    def plus_ftcs(self, v, u, j, fplus):
        # f[  j  ] = 0.5 * u[  j  ] ** 2
        # f[j + 1] = 0.5 * u[j + 1] ** 2
        up         = 0.5 * u[j + 1] ** 2
        down       = 0.5 * u[  j  ] ** 2
        fplus[j]   = 0.5 * (up + down)


if __name__ == '__main__':
    import precisely_domein
    import UI_for_numbers

    precisely_domein = precisely_domein.Precisely(_ryki)
    UI_for_numbers = UI_for_numbers.UIForNumbers()
    flow = Schemes()

    #user interface
    v         = UI_for_numbers.UI_v()
    times     = UI_for_numbers.UI_times()
    precisely = UI_for_numbers.UI_precisely()
    scheme    = UI_for_numbers.UI_scheme()

    # define domein
    x1, u, unew, fminus, fplus = \
        precisely_domein.preparation_for_one_precisely()

    for n in range(times):
        # compute
        for j in range(1,_ryki * 2 - 1):
            # 非保存式による差分化
            # 線形の計算法から非線形の計算法へ
            unew[j] = flow.scheme_call(scheme, v, u, unew, j, fminus, fplus)

#            flow.minus(v, u, j)
#            flow.plus(v, u, j)
#            unew[j] = u[j] - v * (fplus[j] - fminus[j])
        for j in range(1,_ryki * 2 - 1):
            u[j]=unew[j]
        if precisely == 1:
            plt.plot(x1, u, "o")
        else:
            # 精度に応じたx軸配列を取得します。
            ax_x = precisely_domein.make_precisely(x1, precisely, v)
            # fj+1/2 = 0.5*(f(j+1)+f(j))
            u_plot    = precisely_domein.make_precisely(u,  precisely, v)
            plt.plot(ax_x, u_plot, "o", markersize=2)
        print(np.round(u, 1)) # show numeric values
    plt.show()
