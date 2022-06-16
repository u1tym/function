from function import Function as fnc

def main():

	f = fnc("x^2 + 3x - 2 + y")
	v = f.value("x=2, y=1")

	print(v)	# 9


if __name__ == '__main__':

    main()

