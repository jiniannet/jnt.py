# -*- coding: utf-8 -*-
environment = {}
data = None
resolver = []
loader = None

__all__ = ["environment", "data", "resolver", "loader",
           "resolve"]


def resolve(parser, tc): 
    for r in resolver:
        if r == None:
            continue
        t = r.parse(parser, tc)
        if t != None:
            t.first = tc[0]
            if len(t.children) == 0:
                t.last = tc[-1]
            else:
                if t.children[-1].last == None:
                    t.last = t.children[-1].first
                else:
                    t.last = t.children[-1].last
                if tc[-1].compare(t.last) > 0:
                    t.last = tc[-1]
            return t
    return None
