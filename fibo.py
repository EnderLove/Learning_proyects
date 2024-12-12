def fibo_series(n):
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    
    fibo_list = [0, 1]
    for i in range (2, n):
        fibo_list.append(fibo_list[i - 1] + fibo_list[i - 2])
    return fibo_list

    

n = int(input("Enter the range:"))

fibo_list = fibo_series(n)
print(fibo_list)

    