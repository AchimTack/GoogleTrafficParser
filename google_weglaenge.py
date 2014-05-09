#-------------------------------------------------------------------------------
# Name:        google_wegelaenge.py
# Purpose:
#
# Author:      Achim
#
# Created:     19.05.2013
# Copyright:   (c) Achim 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def urlquery(url):
    # function cycles randomly through different user agents and time intervals to simulate more natural queries
    try:
        import urllib2
        import random
        from random import choice
        import time

        sleeptime = float(random.randint(1,6))/5
        time.sleep(sleeptime)

        agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
        'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02',
        'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Mozilla/3.0',
        'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3',
        'Mozilla/5.0 (Linux; U; Android 0.5; en-us) AppleWebKit/522+ (KHTML, like Gecko) Safari/419.3',
        'Opera/9.00 (Windows NT 5.1; U; en)']

        agent = choice(agents)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', agent)]
        #print agent

        html = opener.open(url).read()

        return html

    except:
        print "fehler in urlquery"

def routenlaenge(url):
    import urllib2
    import matplotlib
    from datetime import datetime

    d = datetime.now()
    timestamp = d.strftime('%Y-%m-%d %H:%M:%S')

    try:
        html =  urlquery(url)

        dauer = html.split('<span>Bei aktueller Verkehrslage: ')[1].split(' Minuten</span>')[0].replace('\n','')
        dauer = int(dauer)
    except Exception as e:
        print e
        dauer = 99999

    werte = (timestamp, dauer)

    return(timestamp, dauer)


from datetime import datetime
import time
import csv

routenurls = [('http://goo.gl/maps/v4oMp','Route 1'),
('http://goo.gl/maps/WMCVL','Route 2')
]

d = datetime.now()
filename = d.strftime('%Y-%m-%d_%H%M%S')
ofile  = open('data/'+filename+'.csv', "wb")

while True:
    try:
        for route in routenurls:
            url = route[0]
            ofile  = open('data/'+filename+'.csv', "a")
            routenwerte = routenlaenge(url)
            wert = (route[1],routenwerte[0],routenwerte[1])
            writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, lineterminator = '\n')
            writer.writerow(wert)
            print " Kassel " + str(wert)
            ofile.close()

    except Exception as e:
        print e

    time.sleep(300)

ofile.close()