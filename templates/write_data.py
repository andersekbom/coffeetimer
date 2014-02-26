#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import xml.etree.ElementTree as ET
import pysl
import os
import time
import sys
from datetime import datetime

pysl = pysl.PySL('76fab98f68ead993928b63dc9e2537df')
pysl.set_api('realtid')
siteID = sys.argv[1]

while True:

    theHour = datetime.now().hour
    if (theHour > 6 and theHour < 17):

        deps = pysl.get_departures(siteID,'xml')
        tree = ET.XML(deps.encode('utf-8'))
        next = string.split(tree[3][1][4].text)

        # TODO: Really ugly error handling below, make better!!

        try:
            minutes = next[3]
            text = next[4]
        except TypeError, IndexError, AttributeError:
            minutes = '0'
            text = 'Spring!'

        if minutes == 'Kort':
            minutes = '0'
            text = 'Spring!'

        if len(text) == 3:
            text = text + '&#160;'

        if len(minutes) == 2: # Check for minutes > 10
            num1 = minutes[0]
            num2 = minutes[1]
        else:
            num1 = '0'
            num2 = minutes

        if (num1 == '0' and num2 == '0'):
            num1 = 'N'
            num2 = 'u'

        print 'Writing: %s%s %s' % (num1,num2,text)
        sleep = 15

    else:
        text = 'Offline'
        num1 = '0'
        num2 = '0'
        sleep = 600
        print 'Sleeping...'        

    realTimeXML = '<RESULT><NUM1>%s</NUM1><NUM2>%s</NUM2><TEXT>%s</TEXT></RESULT>' % (num1, num2, text)
    f = open('static/' + siteID + '.xml','w')
    f.write(realTimeXML)
    f.close()

    time.sleep(sleep)
