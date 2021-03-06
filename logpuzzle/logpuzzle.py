#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
def url_sort_key(url):
  """Used to order the urls in increasing order by 2nd word if present."""
  match = re.search(r'-(\w+)-(\w+)\.\w+', url)
  if match:
    return match.group(2)
  else:
    return url

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++

  url_lst = []
  notwice_url_lst = []
  # Read file
  with open(filename, 'r') as f:
    log_file = f.read()
    # Looking for the desired string
    if re.search(r'/edu/languages/google-python-class/images/puzzle/\w+-\w+\.\w+', log_file):
      log_list = (re.findall(r'/edu/languages/google-python-class/images/puzzle/\w+-\w+\.\w+', log_file))
    else:
      log_list = (re.findall(r'/edu/languages/google-python-class/images/puzzle/\w-\w+-\w+\.\w+', log_file))
    # Generate urlname
    name = re.search(r'code.\w+.\w+', filename)
    for item in log_list:
      url_lst.append('http://' + name.group(0) + item)
    # Sort URL
    url_lst.sort(key=url_sort_key)
    # Kill duplicates url(In this level I can use set, but I'm interested try another method)
    for x in url_lst:
      if len(notwice_url_lst) > 0:
        if x != notwice_url_lst[-1]:
          notwice_url_lst.append(x)
      else:
        notwice_url_lst.append(x)
    return notwice_url_lst


def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++

  # This code can create path right, but i don,t  understand ho it work

  # try:
  #   os.mkdir(dest_dir)
  # except OSError as e:
  #   if e.errno != errno.EEXIST:
  #       raise

  # Create path
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  x = os.path.abspath(dest_dir)
  # Downloads file
  n = 0
  list_files =[]
  for url_item in img_urls:
    urllib.urlretrieve(url_item, str(x) +'\img' + str(n))
    list_files.append(str(x) +'\img' + str(n))
    n += 1
    print "Retrieving..."
  # Create html file

  head = '<verbatim>\n<html>\n<body>\n'
  footer = '</body>\n</html>'
  with open(str(x)+'/index.html', 'w') as f:
    f.write(head)
    for file in list_files:
      f.write('<img src="' + file + '">')
    f.write(footer)





def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
