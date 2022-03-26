# -*- coding: utf-8 -*-

import copy


class Interval(object):

    def __init__(self, lower_bound: int, upper_bound: int):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __eq__(self, other):
        return (self.lower_bound == other.lower_bound and self.upper_bound == other.upper_bound)
        
    def __contains__(self, obj):
        if obj.lower_bound < self.lower_bound:
            in_lower = False
        elif obj.lower_bound == self.lower_bound:
            in_lower = True

        if obj.upper_bound > self.upper_bound:
            in_upper = False
        elif obj.upper_bound == self.upper_bound:
            in_upper = True

        return in_lower and in_upper

    def __and__(self, other):
        if self == other:
            result = Interval()
            result.lower_bound = self.lower_bound
            result.upper_bound = self.upper_bound
        elif self.comes_before(other):
            if self.overlaps(other):
                if self.lower_bound == other.lower_bound:
                    lower = self.lower_bound
                elif self.lower_bound > other.lower_bound:
                    lower = self.lower_bound
                else:
                    lower = other.lower_bound

                if self.upper_bound == other.upper_bound:
                    upper = self.upper_bound
                elif self.upper_bound < other.upper_bound:
                    upper = self.upper_bound
                else:
                    upper = other.upper_bound

                result = Interval(lower, upper)
            else:
                result = Interval()
        else:
            result = other & self

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

    def adjacent_to(self, other):
        if self.comes_before(other):
            if self.upper_bound == other.lower_bound:
                result = True
            else:
                result = False
        elif self == other:
            result = False
        else:
            result = other.adjacent_to(self)
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
        for i in items:
            self._add(i)
        self.intervals.sort()

    def __sub__(self, other):
        if not isinstance(other, BaseIntervalList):
            raise TypeError("")

        result = IntervalList(self)
        for j in other.intervals:
            tmp = IntervalList()
            for i in result.intervals:
                if i.overlaps(j):
                    if i in j:
                        pass
                    elif j in i:
                        if j.lower_bound != None:
                            tmp.add(Interval(i.lower_bound, j.lower_bound))
                        if j.upper_bound != None:
                            tmp.add(Interval(j.upper_bound, i.upper_bound))
                    elif j.comse_before(i):
                        tmp.add(j.upper_bound, i.upper_bound)
                    else:
                        tmp.add(i.lower_bound, j.lower_bound)
                else:
                    tmp.add(copy.deepcopy(i))
            result = tmp

        return self.__class__(result)

    def __and__(self, other):
        if not isinstance(other, BaseIntervalList):
            raise TypeError("")

        result = IntervalList()
        for j in other.intervals:
            for i in self.intervals:
                if i.overlaps(j):
                    if i in j:
                        result.add(copy.deepcopy(i))
                    elif j in i:
                        result.add(copy.deepcopy(j))
                    elif j.comes_before(i):
                        result.add(Interval(i.lower_bound, j.upper_bound))
                    else:
                        result.add(Interval(j.lower_bound, i.upper_bound))
        result = self.__class__(result)

        return result

    def _add(self, obj):
        if not isinstance(obj, Interval):
            raise TypeError("")

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
        for i in result.intervals:
            if i.overlaps(j):
                if i in j:
                    pass
                elif j in i:
                    if j.lower_bound != None:
                        tmp.add(Interval(i.lower_bound, j.lower_bound))
                    if j.upper_bound != None:
                        tmp.add(Interval(j.upper_bound, i.upper_bound))
                elif j.comse_before(i):
                    tmp.add(j.upper_bound, i.upper_bound)
            else:
                tmp.add(i.lower_bound, j.lower_bound)
            else:
                tmp.add(copy.deepcopy(i))
        result = tmp


class IntervalList(BaseIntervalList):

    def __init__(self):
        pass

    def print(self):
        pass

    def add(self, obj):
        BaseIntervalList._add(self, obj)

    def remove(self, obj):
        diff = self - IntervalList([obj])
        self.intervals = diff.intervals