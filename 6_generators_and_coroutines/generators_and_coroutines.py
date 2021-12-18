def accepting_generator():
    x = 'first line'
    accepted = yield x
    print('accepting_generator():', accepted)


class ShowMeWhatYouGotException(Exception):
    pass


def average():
    counter = 0
    current_average = None
    entire_sum = 0
    elements = []
    while True:
        try:
            new_element = yield current_average
        except ShowMeWhatYouGotException:
            break
            # return elements  # also StopIteration will be thrown
        else:
            counter += 1
            entire_sum += new_element
            current_average = entire_sum / counter
            elements.append(new_element)

    return elements


def coroutine(wrappee):
    def wrapper(*args, **kwargs):
        object_wrappee = wrappee(*args, **kwargs)
        object_wrappee.send(None)
        return object_wrappee

    return wrapper


@coroutine
def initialize_me():
    x = 'I am initialized'
    accepted_value = yield x
    print('initialize_me():', accepted_value)


def simple_subgenerator():
    for letter in 'MIKHAIL':
        yield letter


def simple_delegator(subgenerator):
    for element in subgenerator:
        yield element


def accepting_subgenerator():
    while True:
        accepted_value = yield
        print('accepting_subgenerator():', accepted_value)


def accepting_delegator(subgenerator):
    while True:
        accepted_value = yield
        print('accepting_delegator():', accepted_value)
        subgenerator.send(accepted_value)


class SilentException(Exception):
    pass


def exception_subgenerator():
    while True:
        try:
            x = yield
            print('exception_subgenerator():', x)
        except StopSubgeneratorException:
            print('StopSubgeneratorException in subgenerator()')
            break
        except StopIteration:
            print('StopIteration in subgenerator()')
        except SilentException:
            print('SilentException in subgenerator()')

    print('subgenerator() is stopped')
    return 'returned from subgenerator()'


class StopSubgeneratorException(Exception):
    pass


def exception_delegator(subgenerator):
    while True:
        try:
            y = yield
            subgenerator.send(y)

        except StopSubgeneratorException as e:
            print('StopSubgeneratorException in delegator()')
            try:
                subgenerator.throw(e)
            except StopIteration as e2:
                print('StopIteration in inner try-except in delegator()')
                yield e2.value


def yield_from_delegator(subgenerator):
    # while True:
    #     try:
    #         data = yield
    #         subgenerator.send(data)
    #     except StopSubgeneratorException as e:
    #         subgenerator.throw(e)

    #  does not handle exception from subgenerator!
    #  Handles exceptions only from caller and throws
    #  it deeper in subgenerator, like in commented code above
    yield from subgenerator


if __name__ == '__main__':
    # ag = accepting_generator()
    # print('first:', ag.send(None))
    # print('second:', ag.send([1, 2, 3]))

    # a = average()
    # print('initializing generator:', a.send(None))
    # print('average =', a.send(5))
    # print('average =', a.send(6))
    # print('average =', a.send(9))
    # print('average =', a.send(10))
    # print('average =', a.send(1))
    # print('average =', a.send(1))
    # print('average =', a.send(1))
    # try:
    #     a.throw(ShowMeWhatYouGotException)
    # except StopIteration as e:
    #     print('StopIteration.value():', e.value)

    # im = initialize_me()
    # try:
    #     im.send((1, 2, 3))
    # except StopIteration:
    #     print('Ran out of iterations!')

    # ssg = simple_subgenerator()
    # sd = simple_delegator(ssg)
    #
    # try:
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    #     print(next(sd))
    # except StopIteration:
    #     print('Ran out of iterations!')

    # asg = accepting_subgenerator()
    # asg.send(None)
    # ad = accepting_delegator(asg)
    # ad.send(None)
    #
    # ad.send('Hey')
    # ad.send('what')
    # ad.send('do')
    # ad.send('you')
    # ad.send('want')
    # ad.send('from')
    # ad.send('me')
    # ad.send('?')

    # esg = exception_subgenerator()
    # esg.send(None)
    #
    # ed = exception_delegator(esg)
    # ed.send(None)
    #
    # try:
    #     print(ed.throw(StopSubgeneratorException))
    # except StopIteration as e:
    #     print('StopIteration in main():', e.value)

    esg2 = exception_subgenerator()
    yfd = yield_from_delegator(esg2)
    yfd.send(None)

    yfd.send('something')
    # yfd.throw(StopSubgeneratorException)
    yfd.throw(SilentException)