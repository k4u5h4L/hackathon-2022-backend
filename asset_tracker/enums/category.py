from __future__ import annotations

from enum import Enum

class CategoryType(object):
    def __init__(self, title: str, types: list = [], description: str = ""):
        self.title = title
        self.types = types
        self.description = description
    def __repr__(self):
        return f'CategoryType({self.title}, {self.description}, {self.types})'

class Category(Enum):
    LAPTOP = CategoryType("Laptop", ["Windows", "Mac"], "A portable laptop for the work.")
    CHARGER = CategoryType("Laptop's Charger", ["Windows", "Mac"], "A laptop charger for your laptop.")
    MOBILE = CategoryType("Mobile", ["Android", "iOS"], "A mobile phone to test SDK builds.")
    HEADPHONES = CategoryType("Headphones", ["Boat", "JBL"], "A Wireless Headphones.")
    WEBCAM = CategoryType("Webcam", ["Logitech"], "An external webcam for the montior.")
    MOUSE = CategoryType("Mouse", ["Logitech", "Zebornics"], "A portable wireless mouse for the work.")
    KEYBOARD = CategoryType("Keyboard", ["Logitech", "Zebornics"], "A portable wireless keyboard for the work.")

    @classmethod
    def choices(cls):
        return [(key.value.title, key.name) for key in cls]

    @classmethod
    def category_choices(cls, category: Category):
        return [(type, type.upper()) for type in category.value.types]

