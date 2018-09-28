def sum(m, n):
    if n<0:
        m, n = n, m
    for i in range(n):
        m += 1
    return m


def divide(m, n):
    i = -1
    if n==0:
        raise ZeroDivisionError()
    else:
        sign = -1 if m>0 and n<0 or m<0 and n>0 else 1
        n, m = abs(n), abs(m)

        while m>=0:
            m -= n
            i += 1

    return i if type(i) == str else i*sign
