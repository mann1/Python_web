#!/usr/bin/env python

__author__ = "Nan Ma"
__copyright__ = "Copyright 2017, The Applause Interview Project"
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Nan Ma"
__email__ = "nan_ma@mit.edu"
__status__ = "Production"

import csv
import operator
import os.path
import sys
from collections import OrderedDict

class matching_tester:
    tester_cnty_dict = dict()
    tester_name_dict = dict()
    device_ID_name = dict()
    tester_dev_dict = dict()
    expr_dict = dict()

    def __init__(self, tester_file, device_file, tester_dev_file, bug_file):
        #initialize tables for doing queries
        if (os.path.exists(tester_file)):
            with open(tester_file) as csvfile:
                testers = csv.DictReader(csvfile)
                for rows in testers:
                    if rows['country'] in self.tester_cnty_dict:
                        self.tester_cnty_dict[rows['country']].append(rows['testerId'])
                    else:
                        self.tester_cnty_dict[rows['country']] = [rows['testerId']]
        else:
            print "Tester file not found!"
            sys.exit(-1)

        if (os.path.exists(tester_file)):
            with open(tester_file) as csvfile:
                testers = csv.DictReader(csvfile)
                self.tester_name_dict = {rows['testerId']:(rows['firstName'],rows['lastName']) for rows in testers}
        else:
            print "Tester file not found!"
            sys.exit(-1)

        if (os.path.exists(device_file)):
            with open(device_file) as csvfile:
                devices = csv.DictReader(csvfile)
                self.device_ID_name = {rows['description']:rows['deviceId'] for rows in devices}
        else:
            print "Device file not found!"
            sys.exit(-1)

        if (os.path.exists(tester_dev_file)):
            with open(tester_dev_file) as csvfile:
                td_map = csv.DictReader(csvfile)
                for rows in td_map:
                    if rows['deviceId'] in self.tester_dev_dict:
                        self.tester_dev_dict[rows['deviceId']].append(rows['testerId'])
                    else:
                        self.tester_dev_dict[rows['deviceId']] = [rows['testerId']]
        else:
            print "Tester Dev file not found"
            sys.exit(-1)

        if (os.path.exists(bug_file)):
            with open(bug_file) as csvfile:
                expr = csv.DictReader(csvfile)
                for rows in expr:
                    if (rows['testerId'], rows['deviceId']) in self.expr_dict:
                        self.expr_dict[(rows['testerId'], rows['deviceId'])] = self.expr_dict[(rows['testerId'], rows['deviceId'])] + 1
                    else:
                        self.expr_dict[(rows['testerId'], rows['deviceId'])] = 1
        else:
            print "Bug file not found"
            sys.exit(-1)

    def __exit__(self):
        self.tester_cnty_dict.clear()
        self.tester_name_dict.clear()
        self.device_ID_name.clear()
        self.tester_dev_dict.clear()
        self.expr_dict.clear()

    def find_testerid_by_country(self, country):
        return self.tester_cnty_dict.get(country)

    def find_devID_by_name(self, dev_name):
        return self.device_ID_name.get(dev_name)

    def find_testername_by_id(self, ID):
        return self.tester_name_dict.get(ID)

    def find_testerid_by_device(self, dev):
        return self.tester_dev_dict.get(dev)

    def find_tester_expr(self, userid, devid):
        return self.expr_dict.get((userid, devid))

    def find_tester(self, country_list, device_list):
        #find the list of testers first
        avail_testers = list()
        for cnty in country_list:
            if (cnty == "All"):
                for cnty1, testers in self.tester_cnty_dict.items():
                    avail_testers = avail_testers + list(testers)
            else:
                avail_testers = avail_testers + list(self.find_testerid_by_country(cnty))

        #find available device
        avail_dev = list()
        for dev in device_list:
            avail_dev = avail_dev + list(self.find_devID_by_name(dev))

        #find avaliable tester and sort them by bug count
        filter_tester = dict()
        for tester in avail_testers:
            for dev in avail_dev:
                if (tester, dev) in self.expr_dict:
                    if tester in filter_tester:
                        filter_tester[tester] = filter_tester[tester] + self.expr_dict.get((tester, dev))
                    else:
                        filter_tester[tester] = self.expr_dict.get((tester, dev))

        sorted_filter_tester = OrderedDict(sorted(filter_tester.items(), key=operator.itemgetter(1),reverse=True))

        matched_tester=list()

        for tester, expr in sorted_filter_tester.items():
            name = [' '.join(list(self.find_testername_by_id(tester)))]
            matched_tester = matched_tester + name

        return matched_tester

    def print_dicts(self):
        print self.tester_cnty_dict
        print self.tester_name_dict
        print self.device_ID_name
        print self.tester_dev_dict
        print self.expr_dict
