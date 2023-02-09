# a*x^2 + b*x + c = 0
a = int(input('a = '))
b = int(input('b = '))
c = int(input('c = '))
D = b ** 2 - 4 * a * c
if D < 0:
    print('Уравнение не имеет действительных корней.')
elif D == 0:
    x = -b / (2 * a)
    print(f'x = {x}')
else:
    x1 = (-b - D ** 0.5) / (2 * a)
    x2 = (-b + D ** 0.5) / (2 * a)
    print(f'x1 = {x1}')
    print(f'x2 = {x2}')