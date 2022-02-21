# -*- coding: utf-8 -*-

import copy


class Interval(object):

    def __init__(self, lower_bound: int, upper_bound: int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __eq__(self, other):
        return (self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound)

    def __lt__(self, other):
        return self.comes_before(other)

    def __gt__(self, other):
        return other.comse_before(other)

    def __cmp__(self, other):
        if self == other:
            result = 0
        elif self.comes_before(other):
            result = -1
        else:
            result = 1
        return result

    def comes_before(self, other) -> bool:
        if self == other:
            result = False
        elif self.lower_bound < other.lower_bound:
            result = True
        elif self.lower_bound > other.lower_bound:
            result = False
        elif self.upper_bound < other.upper_bound:
            result = True
        elif self.upper_bound > other.upper_bound:
            result = False
        else:
            result = False

        return result

    def overlaps(self, other):
        if self == other:
            result = True
        elif other.comes_before(self):
            result = other.overlaps(self)
        elif other.lower_bound <= self.upper_bound:
            result = True
        else:
            result = False
        return result

    def join(self, other):
        if self.overlaps(other):
            if self.lower_bound <= other.lower_bound:
                lbound = self.lower_bound
            else:
                lbound = other.lower_bound
            
            if self.upper_bound >= other.upper_bound:
                ubound = self.upper_bound
            else:
                ubound = other.upper_bound

            return Interval(lbound, ubound)


class BaseIntervalList(object):

    def __init__(self, items=[]):
        self.intervals = []
        self._add(Interval(items[0], items[1]))
        self.intervals.sort()

    def _add(self, obj):
        new_intervals = []
        for i in self.intervals:
            if i.overlaps(obj):
                obj = obj.join(i)
            else:
                new_intervals.append(i)
        new_intervals.append(obj)
        self.intervals = new_intervals
        self.intervals.sort()


class IntervalList(BaseIntervalList):

    def __init__(self, items=[]):
        super().__init__(items=items)

    def __repr__(self) -> str:
        return super().__repr__()

    def print(self):
        return ",".join(["[{}, {})".format(obj.lower_bound, obj.upper_bound) for obj in self.intervals])

    def add(self, obj):
        interval = Interval(obj[0], obj[1])
        super()._add(interval)


if __name__ == "__main__":
    r1 = IntervalList([1, 3])
    r1.add([2, 5])
    r1.add([10, 21])
    r1.add([21, 21])
    print(r1.print())