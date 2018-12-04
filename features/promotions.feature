Feature: The promotions service back-end
    As a Promotion Manager
    I need a RESTful catalog service
    So that I can keep track of all the promotions

Background:
    Given the following promotions
        | id | promo_name  | goods_name | category | price| discount  | available |
        |  1 | BlackFriday | LEGO       | Kids     | 100  | 20      |   True      |
        |  2 | CyberMonday | Dress      | Females  | 300  | 100     |   True      |
        |  3 | Christmas   | Dishes       | Kitchen  | 50   | 5       |   False      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Promotion RESTful Service" in the title
    And I should not see "404 Not Found"

#################################
############# Read ##############
#################################

Scenario: Read a promotion
    When I visit the "Home Page"
    And I set the "Category" to "Kids"
    And I press the "Search" button
    Then I should see "BlackFriday" in the results
    And I should not see "Christmas" in the results

##################################
############ Create ##############
##################################

Scenario: Create a Promotion
    When I visit the "Home Page"
    And I set the "id" to "1"
    And I set the "name" to "New Promotion"
    And I set the "goods_name" to "Toy"
    And I set the "category" to "Kids"
    And I set the "price" to "100"
    And I set the "discount" to "20"
    And I select the "available" to "True"
    When I press the "Create" button
    Then I should see the message "Success"
    And I should not see "404 Not Found"

##################################
############  List  ##############
##################################

Scenario: List all the Promotion
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "BlackFriday" in the results
    And I should see "CyberMonday" in the results
    And I should see "Christmas" in the results

#################################
############  Query #############
#################################

Scenario: Search promotions with name Christmas
    When I visit the "Home Page"
    And I set the "name" to "Christmas"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Christmas" in the results
    And I should not see "BlackFriday" in the results
    And I should not see "CyberMonday" in the results

Scenario: Search promotions in category Females
    When I visit the "Home Page"
    And I set the "category" to "Females"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Females" in the results
    And I should not see "Kids" in the results
    And I should not see "Kitchen" in the results

Scenario: Search available promotions
    When I visit the "Home Page"
    And I select the "available" to "True"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "true" in the results
    And I should not see "false" in the results

#################################
############ Update #############
#################################

Scenario: Update a Promotion 
    When I visit the "Home Page"
    And I set the "id" to "1"
    And I press the "Retrieve" button
    Then I should see "BlackFriday" in the "name" field
    And I should see "LEGO" in the "goods_name" field
    And I should see "Kids" in the "category" field
    And I should see "True" in the "available" field
    When I change "name" to "NewYear"
    And I change "goods_name" to "candle"
    And I change "category" to "Home"
    And I reselect "available" to "False"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "id" to "1"
    And I press the "Retrieve" button
    Then I should see "NewYear" in the "name" field
    And I should see "candle" in the "goods_name" field
    And I should see "Home" in the "category" field
    And I should see "False" in the "available" field

# Scenario: Update promotion with invalid id
#     When I visit the "Home Page"
#     And I set the "id" to "30"
#     And I press the "Retrieve" button
#     Then I should get a response code "404"
#     When I visit "Home Page"
#     Then I will not see a promotion with "id" as "30"

#################################
############ Delete #############
#################################

Scenario: Delete a Promotion
    When I visit the "Home Page"
    And I set the "id" to "1"
    And I press the "Retrieve" button
    Then I should see "BlackFriday" in the "name" field
    And I should see "LEGO" in the "goods_name" field
    And I should see "Kids" in the "category" field
    And I should see "True" in the "available" field
    When I press the "Delete" button
    Then I should see the message "Promotion with ID [1] has been Deleted!"
    When I press the "Retrieve" button
    Then I should see the message "Promotion with id '1' was not found."

#############################################
############ Action: Delete All #############
#############################################


Scenario: Action-Delete all promotions in service
    When I send a DELETE request to '/promotions/reset'
    Then I should see the message " "
    When I visit the "Home Page"
    Then There should be "0" promotions


