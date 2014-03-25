'''
Created on Oct 31, 2012

@author: perf
'''

import unittest
import seleshot


class Test(unittest.TestCase):
    def setUp(self):
        self.s = seleshot.create()
        url = 'http://www.python.org'
        self.i = self.s.get_screen(url)

    def tearDown(self):
        self.s.close()

    def test_cut_element(self):
        self.assertNotEqual(self.i.cut_element("submit"), None)

        self.assertRaises(Exception, self.i.cut_element, "wrongid")

        self.assertNotEqual(self.i.cut_element(xpath = ".//*[@id='mainnav']/ul/li"), None)

        self.assertRaises(Exception, self.i.cut_element, None, ".//*[@id='wrongid']/ul/li")

        ii = self.i.cut_element("submit")
        self.assertRaises(Exception, ii.cut_element, 'submit')

    def test_cut_area(self):
        d = self.i.cut_area(0, 0, 150, 250)
        self.assertNotEqual(d, None)

        d = self.i.cut_area(height = 100)
        self.assertEqual(d.image.size[1], 100)

        d = self.i.cut_area(0, 0, 150, 250)
        self.assertEqual(d.image.size, (250, 150))

        d = self.i.cut_area(200, 300, 250, 350)
        self.assertEqual(d.image.size, (350, 250))

if __name__ == "__main__":
    unittest.main()
