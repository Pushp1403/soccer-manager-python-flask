import re
import datetime
import locale
import random
import string
import pycountry

from flask import request
from config.errors import InputValidationError


def validate_country_name(country_name):
    """
    Validates the given country name using pycountry lib
    :param country_name: given country name
    :return: None if validation passes
    """
    try:
        pycountry.countries.lookup(country_name)
    except LookupError as e:
        raise InputValidationError(message="Invalid country name specified",
                                   payload={'country': country_name})


def format_url(uri):
    """returns the full url"""
    return f'{request.root_url}{uri}'


def generate_team_name():
    """
    Generates a random string
    :return: str
    """
    return ''.join(
        random.choices(string.ascii_uppercase +
                       string.digits, k=7)
    )


def adjust_market_value(ask_price):
    """
    Increase player's market value by a random factor in range (10, 100)
    :param ask_price: current ask_price
    :return: updated ask_price
    """
    percent_increase = random.randint(10, 100)
    increment = (percent_increase / 100) * ask_price
    return ask_price + increment


def currency_formatter(num):
    """
    Format currency as USD
    :param num: int
    :return: $ amount
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(num, grouping=True)


def player_age_generator():
    """Generate random age in range (18, 40)"""
    return random.randint(18, 40)


def format_error(e):
    """
    Format API error response
    :param e: exception object
    :return: JSON
    """
    if "password" in e.payload:
        del e.payload["password"]
    data = {
        "success": False,
        "timestamp": datetime.datetime.utcnow(),
        "request_uri": request.url,
        "request_payload": e.payload,
        "error": {
            "name": e.name,
            "response code": e.status_code,
            "description": e.message,
        }
    }
    return data, e.status_code


def format_generic_error(e):
    """
    Format API error response
    :param e: exception object
    :return: JSON
    """
    data = {
        "success": False,
        "timestamp": datetime.datetime.utcnow(),
        "request_uri": request.url,
        "error": {
            "description": str(e),
            "name": e.__class__.__name__
        }
    }
    return data, 500


def format_response(data, code):
    """
    Format success response
    :param data: json result
    :param code: response code
    :return: JSON
    """

    data = {
        "success": True,
        "timestamp": datetime.datetime.utcnow(),
        "request_uri": request.url,
        "data": data,
        "status_code": code,
    }

    return data


def is_valid_email(email_id):
    """
    Validate if the provided email is a valid email
    :param email_id: email ID
    :return: boolean
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email_id):
        raise InputValidationError(message="Invalid email ID",
                                   payload={"username": email_id})
