#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on May 5, 2011

@author: Radoslaw Palczynski, Grzegorz Bilewski et al.
'''

import sys
import argparse
import tempfile
import Image
import ImageDraw
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from types import MethodType


def create(driver = None):
    # hiding everything from the world, buahaha ^_^

    def check_url(url):
        if not isinstance(url, basestring):
            raise ValueError("i don't understand your url :(")

        if url[:7] != "http://":
            raise ValueError("http protocol is required")

        return url

    def get_web_element_by_id(driver, id):
        element = None
        try:
            element = driver.find_element_by_id(id)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_by_xpath(driver, xpath):
        element = None
        try:
            element = driver.find_element_by_xpath(xpath)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_box_size(web_element):
        location = web_element.location
        size = web_element.size
        left = location['x']
        right = location['x'] + size['width']
        top = location['y']
        down = location['y'] + size['height']
        # box of region to crop
        box = (left, top, right, down)
        return box

    class ScreenShot(object):
        def __init__(self, driver):
            self.driver = driver

        def get_screen(self, url = None):
            """
            Get specified screen(s)

            @param url: web page to capture (including http protocol, None to reuse loaded webpage)
            """

            if url is not None:
                url = check_url(url)
                self.driver.get(url)
            elif self.driver.current_url == "about:blank":
                raise Exception("No page loaded")

            return get_screen(self.driver)

        def close(self):
            self.driver.close()

    class ImageContainer(object):

        def __init__(self, image, driver, cut = False):
            self.cut = cut
            self.driver = driver
            if image is None:
                raise Exception("Please provide an image.")
            elif isinstance(image, Image.Image):
                self.image = image
            else:
                self.tempfd = image
                self.image = Image.open(self.tempfd)

        def cut_element(self, id = None, xpath = None):
            """
            Crop one element by id or xpath
            return ImageContainer
            :param id:
            :param xpath:
            """
            if self.cut is True:
                raise Exception('You cannot cut more elements')
            elif (id is None) and (xpath is None):
                raise Exception("Please provide id or xpath.")
            elif id is not None:
                my_element = get_web_element_by_id(self.driver, id)
                box = get_web_element_box_size(my_element)
                new_image = self.image.crop(box)
                return ImageContainer(new_image, self.driver, True)
            elif xpath is not None:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                box = get_web_element_box_size(my_element)
                new_image = self.image.crop(box)
                return ImageContainer(new_image, self.driver, True)

        def cut_area(self, x = 0, y = 0, height = None, width = None):
            """
            Crop page vertically from a given point to a given size (in px)
            return ImageContainer
            :param x:
            :param y:
            :param height:
            :param width:
            """
            if height is None:
                height = self.image.size[1] - y
            if width is None:
                width = self.image.size[0] - x

            box = (x, y, width + x, height + y)
            new_image = self.image.crop(box)
            return ImageContainer(new_image, self.driver, True)

        def draw_dot(self, id = None, xpath = None, coordinates = None, padding = 0, color = None, size = None):
            """
            Draw a red dot on the left of a given element (resize image to add space on left if required)
            coordinates = (x, y) - center of a dot
            Use PIL to draw elements, no JavaScript allowed.
            return ImageContainer
            :param id:
            :param xpath:
            :param coordinates:
            :param padding:
            :param color:
            :param size:
            """
            if color is None:
                color = 'red'
            if size is None:
                size = 0
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if (id is None) and (xpath is None) and (coordinates is None):
                raise Exception("Please provide id or xpath.")
            elif id is not None and self.cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                # box = get_web_element_box_size(my_element)
                # box = [box[0], box[1], box[2], box[3]]

                # TODO It's difficult to add an empty space for a dot
            elif xpath is not None and self.cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                # box = get_web_element_box_size(my_element)
                # box = [box[0], box[1], box[2], box[3]]

                # TODO It's difficult to add an empty space for a dot
            elif coordinates is not None:
                box = (coordinates[0] - size - padding,
                       coordinates[1] - size,
                       coordinates[0] + size - padding,
                       coordinates[1] + size)

                draw.ellipse(box, fill = color, outline = color)

                return ImageContainer(new_image, self.driver)
            del draw

        def draw_frame(self, id = None, xpath = None, coordinates = None, padding = None, color = None, size = None):
            """
            Draw a frame around a given element
            coordinates = (x, y, width, height) - middle of a dot
            Use PIL to draw elements, no JavaScript allowed.
            return ImageContainer
            :param id:
            :param xpath:
            :param coordinates:
            :param padding:
            :param color:
            :param size:
            """
            if color is None:
                color = 'red'
            if size is None:
                size = 0
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if (id is None) and (xpath is None) and (coordinates is None):
                raise Exception("Please provide id or xpath.")
            elif id is not None and self.cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                box = get_web_element_box_size(my_element)
                box = [box[0], box[1], box[2], box[3]]
                if padding is not None:
                    box[0] = box[0] - padding
                    box[1] = box[1] - padding
                    box[2] = box[2] + padding
                    box[3] = box[3] + padding
                frame = ((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]), (box[0], box[1]))
                draw.line(frame, fill = color, width = size)
                return ImageContainer(new_image, self.driver)
            elif xpath is not None and self.cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                box = get_web_element_box_size(my_element)
                box = [box[0], box[1], box[2], box[3]]
                if padding is not None:
                    box[0] = box[0] - padding
                    box[1] = box[1] - padding
                    box[2] = box[2] + padding
                    box[3] = box[3] + padding
                frame = ((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]), (box[0], box[1]))
                draw.line(frame, fill = color, width = size)

                return ImageContainer(new_image, self.driver)
            elif coordinates is not None:
                box = list()
                box.append(coordinates[0] - (int(coordinates[2] / 2)))
                box.append(coordinates[1] - (int(coordinates[3] / 2)))
                box.append(coordinates[0] + (int(coordinates[2] / 2)))
                box.append(coordinates[1] + (int(coordinates[3] / 2)))

                if padding is not None:
                    box[0] = box[0] - padding
                    box[1] = box[1] - padding
                    box[2] = box[2] + padding
                    box[3] = box[3] + padding
                frame = ((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]), (box[0], box[1]))
                draw.line(frame, fill = color, width = size)
                return ImageContainer(new_image, self.driver)
            del draw

        def save(self, filename):
            """
            Save to a filename
            :param filename:
            """
            self.image.save(filename, "PNG")
            return self

        def close(self):
            self.driver.close()

    def get_screen(driver):
        """
        :param driver:
        :return:
        """
        tempfd = tempfile.NamedTemporaryFile(mode = 'w+t', delete = False)
        driver.save_screenshot(tempfd.name)
        temp_filename = tempfd.name
        tempfd.close()
        return ImageContainer(temp_filename, driver)

    #########################
    #          body         #
    #########################

    if driver is None:
        # no parameter provided, create the default driver

        return ScreenShot(webdriver.Firefox())
    elif isinstance(driver, WebDriver):
        # an instance of a class/webdriver
        # will add get_screen to it

        if "get_screen" not in dir(driver):
            driver.get_screen = MethodType(get_screen, driver, driver.__class__)

        return driver
    elif isinstance(driver, WebDriver) is False and isinstance(driver, type) is True:
        # a class
        # will create an instance and rerun create function to add get_screen function

        return create(driver())
    else:
        raise Exception("There is something strange with the driver, will you check it?")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Takes a screen shot of a web page.')
    parser.add_argument('-u', '--url', dest = "url", help = "url to web page (including http protocol)",
                        required = True)
    parser.add_argument('-i', '--ids', dest = "ids",
                        help = "list of ids on the web page separated by a space character",
                        nargs = '+')
    parser.add_argument('-x', '--xpath', dest = "xpath",
                        help = "list of xpath on the web page separated by a space character", nargs = '+')
    parser.add_argument('-d', '--path', dest = "path", help = "path to save directory; default as run script",
                        default = ".")
    parser.add_argument('-r', '--remoteUrl', dest = "remoteUrl", help = "url of selenium-server-standalone")
    # parser.add_argument('-f', '--format', dest="format", help="choose a code's output [opt: xml, json]", default=None)

    args = parser.parse_args()

    if args.url[:7] != "http://":
        print sys.argv[0] + ": error: argument -u/--url requires http protocol"
        sys.exit(2)

    if args.remoteUrl:
        s = create(webdriver.Remote(command_executor = args.remoteUrl, desired_capabilities = {
            "browserName": "firefox",
            "platform": "ANY",
        }))
        s.get(args.url)
        s.get_screen(args.ids, args.xpath, args.path)
    else:
        s = create()
        s.get_screen(args.url, args.ids, args.xpath, args.path)
    s.close()


