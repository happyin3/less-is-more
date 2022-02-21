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

    def __contains__(self, obj):
        if obj.lower_bound < self.lower_bound:
            in_lower = False
        elif obj.lower_bound >= self.lower_bound:
            in_lower = True

        if obj.upper_bound > self.upper_bound:
            in_upper = False
        elif obj.upper_bound <= self.upper_bound:
            in_upper = True

        return in_lower and in_upper

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
        if items:
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

    def _remove(self, obj):
        tmp = IntervalList()
        for i in self.intervals:
            if i.overlaps(obj):
                if i in obj:
                    pass
                elif obj in i:
                    tmp.add([i.lower_bound, obj.lower_bound])
                    tmp.add([obj.upper_bound, i.upper_bound])
                elif obj.comes_before(i):
                    tmp.add([obj.upper_bound, i.upper_bound])
                else:
                    tmp.add([i.lower_bound, obj.lower_bound])
            else:
                tmp.add([i.lower_bound, i.upper_bound])
        self.intervals = tmp.intervals


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

    def remove(self, obj):
        interval = Interval(obj[0], obj[1])
        super()._remove(interval)


if __name__ == "__main__":
    r1 = IntervalList([1, 3])
    r1.add([2, 5])
    r1.add([10, 21])
    r1.add([21, 21])
    print(r1.print())
    r1.remove([3, 17])
    r1.remove([17, 17])
    r1.remove([22, 25])
    print(r1.print())