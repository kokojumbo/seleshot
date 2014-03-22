#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Bartosz Alchimowicz
'''

import seleshot

if __name__ == '__main__':
    s = seleshot.create()
    xpath = ".//*[@id='mainnav']/ul/li"
    id = "submit"
    url = 'http://www.python.org'

    i = s.get_screen(url)
    i.cut_element(id = id).save('cut1.png')
    i.cut_element(xpath = xpath).save('cut2.png')
    i.cut_area(height = 100).save("area1.png")
    i.cut_area(200, 300, 250, 350).save('area2.png')
    i.cut_area(200, 300, 250, 350).cut_area(60, 60, 50, 50).save("area3.png")

    s.close()

