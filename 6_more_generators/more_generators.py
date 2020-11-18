def generator1():
    print('ready to receive message...')
    message = yield
    print('generator1 received:', message)
    return 'this string can be returned only as value in exception StopIteration'


g1 = generator1()
print('INITIALISING GENERATOR1:')
g1.send(None)
print('GENERATOR1 IS NOW READY TO TAKE SMTH')

try:
    g1.send('MESSAGE')
except StopIteration as e:
    print('RETURNED FROM GENERATOR1:', e.value)

print('\n\n')
#=================================================================



class ExceptionToBreakLoopInGenerator2(Exception):
    pass


def generator2():
    print('ready to receive message...')
    while True:
        try:
            message = yield
            print('generator2 received:', message)
        except ExceptionToBreakLoopInGenerator2:
            print('infinite loop is about to be broken')
            break

    print('this line executes only when StopIteration is about to be raised')
    return 'this string can be returned only as value in exception StopIteration'


g2 = generator2()
print('INITIALISING GENERATOR2:')
g2.send(None)
print('GENERATOR2 IS NOW READY TO TAKE SMTH')
g2.send('MESSAGE #1')
g2.send('MESSAGE #2')
g2.send('MESSAGE #3')

try:
    g2.throw(ExceptionToBreakLoopInGenerator2)
except StopIteration as e:
    print('RETURNED FROM GENERATOR2:', e.value)

print('\n\n')
#=================================================================


class ShowMeWhatYouGot(Exception):
    pass


def coroutine(generator):
    def wrapper(*args, **kwargs):
        instance = generator(*args, **kwargs)
        instance.send(None)
        return instance

    return wrapper


@coroutine
def calculate_average():
    counter = 0
    summ = 0
    numbers = dict()
    average = None
    while True:
        try:
            current = yield average
        except ShowMeWhatYouGot:
            print('Okay, I will show you')
            break
        else:
            counter += 1
            summ += current
            average = round(summ / counter, 1)
            if current not in numbers:
                numbers[current] = 1
            else:
                numbers[current] += 1
    return average, numbers


sg = calculate_average()

print(sg.send(2))
print(sg.send(4))
print(sg.send(7))
print(sg.send(1))
print(sg.send(10))
print(sg.send(1))
print(sg.send(2))
print(sg.send(10))
print(sg.send(100))
print(sg.send(100))

try:
    sg.throw(ShowMeWhatYouGot)
except StopIteration as e:
    print('GENERATOR RETURNED:', e.value)

print('\n\n')
#=================================================================


def subgen1():
    for k in 'string from subgen1()':
        yield k


def delegator1(g):
    for k in g:
        yield k


sb1 = subgen1()
d1 = delegator1(sb1)
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))
print(next(d1))

print('\n\n')
#=================================================================


class SomeException(Exception):
    pass


def subgen2():
    while True:
        try:
            message = yield
        except SomeException:
            print('broken by SomeException')
            break
        else:
            print('...............', message)
    return 'this string is returned from subgen2()'


def delegator2(g):
    try:
        while True:
            try:
                data = yield
                g.send(data)
            except SomeException as e:
                g.throw(e)
    except StopIteration as e:
        print('delegator2() caught StopIteration:', e.value)
    return 'StopIteration from delegator2()'


sb2 = subgen2()
sb2.send(None)

d2 = delegator2(sb2)
d2.send(None)

d2.send('MESSAGE1')
d2.send('MESSAGE2')
d2.send('MESSAGE3')

try:
    d2.throw(SomeException)
except StopIteration as e:
    print('CAUGHT:', e.value)

print('\n\n')
#=================================================================


def delegator3(g):
    result = yield from g
    print('delegator3() caught StopIteration:', result)


d3 = delegator3(subgen2())
d3.send(None)
d3.send('wow')
d3.send('hello')
d3.send('world')
try:
    d3.throw(SomeException)
except StopIteration as e:
    print('CAUGHT:', e.value)

print('\n\n')
#=================================================================


def delegator4(g):
    while True:
        try:
            data = yield
            g.send(data)
        except SomeException as outerException:
            try:
                g.throw(outerException)
            except StopIteration as exceptionFromSubgen:
                print('delegator4() caught StopIteration:', exceptionFromSubgen.value)


sb2 = subgen2()
sb2.send(None)

d4 = delegator4(sb2)
d4.send(None)

d4.send('MESSAGE1')
d4.send('MESSAGE2')
d4.send('MESSAGE3')
d4.throw(SomeException)
