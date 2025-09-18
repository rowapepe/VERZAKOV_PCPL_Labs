import sys
import math

def get_coef(index, prompt):
    try:
        coef_str = sys.argv[index]
    except:
        print(prompt)
        coef_str = input()
    coef = float(coef_str)
    return coef
    

def get_roots(a, b, c):
    result = []
    D = b*b - 4*a*c
    if D == 0.0:
        root = -b / (2.0*a)
        if root > 0:
            result.append(root)
            result.append(-root)
        elif root == 0:
            result.append(0)
    elif D > 0.0:
        sqD = math.sqrt(D)
        root1 = (-b + sqD) / (2.0*a)
        root2 = (-b - sqD) / (2.0*a)

        if root1 > 0:
            r = math.sqrt(root1)
            result.append(r)
            result.append(-r)
        elif root1 == 0:
            result.append(0)

        if root2 > 0:
            r = math.sqrt(root2)
            result.append(r)
            result.append(-r)
        elif root2 == 0:
            result.append(0)

    return result


def main():
    a = get_coef(1, 'Введите коэффициент А:')
    b = get_coef(2, 'Введите коэффициент B:')
    c = get_coef(3, 'Введите коэффициент C:')

    roots = get_roots(a,b,c)

    if not roots:
        print('Нет действительных корней')
    elif len(roots) == 1:
        print('Один корень: {}'.format(roots[0]))
    elif len(roots) == 2:
        print('Два корня: {} и {}'.format(roots[0], roots[1]))
    else:
        print('Четыре корня: {}, {}, {}, {}'.format(roots[0], roots[1], roots[2], roots[3]))
    

if __name__ == "__main__":
    main()