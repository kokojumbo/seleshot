#!/usr/bin/env python

'''
Created on Apr 13, 2012

@author: Marcin Gumkowski, Wojciech Zamozniewicz
'''

import seleshot

if __name__ == '__main__':
    s = seleshot.create()
    url = 'http://www.python.org'

    i = s.get_screen(url)
    i.cut_element(id = 'submit').save('cut1.png')
    i.cut_element(xpath = ".//*[@id='mainnav']/ul/li").save('cut2.png')
    i.cut_area(height = 100).save('area1.png')
    i.cut_area(200, 300, 250, 350).save('area2.png')
    i.cut_area(200, 300, 250, 350).cut_area(60, 60, 50, 50).save('area3.png')
    i.draw_frame(id = 'submit', padding = 10, color='yellow', size = 5).save('frame1.png')
    i.draw_frame(coordinates=(500, 500, 40, 50), color='green').save('frame2.png')
    i.cut_area(200, 300, 250, 350).draw_dot(coordinates = (50, 50), padding = 3, color = 'yellow', size = 5).draw_dot(
        coordinates = (60, 20), padding = 4, color = 'red', size = 10).save('dot1.png')
    i.draw_dot(id ='touchnav-wrapper', padding = 10, size = 100).save('dot2.png')
    i.draw_dot(id = 'submit', padding = 1, size = 3).save('dot3.png')
    s.close()

