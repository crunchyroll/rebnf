# -*_ coding: utf-8 -*-

# chris 073015

from HTMLParser import HTMLParser
from argparse import ArgumentParser
from contextlib import closing
from os.path import commonprefix
from urllib2 import urlopen

base = 'http://www.fileformat.info/info/unicode/category'

htmlunescape = HTMLParser().unescape

# Get characters.
def getchars(cat):
  url = '%s/%s/list.htm' % (base,cat)
  chars = []
  with closing(urlopen(url)) as page:
    for line in page:
      if 'U+' not in line: continue
      idx = line.index('U+')
      idx += 2
      idx2 = line.index('<',idx)
      point = int(line[idx:idx2],16)
      descr = page.next().strip()
      # Eliminate <td> and </td>
      descr = descr[4:-5]
      descr = htmlunescape(descr)
      chars.append((point,descr))
  return chars

# Consolidate contiguous ranges.
def consolidate(chars):
  chars.sort()
  ranges = []
  last = start = None
  descrs = []
  for point,descr in chars:
    if start is None:
      start = point
    elif point != last + 1:
      end = last
      descr2 = commonprefix(descrs)
      if not descr2: descr2 = '?'
      ranges.append(((start,end),descr2))
      start = point
      descrs = []

    last = point
    descrs.append(descr)

  return ranges

def output(ranges):
  for (start,end),descr in ranges:
    out = ''
    if start == end:
      out += r'"\U%08x"' % start
      out += ' ' * 15
    else:
      out += r'"\U%08x" … "\U%08x"' % (start,end)
    out += ' | // %s' % descr
    print out

def main():
  descr = ('This script takes one or more names of Unicode character '
    'categories as command line arguments.  It fetches the '
    'character listings from fileformat.info and consolidates '
    'them into ranges with helpful comments.  The output is '
    'suitable for use in golang.org/x/exp/ebnf EBNF grammars.')
  parser = ArgumentParser(description=descr)
  parser.add_argument('cat',nargs='+',help='unicode category name')
  args = parser.parse_args()

  chars = []
  for cat in args.cat: chars.extend(getchars(cat))
  ranges = consolidate(chars)
  output(ranges)

main()
