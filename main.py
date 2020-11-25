#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 17:46:13 2020

@author: mana
"""


from apiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
from utils import *

def main():
    words = input("Enter the keywords: ")
    words = words.split(",")
    order = input("Order by relevance or viewer count?: ")
    loop(words, order)

if __name__ == "__main__":
    main()