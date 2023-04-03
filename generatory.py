x = ['mama', 'tata', 'ja']
for e in x:
    print(e)

i = x.__iter__()
while True:
    try:
        e = i.__next__()
        print(e)
    except StopIteration:
        break


def funkcja_generator():
    print('start_generatora')
    yield 'mama'
    print('czekam1')
    yield 'tata'
    print('czekam2')
    yield 'ja'
    print('koniec')


for e in funkcja_generator():
    print('petla', e)

g = (i ** 2 for i in range(10))
print(g)
for e in g:
    print(e)


class GeneratorKlasa:
    def __init__(self, n=5):
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.n > 0:
            self.n -= 1
            return self.n
        else:
            raise StopIteration()

for e in GeneratorKlasa(5):
    print(e)

x = [1,2,3,4,5,6,7,8,9]

def dodaj_2(g):
    for i in g:
        yield i + 2

def do_kwadratu(g):
    for i in g:
        yield i ** 2

g1 = dodaj_2(x)
g2 = do_kwadratu(g1)
for i in g2:
    print(i)
    