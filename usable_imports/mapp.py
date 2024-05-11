#can it work if min max are swapped?

def mapp(value, min, max, n_min, n_max):
    p_a = (value-min) * 100 / (max-min)
    perc = p_a / 100
    out = int(perc * (n_max-abs(n_min)))
    return out

if __name__ == '__main__':
	a = 12
	b = 30
	print(mapp(20, a, b, 0, 100))