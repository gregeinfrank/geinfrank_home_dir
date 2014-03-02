#!/usr/bin/env python

import commands
import re
import sys


def make_re(*msgs):
    return re.compile('(%s)' % '|'.join(msgs))

pyflakes_ignore = make_re('unable to detect undefined names')
pyflakes_warning = make_re(
    'imported but unused',
    'is assigned to but never used',
    'redefinition of unused',
)
pep8_ignore = ['E501', # line too long (82 > 79 characters)
               'E231', # missing whitespace after ','
               'W291', # trailing whitespace
               'E261', # at least two spaces before inline comment
               'E126', # continuation line over-indented for hanging indent
               'E123', # closing bracket does not match indentation of opening bracket's line
               'E702'] # multiple statements on one line (semicolon)

pep8_warning = make_re('.')


def run(cmd, ignore_re, warning_re):
    output = commands.getoutput(cmd)
    for line in output.splitlines():
        if ignore_re and ignore_re.search(line):
            continue
        elif ': ' in line and warning_re.search(line):
            line = '%s: WARNING %s' % tuple(line.split(': ', 1))
        print line

run('pyflakes %s' % sys.argv[1], pyflakes_ignore, pyflakes_warning)
print '## pyflakes above, pep8 below ##'
pep8_ignore = '--ignore=%s' % ','.join(pep8_ignore)
run('pep8 %s --repeat %s' % (pep8_ignore, sys.argv[1]), None, pep8_warning)
