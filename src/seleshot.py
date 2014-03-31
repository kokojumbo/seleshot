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

    """

    :param driver:
    :return: :raise:
    """

    def check_url(url):
        """
        Check provided url is valid.
        :rtype : string
        :param url: URL - string
        :return: Valid URL  :raise: ValueError
        """
        if not isinstance(url, basestring):
            raise ValueError("i don't understand your url :(")

        if url[:7] != "http://":
            raise ValueError("http protocol is required")

        return url

    def get_web_element_by_id(driver, id):
        """
        Get web element by id.
        :rtype : WebElement
        :param driver: WebDriver
        :param id: id to find WebElement
        :return: WebElement from WebDriver
        """
        element = None
        try:
            element = driver.find_element_by_id(id)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_by_xpath(driver, xpath):
        """
        Get web element by xpath.
        :rtype : WebElement
        :param driver: WebDriver
        :param xpath: xpath to find WebElement
        :return: WebElement from WebDriver
        """
        element = None
        try:
            element = driver.find_element_by_xpath(xpath)

            if not element.is_displayed() or element.size['width'] == 0 or element.size['height'] == 0:
                return None
        except NoSuchElementException:
            pass

        return element

    def get_web_element_box_size(web_element):
        """
        Get coordinates of the WebElement.
        :rtype :  tuple
        :param web_element: WebElement
        :return: coordinates of WebElement in box
        """
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
        :rtype : ImageContainer
        :param driver:
        :return: Screen shot
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

            elif id is not None:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
                new_image = self.image.crop(box)
                return ImageContainer(new_image, self.driver, True)
            elif xpath is not None:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise ValueError("There is no such element")
                box = get_web_element_box_size(my_element)
                new_image = self.image.crop(box)
                return ImageContainer(new_image, self.driver, True)
            else:
                raise ValueError("Please provide id or xpath.")

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

        def draw_dot(self, id = None, xpath = None, coordinates = None, padding = 0, color = None, size = None):
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
                    raise Exception("There is no such element")
                box = get_web_element_box_size(my_element)
            elif xpath is not None and self.cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise Exception("There is no such element")
                box = get_web_element_box_size(my_element)
            elif coordinates is not None:
                box = (coordinates[0] - size - padding,
                       coordinates[1] - size,
                       coordinates[0] + size - padding,
                       coordinates[1] + size)

                draw.ellipse(box, fill = color, outline = color)

                return ImageContainer(new_image, self.driver)
            else:
                del draw
                raise ValueError("Please provide id or xpath or coordinates")
            x = box[0] - 1
            y = box[1] + int((box[3] - box[1]) / 2)
            dot_box = (x - size - size - padding,
                       y - size,
                       x - padding,
                       y + size)
            if dot_box[0] < 0:
                additional_space = 2
                difference = -dot_box[0]
                bigger_image = Image.new('RGB',
                                         (new_image.size[0] + difference + additional_space, new_image.size[1]),
                                         "white")
                bigger_image.paste(new_image, (difference + additional_space, 0))

                dot_box = (dot_box[0] + difference + additional_space,
                           dot_box[1],
                           dot_box[2] + difference + additional_space,
                           dot_box[3])
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
            :rtype : ImageContainer
            :param id: id of a given element
            :param xpath: xpath of a given element
            :param coordinates: coordinates for a frame - coordinates = (x, y, width, height) - middle of a dot
            :param padding: padding between frame and element
            :param color: color of frame
            :param size: size of frame (thickness)
            """
            color = color if color is not None else "red"
            size = size if size is not None else 0
            new_image = self.image.copy()
            draw = ImageDraw.Draw(new_image)
            if id is not None and self.cut is False:
                my_element = get_web_element_by_id(self.driver, id)
                if my_element is None:
                    raise Exception("There is no such element")
                box = [i for i in get_web_element_box_size(my_element)]
            elif xpath is not None and self.cut is False:
                my_element = get_web_element_by_xpath(self.driver, xpath)
                if my_element is None:
                    raise Exception("There is no such element")
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



