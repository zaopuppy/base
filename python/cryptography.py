#!/usr/bin/env python
# -*- coding: utf-8 -*-


def gcd_ex(a, b):
    """
    Implementation of Extended Euclidean Algorithm

    ax + by = GCD(a, b)

    return (gcd(a, b), x, y)
    """
    if a == b:
        return a

    r0, r1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while True:
        quo, rm = divmod(r0, r1)
        r0, r1 = r1, rm
        new_s = s0 - quo*s1
        s0, s1 = s1, new_s
        new_t = t0 - quo*t1
        t0, t1 = t1, new_t
        if rm == 0:
            break

    return r0, s0, t0


def gcd(a, b):
    return gcd_ex(a, b)[0]


def invert(a, m):
    """
    a*x = 1 (mod m)
    ax + my = 1
    """
    _, x, y = gcd_ex(a, m)
    return x % m


def main():
    print(gcd(7, 10))
    print(gcd_ex(7, 10))
    print(invert(7, 10))


if __name__ == "__main__":
    main()

