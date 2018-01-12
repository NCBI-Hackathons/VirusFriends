#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  interval.py
#
#  Copyright 2017 The University of Sydney
#  Author: Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  Description:
#
#  Version: 0



class Interval:

  def __init__(self, lower, upper, name):
    self.lower = lower
    self.upper = upper
    self.name = name
    self.order()
    self.frame = 1
    self.edges = {}
    self.links = {}

  def order(self):
    if self.lower > self.upper:
      tmp = self.lower
      self.upper = self.lower
      self.lower = tmp

  def update(self, attributes):
    self.frame = attributes.get('hframe', self.frame)

  def connect(self, interval, hsp):
    if hsp.hid not in self.edges:
      self.edges[hsp.hid] = []
    self.edges[hsp.hid].append(interval)
