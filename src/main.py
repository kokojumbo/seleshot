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
    i.cut_element(id = 'krowa').save('cut1')
    i.cut_element(xpath = ".//*[@id='mainnav']/ul/li").save('cut2.png')
    i.cut_area(height = 100).save('area1.png')
    i.cut_area(200, 300, 250, 350).save('area2.png')
    i.cut_area(200, 300, 250, 350).cut_area(60, 60, 50, 50).save('area3.png')
    i.draw_frame(id = 'submit', padding = 10, color = 'yellow', size = 5).save('frame1.png')
    i.draw_frame(coordinates = (500, 500, 40, 50), color = 'green').save('frame2.png')
    i.cut_area(200, 300, 250, 350).draw_dot(coordinates = (50, 50), padding = (10, 4), color = 'yellow',
                                            size = 5).draw_dot(
        coordinates = (60, 20), padding = (10, 4), color = 'red', size = 10).save('dot1.png')
    i.draw_dot(id = 'touchnav-wrapper', padding = (100, 200), size = 100, position = seleshot.Position.MIDDLE).save(
        "dot2M.png")
    i.draw_dot(id = 'submit', padding = (10, -10), size = 3, position = seleshot.Position.MIDDLE).save("dot3M.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (100, 100), size = 100,
               position = seleshot.Position.INSIDE_LEFT).save(
        "dot2IL.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.INSIDE_LEFT).save("dot3IL.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.INSIDE_RIGHT).save(
        "dot2IR.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.INSIDE_RIGHT).save("dot3IR.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.INSIDE_TOP).save(
        "dot2IT.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.INSIDE_TOP).save("dot3IT.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.INSIDE_BOTTOM).save(
        "dot2IB.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.INSIDE_BOTTOM).save(
        "dot3IB.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.OUTSIDE_LEFT).save(
        "dot2OL.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.OUTSIDE_LEFT).save("dot3OL.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.OUTSIDE_RIGHT).save(
        "dot2OR.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.OUTSIDE_RIGHT).save(
        "dot3OR.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.OUTSIDE_TOP).save(
        "dot2OT.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.OUTSIDE_TOP).save("dot3OT.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100,
               position = seleshot.Position.OUTSIDE_BOTTOM).save(
        "dot2OB.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.OUTSIDE_BOTTOM).save(
        "dot3OB.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.BORDER_LEFT).save(
        "dot2BL.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.BORDER_LEFT).save("dot3BL.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.BORDER_RIGHT).save(
        "dot2BR.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.BORDER_RIGHT).save("dot3BR.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.BORDER_TOP).save(
        "dot2BT.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.BORDER_TOP).save("dot3BT.png")

    i.draw_dot(id = 'touchnav-wrapper', padding = (10, 4), size = 100, position = seleshot.Position.BORDER_BOTTOM).save(
        "dot2BB.png")
    i.draw_dot(id = 'submit', padding = (10, 4), size = 3, position = seleshot.Position.BORDER_BOTTOM).save(
        "dot3BB.png")
    s.close()

