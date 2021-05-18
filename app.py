# Import depedencies

import numpy as np
import pandas as pd
import datetime as dt

# Import Python SQL Toolkit

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Import flask, jsonify

from flask import Flask, jsonify 