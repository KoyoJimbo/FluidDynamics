import matplotlib.pyplot as plt
import numpy as np     # 結果表示に使いました。
import colorama
import precisely_domein
import UI_for_numbers
import schemes
import plot_modules
from colorama import Fore, Back, Style
from tqdm import tqdm
colorama.init(autoreset=True)

_ryki = 8

#============================================
#       線形の計算法から非線形の計算法へ
#
#           1.陽的な数値粘性項の付加         < 今回使っていません
#
#           2.高解像度風上法                 < 今回使いました
#============================================

# インスタンスを生成します。
UI_for_numbers   = UI_for_numbers.UIForNumbers()
plot_modules     = plot_modules.PlotModules()
precisely_domein = precisely_domein.Precisely(_ryki)
schemes          = schemes.Schemes()

# 各値をコマンドラインから取得します。
v                = UI_for_numbers.UI_v()
times            = UI_for_numbers.UI_times()
precisely        = UI_for_numbers.UI_precisely()
scheme           = UI_for_numbers.UI_scheme()

# 領域を取得します。
axis_x, u, u_new, fminus, fplus = precisely_domein.first_domein()

# グラフのタイトルを取得します。
plot_modules.plot_title_call(scheme, v)

# compute
for n in range(times):
    # plot
    plt.plot(axis_x, u)
    print(np.round(u, 1))
    # 次のuを算出
    for j in range(1,_ryki * 2 - 1):
        u_new[j]  = schemes.scheme_call(scheme, v, u, u_new, j, fminus, fplus)
    # 更新
    for j in range(1,_ryki * 2 - 1):
        u[j]     = u_new[j]
plt.show()
plt.figure()
