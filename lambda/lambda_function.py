import json
import boto3
from boto3.dynamodb.conditions import Key
import logging
import random
import traceback




aDict={}
logger = logging.getLogger()
logger.setLevel(logging.INFO)
qTable = []
qTablesize = 0



def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def on_launch(event, context):
    global qTable, qTablesize, aDict
    aTable = []
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('Quotes')
        lqtable = table.scan()
        qTable = lqtable['Items']
        qTablesize = lqtable['Count']
    
        table = dynamodb.Table('Authors')
        latable = table.scan()
        aTable = latable['Items']
        
    
        for item in aTable:
            laid = item['AuthorId']
            print(laid)
            aDict[laid] = item
    
        return question("Berkshire Quotes",getquotes("initial") )
    except:
        traceback.print_exc()
        return statement("Berkshire Quotes", "Sorry, an error occured while accessing our servers. Please try a little later.","Sorry, an error occured while accecing our servers. Please Try again later.")

def statement(title, body, text):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, text)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)
    
def question(title, retVal):
    
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(retVal['message'])
    speechlet['card'] = build_SimpleCard(title, retVal['qwname'])
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, retVal['att'])

def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response
    
def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech
    

def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card
    
def yes_intent(event, context):
    lfname = event['session']['attributes']['fname']
    if lfname == 'getAuthName':
        att = {'aid' : 0 , 'fname':'getAuthDes'}
        authid = int(event['session']['attributes']['aid'])
        aname = aDict[authid]['AuthorName']
        authdes = aDict[authid]['AuthorDescription']
        retVal={}
        retVal['message'] =getAuthDes(event)
        retVal['qwname'] = aname + " is the "+authdes
        retVal['att'] = att
        return question("Author Details",retVal)
    else:
        return question("Berkshire Quotes", getquotes("continue"))

def fallback(event, context):
    att = {'aid' : 0 , 'fname':'none'}
    print("In fallback")
    retVal={}
    retVal['message'] = "Sorry, I did not get that! Would you like another quote?"
    retVal['qwname'] = "Sorry, I did not get that! Would you like another quote?"
    retVal['att'] = att
    return question("Berkshire quotes",retVal )
    
def no_intent(event, context):
    return statement("Thanks!", "Thanks for using Berkshire Quotes! Hope to see you soon!", "Thanks for using Berkshire Quotes!")
        
def stopskill():
    return statement("Thanks!", "Thanks for using Berkshire Quotes! Hope to see you soon!", "Thanks for using Berkshire Quotes!")
    
def startskill():
    global qTable, qTablesize, aDict
    aTable = []
    try:
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
        table = dynamodb.Table('Quotes')
        lqtable = table.scan()
        qTable = lqtable['Items']
        qTablesize = lqtable['Count']
    
        table = dynamodb.Table('Authors')
        latable = table.scan()
        aTable = latable['Items']
        
    
        for item in aTable:
            laid = item['AuthorId']
            print(laid)
            aDict[laid] = item
    
        return question("Berkshire Quotes",getquotes("initial") )
    except:
        traceback.print_exc()
        return statement("Berkshire Quotes", "Sorry, an error occured while accessing our servers. Please try a little later.","Sorry, an error occured while accecing our servers. Please Try again later.")

    
def intent_router(event, context):
    intent = event['request']['intent']['name']
    print(intent)
    if intent == "AMAZON.YesIntent":
        return yes_intent(event, context)
    if intent == "AMAZON.NoIntent":
        return no_intent(event, context)
    if intent == "startskill":
        return startskill()
    # Required Intents
    if intent == "AMAZON.CancelIntent":
        return stopskill()
    if intent == "AMAZON.HelpIntent":
        return help_intent()
    if intent == "AMAZON.FallbackIntent":
        return fallback(event, context)
    if intent == "AMAZON.StopIntent":
        return stopskill()


        
def getAuthDes(event):
    authid = int(event['session']['attributes']['aid'])
    authdes = aDict[authid]['AuthorDescription']

    aname = aDict[authid]['AuthorName']
    print(aname)
    
    return aname + " is the "+authdes + ". Would you like another quote?"
    
def getAuthName(event):
    authid = int(event['session']['attributes']['aid'])
    authname = aDict[authid]['AuthorName']
    return "Would you like to know about " + authname
    
def getquotes(mode):
    
    att = {'aid' : 0 , 'fname':'none'}
    
    retVal = {"att":{},"qwname":"","message":""}
    rnum = random.randint(0, qTablesize - 1)
    resp = qTable[rnum]['Quote']
    logger.info(qTable[rnum])
    
    aid = int(qTable[rnum]['AuthorID'])
    
    logger.info("Vishal: From getquotes() mode:"+mode + " Response:"+resp+" Author ID: "+str(aid))
    author = aDict[aid]
    logger.info("Vishal: Author Json: "+str(author))
    auth = author['AuthorName']
    att['aid'] = aid
    att['fname'] = 'getquotes'
    
    retVal['att'] = att
    retVal['qwname'] = resp + "\n -" + auth
    if mode == "initial":
        retVal['message'] = "Hello! Welcome to Berkshire Quotes! Here's a quote from " + auth + ", " + resp + ". Would you like another quote?"
    else:
        retVal['message'] = "Ok, here's another quote from " + auth + ", " + resp + ". Would you like another quote?"
       
    return retVal
    
