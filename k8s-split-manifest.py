#!/usr/bin/env python3
# k8s-split-manifest by Brian Joseph Czapiga <brian@czapiga.com>

# Usage:
#   ./k8s-split-manifest.py manifest.yaml

import yaml
import os
import sys
import re
import json

def pushObject(objects, object):
  objectText = "\n".join(object)
  objectYaml = yaml.safe_load(objectText)
  if 'kind' in objectYaml:
    kind = objectYaml['kind'].lower()
    if 'metadata' in objectYaml:
      metadata = objectYaml['metadata']
      if kind not in objects:
        objects[kind] = []
      objects[kind].append(objectText)
      sys.stderr.write("INFO: Parsed " + kind + "/" + metadata['name'] + "\n")
    else:
      raise ValueError('missing metadata')
      return False
  else:
    raise ValueError('missing kind')
    return False
  return True

def main():
  if len(sys.argv) != 2:
    sys.stderr.write("Usage: " + sys.argv[0] + " [ manifest.yaml ]\n")
    sys.exit(1)

  manifestFile = sys.argv[1]
  if not os.path.exists(manifestFile):
    sys.stderr.write("ERROR: File not found: " + manifestFile + "\n")
    sys.exit(1)

  try:
    manifestFD = open(manifestFile, 'r')
  except IOError as e:
    sys.stderr.write("ERROR: Error opening file [" + manifestFile + "]: " + str(e.strerror) + "\n")
    sys.exit(1)
    
  manifestRaw = manifestFD.read().split("\n")
  manifestFD.close() 

  # compiled rexps

  # end of object
  eoo = re.compile('^---\s*')
  # comment
  comment = re.compile('^\s*\#.*')
  # empty lines
  el = re.compile('^\s*$')

  # objects
  objects = {}
  curObject = []

  # counters
  curObjectStartLine = -1
  linePos = -1
  warnings = 0

  for line in manifestRaw:
    # update line position
    linePos = linePos + 1
    # set start line for current object
    if curObjectStartLine < 0:
      curObjectStartLine = linePos
    # skip comments and empty lines
    if comment.match(line) or el.match(line):
      continue
    # end of object
    if eoo.match(line):
      if len(curObject) > 0:
        try:
          pushObject(objects, curObject)
        except ValueError as e:
          sys.stderr.write("WARN: Ignored object starting on line " + str(curObjectStartLine) + "]: " + str(e.message) + "\n")
          warnings = warnings + 1
      # flush object
      curObject = []
      curObjectStartLine = -1
      continue

    # append lines to objects
    curObject.append(line)

  # flush remaining object
  if len(curObject) > 0:
    try:
      pushObject(objects, curObject)
    except ValueError as e:
      sys.stderr.write("WARN: Ignored object starting on line " + str(curObjectStartLine) + "]: " + str(e.message) + "\n")
      warnings = warnings + 1

  # the reason this is done in two loops is that multiple objects of the same kind will
  # be placed in a directory of 'kind'/'name' while single objects will be placed in the current
  # directory as 'name'

  for kind in sorted(objects.keys()):
    if len(objects[kind]) == 1:
      objectText = objects[kind].pop()
      filename = kind + '.yaml'
      sys.stderr.write("INFO: Writing [" + str(filename) + "]\n")
      fdout = open(filename, "w")
      fdout.write(objectText + "\n")
      fdout.close()
      continue
    if not os.path.exists(kind):
      os.mkdir(kind)
    for object in objects[kind]:
      objectYaml = yaml.safe_load(object)
      name = objectYaml['metadata']['name']
      filename = re.sub('[^a-zA-Z0-9\.\-]','-', name) + '.yaml'
      sys.stderr.write("INFO: Writing [" + str(kind) + '/' + str(filename) + "]\n")
      fdout = open(str(kind) + '/' + str(filename), "w")
      fdout.write(object + "\n")
      fdout.close()

  if warnings > 0:
    sys.stderr.write("WARN: There w" + ("as" if warnings == 1 else "ere") + " " + str(warnings) + " warning" + ("s" if warnings > 1 else "") + "\n")

if __name__ == '__main__':
  main()
