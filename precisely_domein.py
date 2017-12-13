class Precisely:
    def __init__(self, _ryki):
        self.__ryki = _ryki

# 一次精度
    def first_domein(self):
        domein1 = self.__ryki * 2
        x1 = [per_x - self.__ryki for  per_x in range(domein1)]
        u      = [0 for per_x in range(domein1)] # 同じよ
        for per_x in range(self.__ryki):
            u[per_x] = 1
        unew   = [0 for per_x in range(domein1)]
        fminus = [0 for per_x in range(domein1)]
        fplus  = [0 for per_x in range(domein1)]
        # fminus -> f((j-1)/2)
        # fplus  -> f((j+1)/2)
        return x1, u, unew, fminus, fplus


# 一次精度以降

    # 指定された領域を作成:main
    def make_precisely(self, x, precisely, v, scheme):
        new_x = self.scheme_call_domein(x, 2, v, scheme) # ここで2次精度
        for now_precisely in range(3, precisely + 1):
            new_x = self.scheme_call_domein(new_x, now_precisely, v, scheme)
        return new_x

    # 各精度に対応する領域(配列)の大きさを返す
    def make_domein(self, precisely):
        domein = self.__ryki * 2
        if precisely == 2 :
            previous_domein = domein
        for i in range (precisely - 1):
            domein = domein * 2 - 1
            if i == precisely - 3:
                previous_domein = domein
        return domein, previous_domein

    # スキームを呼ぶ
    def scheme_call_domein(self, x, precisely, v, scheme):
        if  (scheme == 0):
            new_x = self.next_precisely_one_preci(x, precisely, v)
        elif(scheme == 1):
            new_x = self.next_precisely_FTCS_or_X(x, precisely)
        elif(scheme == 2):
            new_x = self.next_precisely_lax(x, precisely, v, 0)
        elif(scheme == 3):
            new_x = self.next_precisely_lax(x, precisely, v, 1)
        return new_x


    # 次の精度の領域を作る

    def next_precisely_FTCS_or_X(self, old_x, precisely):
        domein, previous_domein = self.make_domein(precisely)
        new_x = [0 for per_x in range(domein)]
        for per_x in range (previous_domein - 1):
            new_x[per_x * 2]     =         old_x[per_x]
            new_x[per_x * 2 + 1] =  0.5 * (old_x[per_x] + old_x[per_x + 1])
        new_x[domein - 1] = old_x[previous_domein - 1]
        return new_x

    def next_precisely_one_preci(self, old_x, precisely, v):
        domein, previous_domein = self.make_domein(precisely)
        key_up   = 0.5 * (v - abs(v)) / abs(v)
        key_down = 0.5 * (v + abs(v)) / abs(v)
        new_x = [0 for per_x in range(domein)]
        for per_x in range (previous_domein - 1):
            new_x[per_x * 2]     = old_x[per_x]
            new_x[per_x * 2 + 1] = \
                key_up * old_x[per_x + 1] + key_down * old_x[per_x]
        new_x[domein - 1] = old_x[previous_domein - 1]
        return new_x

    def next_precisely_lax(self, old_x, precisely, v, wend_or_fried):
        domein, previous_domein = self.make_domein(precisely)
        if  (wend_or_fried == 0): # wendroff
            a = v
        elif(wend_or_fried == 1): # friedrich
            a = 1/v

        key_up   = 1 - a
        key_down = 1 + a
        new_x = [0 for per_x in range(domein)]
        for per_x in range (previous_domein - 1):
            new_x[per_x * 2] = old_x[per_x]

            up   = old_x[per_x + 1]
            down = old_x[per_x]
            new_x[per_x * 2 + 1] = 0.5 * (key_up * up + key_down * down)

        new_x[domein - 1] = old_x[previous_domein - 1]
        return new_x



if __name__ == '__main__':
    precisely_module = Precisely(8)

    precisely = 2

    x1, u, unew, fminus, fplus = \
        precisely_module.preparation_for_one_precisely()
    print(x1)
    if precisely > 1:
        ax_x = precisely_module.make_precisely(x1, precisely)
        u    = precisely_module.make_precisely(u, precisely)
        print(ax_x)
        print(u)
