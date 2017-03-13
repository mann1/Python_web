#!/usr/bin/env python
__author__ = "Nan Ma"
__copyright__ = "Copyright 2017, The Applause Interview Project"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Nan Ma"
__email__ = "nan_ma@mit.edu"
__status__ = "Production"

import web
import pdb
import unicodedata
from matching_tester import *

def display_results(country_list, dev_list):
    string = matching_obj.find_tester(country_list, dev_list)
    return string

urls = ('/', 'tutorial')
render = web.template.render('templates/')
app = web.application(urls, globals())
my_form = web.form.Form()
matching_obj = matching_tester('testers.csv', 'devices.csv', 'tester_device.csv', 'bugs.csv')


class tutorial:
    def GET(self):
        form = my_form()
        return render.tutorial(my_form(), "Your Results will be appeared on next page.")

    def POST(self):

        dev = web.input(Devices = [])
        dev = [x.encode('UTF8') for x in dev.Devices]
        cntry = web.input(Country = [])
        cntry = [y.encode('UTF8') for y in cntry.Country]
        return display_results(cntry, dev)

if __name__ == '__main__':

    app.run()
