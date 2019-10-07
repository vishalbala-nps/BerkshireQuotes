# BerkshireQuotes

An Alexa Skill which gives quotes by Warren Buffett and Charlie Munger

## Setup Instructions:
Start by cloning the repository on to your local machine with the following command:
```bash
git clone https://github.com/vishalbala-nps/BerkshireQuotes.git
```
### Configuration in Alexa Dev Console:
* First, we need to go to this page: https://developer.amazon.com/alexa/console/ask Then, we shoul click on "Create Skill" button

* Then, Enter a name for the skill, select the language as "English (IN)", select "Custom" in the Model Selection

* For Backend Resources, select "Provison your Own"

* After that, on the sidebar, select "JSON Editor" under "Interaction Model".

* Then Import the "skill.json" file on to the JSON Editor

* Now, Select "Endpoint" on the sidebar and click on "AWS Lambda ARN". Now, keep this screen open as we now need to configure in AWS
    
### AWS Configuration
#### Setup Lambda Function
* Login into your AWS Account. Then, change our server to "Ireland". Then, under "All Services" and under "Compute", click on "Lambda"

* Then here, click on "Create Function". Here, enter a function name, set the Runtime to "Python 3.6" and under Permissons, select "Create a new role with basic Lambda permissions"

* Then we will be greeted with another screen. Scroll down until you see "Function Code". Set the Handler to "lambda_function.lambda_handler". Then, delete all the existing code and copy-paste the "lambda_function.py" inside the "lambda" folder in this repository

##### Integrate the Lambda function with Amazon Alexa
* Now, under Designer, select "Add Trigger". Then under the drop-down, select "Alexa Skills Kit". Then, enable Skill ID Verification. Copy the Skill ID from the Alexa dev console and select "Submit"

* Now, copy the ARN and paste it under the "Default Region" in the Alexa dev console

##### Attach policies for Amazon DynamoDB to the Lambda Function
* Now, we need to attach policies for Amazon DynamoDB to the Lambda Function. For this, go to https://console.aws.amazon.com/iam/home/ Then, here select Roles. Then, select the role for our Lambda Function. Mostly, it will be named like: <name-of-lambda-function>-role-<pre-generated-id>

* Here, select "Attach policies" and add the "AWSLambdaDynamoDBExecutionRole" policy and the "AmazonDynamoDBFullAccess"

#### Setup DynamoDB Tables
* Now, we need to setup Amazon DynamoDB Tables. Go to: https://eu-west-1.console.aws.amazon.com/dynamodb/home/ Then, click on "Create table"

##### Setup Authors table
* Now, for name of table, enter "Authors" and type "AuthorId" as Primary Key and select it as Number. Now click on Create.

* Now, after the table has been created, click on "Items" and click on "Create Item"

* Here, on the text box which says "value", enter the Author ID. Which in this case is 1

* Then click on the plus sign and select Insert. Under this, select "String" and in Field, enter it as "AuthorName". Now, enter an author's name under value. In this case, Warren Buffett. After this, select Save

* Do this for all other Authors. Do note that the "AuthorId" MUST be unique

##### Setup Quotes table
* Now, for name of table, enter "Quotes" and type "QuoteID" as Primary Key and select it as Number. Now click on Create.

* Now, after the table has been created, click on "Items" and click on "Create Item"

* Here, on the text box which says "value", enter the Quote ID. Which in this case is 1

* Then click on the plus sign and select Insert. Under this, select "Number" and in Field, enter it as "AuthorID". Now, enter the author's id from the previous table

* Now, again click on the plus sign and select Insert. Under this, select "String" and in Field, enter it as "Quote". Now, enter a Quote from that author. After this, select Save

* Do this for all other Quotes. Do note that the "QuoteID" MUST be unique
