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


class Position():
    MIDDLE = 1
    INSIDE_LEFT = 2
    INSIDE_RIGHT = 3
    INSIDE_TOP = 4
    INSIDE_BOTTOM = 5
    OUTSIDE_LEFT = 6
    OUTSIDE_RIGHT = 7
    OUTSIDE_TOP = 8
    OUTSIDE_BOTTOM = 9
    BORDER_LEFT = 10
    BORDER_RIGHT = 11
    BORDER_TOP = 12
    BORDER_BOTTOM = 13


def create(driver = None):
    # hiding everything from the world, buahaha ^_^

    """

    :param driver:
    :return: :raise:
    """


    def check_url(url):
        # Check provided url is valid.
        # :param url: URL - string
        # :return: Valid URL  :raise: ValueError
        # :rtype : string

        if not isinstance(url, basestring):
            raise ValueError("i don't understand your url :(")

        if not url.startswith("http://"):
            raise ValueError("http protocol is required")

        return url

    def get_web_element_by_id(driver, id):
        # Get web element by id.
        # :param driver: WebDriver
        # :param id: id to find WebElement
        # :return: WebElement from WebDriver
        # :rtype : WebElement

        element = None
        try:
            element = driver.find_element_by_id(id)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_by_xpath(driver, xpath):
        # Get web element by xpath.
        # :param driver: WebDriver
        # :param xpath: xpath to find WebElement
        # :return: WebElement from WebDriver
        # :rtype : WebElement

        element = None
        try:
            element = driver.find_element_by_xpath(xpath)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_box_size(web_element):
        # Get coordinates of the WebElement.
        # :param web_element: WebElement
        # :return: coordinates of WebElement in box
        # :rtype :  tuple

        location = web_element.location
        size = web_element.size
        left = location['x']
        right = location['x'] + size['width']
        top = location['y']
        down = location['y'] + size['height']
        # box of region to crop
        box = (left, top, right, down)
        return box

    def get_screen(driver):
        """
        Get screen shoot and save it in a temporary file
        :param driver:
        :return: Screen shot
        :rtype : ImageContainer
        """
        tempfd = tempfile.NamedTemporaryFile(mode = 'w+t', delete = False)
        driver.save_screenshot(tempfd.name)
        temp_filename = tempfd.name
        tempfd.close()
        return ImageContainer(temp_filename, driver)

    class ScreenShot(object):
        def __init__(self, driver):
            self.driver = driver

        def get_screen(self, url = None):
            """
            Get specified screen(s)

            :param url: web page to capture (including http protocol, None to reuse loaded webpage)
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
            """
            Constructor for ImageContainer.
            :param image: In this parameter you can provide Image object or a path to Image
            :param driver: WebDriver object
            :param cut: True - image was cut one or more times, False - there were not any cut operation
            :rtype : ImageContainer
            """
            self.cut = cut
            self.driver = driver
            if image is None:
                raise ValueError("Image required")
            elif isinstance(image, Image.Image):
                self.image = image
            else:
                self.filename = image
                self.image = Image.open(self.filename)

        def cut_element(self, id = None, xpath = None):
            """
            Cut one element by id or xpath. After this operation you cannot cut more elements.
            return ImageContainer
            :param id: id of a given element
            :param xpath: xpath of a given element
            """
            if self.cut is True:
                raise RuntimeError('Element can be cut only once')
            if id is not None:
                element = get_web_element_by_id(self.driver, id)
            elif xpath is not None:
                element = get_web_element_by_xpath(self.driver, xpath)
            else:
                raise ValueError("Please provide id or xpath.")
            if element is None:
                raise ValueError("There is no such element")
            box = get_web_element_box_size(element)
            new_image = self.image.crop(box)
            return ImageContainer(new_image, self.driver, True)


        def cut_area(self, x = 0, y = 0, height = None, width = None):
            """
            Cut area from a given point to a given size (in px)
            return ImageContainer
            :param x: x coordinate for a point
            :param y: y coordinate for a point
            :param height: height of an area
            :param width: width of an area
            """
            height = height if height is not None else self.image.size[1] - y
            width = width if width is not None else self.image.size[0] - x
            box = (x, y, width + x, height + y)
            new_image = self.image.crop(box)
            return ImageContainer(new_image, self.driver, True)

        def draw_dot(self, id = None, xpath = None, coordinates = None, position = Position.MIDDLE, padding = (0, 0),
                     color = None, size = None):
            """
            For id and xpath:
                Draw a red dot on the left of a given element. (resize image to add space on left if it is required)
            For coordinates:
                Draw a red dot in a given point (x, y)
            return ImageContainer
            :param id: id of a given element
            :param xpath: xpath of a given element
            :param coordinates: coordinates = (x, y) - center of a dot
            :param padding: padding between dot and element
            :param color: color of dot
            :param size: size of dot
            """
            color = color if color is not None else "red"
            size = size if size is not None else 1
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)

            if id is not None and self.cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
            elif xpath is not None and self.cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
            elif coordinates is not None:
                box = (coordinates[0] - size + padding[0],
                       coordinates[1] - size + padding[1],
                       coordinates[0] + size + padding[0],
                       coordinates[1] + size + padding[1])

                draw.ellipse(box, fill = color, outline = color)

                return ImageContainer(new_image, self.driver)

            else:
                del draw
                raise ValueError("Please provide id or xpath or coordinates")

            # distances from borders
            border_x = int((box[2] - box[0]) / 2)
            border_y = int((box[3] - box[1]) / 2)
            # central point of element
            x = box[0] + border_x
            y = box[1] + border_y

            inside_left = 0
            inside_right = 0
            inside_top = 0
            inside_bottom = 0
            outside_left = 0
            outside_right = 0
            outside_top = 0
            outside_bottom = 0
            border_left = 0
            border_right = 0
            border_top = 0
            border_bottom = 0

            if position == Position.INSIDE_LEFT:
                inside_left = -border_x + size
            elif position == Position.INSIDE_RIGHT:
                inside_right = border_x - size
            elif position == Position.INSIDE_TOP:
                inside_top = -border_y + size
            elif position == Position.INSIDE_BOTTOM:
                inside_bottom = border_y - size
            elif position == Position.OUTSIDE_LEFT:
                outside_left = -border_x - size
            elif position == Position.OUTSIDE_RIGHT:
                outside_right = border_x + size
            elif position == Position.OUTSIDE_TOP:
                outside_top = -border_y - size
            elif position == Position.OUTSIDE_BOTTOM:
                outside_bottom = border_y + size
            elif position == Position.BORDER_LEFT:
                border_left = -border_x
            elif position == Position.BORDER_RIGHT:
                border_right = border_x
            elif position == Position.BORDER_TOP:
                border_top = -border_y
            elif position == Position.BORDER_BOTTOM:
                border_bottom = border_y

            dot_box = (
                x - size + inside_left + inside_right + outside_left + outside_right + border_left + border_right +
                padding[0],
                y - size + inside_top + inside_bottom + outside_top + outside_bottom + border_top + border_bottom +
                padding[1],
                x + size + inside_left + inside_right + outside_left + outside_right + border_left + border_right +
                padding[0],
                y + size + inside_top + inside_bottom + outside_top + outside_bottom + border_top + border_bottom +
                padding[1],)

            # add additional space for a dot
            if dot_box[0] < 0 or dot_box[1] < 0 or dot_box[2] > new_image.size[0] or dot_box[3] > new_image.size[1]:
                difference_left = -dot_box[0] if dot_box[0] < 0 else 0
                difference_top = -dot_box[1] if dot_box[1] < 0 else 0
                difference_right = dot_box[2] - new_image.size[0] if dot_box[2] > new_image.size[0] else 0
                difference_bottom = dot_box[3] - new_image.size[1] if dot_box[3] > new_image.size[1] else 0
                bigger_image = Image.new('RGB',
                                         (new_image.size[0] + difference_left + difference_right,
                                          new_image.size[1] + difference_top + difference_bottom),
                                         "white")
                bigger_image.paste(new_image, (difference_left, difference_top))
                dot_box = (dot_box[0] + difference_left,
                           dot_box[1] + difference_top,
                           dot_box[2] + difference_left,
                           dot_box[3] + difference_top)
                draw = ImageDraw.Draw(bigger_image)
                draw.ellipse(dot_box, fill = color, outline = color)
                return ImageContainer(bigger_image, self.driver)
            else:
                draw.ellipse(dot_box, fill = color, outline = color)
                return ImageContainer(new_image, self.driver)


        def draw_frame(self, id = None, xpath = None, coordinates = None, padding = None, color = None, size = None):
            """
            For id and xpath:
                Draw a frame around a given element
            For coordinates:
                Draw a frame for a given coordinates
            return ImageContainer
            :param id: id of a given element
            :param xpath: xpath of a given element
            :param coordinates: coordinates for a frame - coordinates = (x, y, width, height) - middle of a dot
            :param padding: padding between frame and element
            :param color: color of frame
            :param size: size of frame (thickness)
            :rtype : ImageContainer
            """
            color = color if color is not None else "red"
            size = size if size is not None else 0
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if id is not None and self.cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = [i for i in get_web_element_box_size(my_element)]
            elif xpath is not None and self.cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = [i for i in get_web_element_box_size(my_element)]
            elif coordinates is not None:
                box = [
                    coordinates[0] - int(coordinates[2] / 2),
                    coordinates[1] - int(coordinates[3] / 2),
                    coordinates[0] + int(coordinates[2] / 2),
                    coordinates[1] + int(coordinates[3] / 2)
                ]
            else:
                del draw
                raise ValueError("Please provide id or xpath or coordinates")
            if padding is not None:
                box[0] = box[0] - padding
                box[1] = box[1] - padding
                box[2] = box[2] + padding
                box[3] = box[3] + padding
            frame = ((box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3]), (box[0], box[1]))
            draw.line(frame, fill = color, width = size)
            return ImageContainer(new_image, self.driver)


        def save(self, filename):
            """
            Save to a filename
            :param filename: name of a file
            """
            self.image.save(filename, "PNG")
            return self


        def close(self):
            self.driver.close()


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
        s.get_screen(args.url, args.ids, args.xpath, args.path).save("c:/shot_example.png").save("c:/shot_examplxe.png")

    s.close()
