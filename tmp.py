import functools


def do_potegi(podstawa, wykladnik):
    return podstawa ** wykladnik


def do_kwadratu(podstawa):
    return do_potegi(podstawa, 2)


print(do_kwadratu(4))

do_kwadratu1 = functools.partial(do_potegi, wykladnik=2)
print(do_kwadratu1(4))
