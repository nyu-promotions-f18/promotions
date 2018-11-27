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

Scenario: search promotions with name Christmas
    When I visit the "Home Page"
    And I set the "name" to "Christmas"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Christmas" in the results
    And I should not see "BlackFriday" in the results
    And I should not see "CyberMonday" in the results

Scenario: search promotions in category Females
    When I visit the "Home Page"
    And I set the "category" to "Females"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Females" in the results
    And I should not see "Kids" in the results
    And I should not see "Kitchen" in the results

Scenario: search available promotions
    When I visit the "Home Page"
    And I select the "available" to "True"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "true" in the results
    And I should not see "false" in the results

