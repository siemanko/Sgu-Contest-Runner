#!/usr/bin/env python

from xhpy.init import register_xhpy_module
register_xhpy_module('render')
from render import render_acm

def main():
    tasks = []
    teams = []
    open("test.html", "wt").write(render_acm(tasks, teams))
    return 0

if __name__ == "__main__":
    main()
