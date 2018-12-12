"""
Pet Steps
Steps file for Pet.feature
"""
from os import getenv
import json
import requests
from behave import *
from compare import expect, ensure
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


WAIT_SECONDS = 30

@given('the following promotions')
def step_impl(context):
    """ Delete all Promotions and load new ones """
    headers = {'Content-Type': 'application/json'}
    context.resp = requests.delete(context.base_url + '/promotions/reset', headers=headers)
    expect(context.resp.status_code).to_equal(204)
    create_url = context.base_url + '/promotions'
    for row in context.table:
        data = {
            "promo_name": row['promo_name'],
            "goods_name": row['goods_name'],
            "category": row['category'],
	        "price": row['price'],
	        "discount": row['discount'],
            "available": row['available'] in ['True', 'true', '1']
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)


@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    expect(context.driver.title).to_contain(message)

@then('I should not see "{message}"')
def step_impl(context, message):
    error_msg = "I should not see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, error_msg)


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'promo_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select the "{element_name}" to "{choice}"')
def step_impl(context, element_name, choice):
    element_id = 'promo_' + element_name.lower()
    select = Select(context.driver.find_element_by_id(element_id))
    select.select_by_visible_text(choice)

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)


@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    expect(found).to_be(True)


##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by 'promo_' so the Name field has an id='promo_name'
# We can then lowercase the name and prefix with promo_ to get the id
##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = 'promo_' + element_name.lower()
    found = WebDriverWait(context.driver, WAIT_SECONDS).until(
        EC.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = 'promo_' + element_name.lower()
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@when('I reselect "{element_name}" to "{choice}"')
def step_impl(context, element_name, choice):
    element_id = 'promo_' + element_name.lower()
    select = Select(context.driver.find_element_by_id(element_id))
    select.select_by_visible_text(choice)