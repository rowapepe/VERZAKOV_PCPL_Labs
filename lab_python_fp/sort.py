#Вывод: [123, 100, -100, -30, 30, 4, -4, 1, -1, 0]

data = [4, -30, 100, -100, 123, 1, 0, -1, -4]

if __name__ == '__main__':
    result = sorted(data, key = abs, reverse=True)
    print(result)

    result_with_lambda = sorted(data, key = lambda x: -abs(x))
    print(result_with_lambda)