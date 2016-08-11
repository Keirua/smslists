# -*- coding: utf-8 -*-
""" [commmented out to prevent coverage errors]
import plivo
import views

auth_id = "MANGVIYZY0ZMFIMTIWOG"
auth_token = "Yzc3OTgzZmU4MGIyNDI4ODgzMWE1MWExOWYxZTcx"

def plivo_out():

p = plivo.RestAPI(auth_id, auth_token)


params = {
    'src': views.reply_source,  # Sender's phone number with country code
    'dst': views.reply_destination,  # Receiver's phone Number with country code
    'text' : "u"+views.menu_text, # Your SMS Text Message - English
#   'text' : u"こんにちは、元気ですか？" # Your SMS Text Message - Japanese
#   'text' : u"Ce est texte généré aléatoirement" # Your SMS Text Message - French
    'url' : "", # The URL to which with the status of the message is sent
    'method' : 'POST' # The method used to call the url
}

response = p.send_message(params)

# Prints the complete response
print str(response)

# Sample successful output
# (202,
#       {
#               u'message': u'message(s) queued',
#               u'message_uuid': [u'b795906a-8a79-11e4-9bd8-22000afa12b9'],
#               u'api_id': u'b77af520-8a79-11e4-b153-22000abcaa64'
#       }
# )

# Prints only the status code
print str(response[0])

# Sample successful output
# 202

# Prints the message details
print str(response[1])

# Sample successful output
# {
#       u'message': u'message(s) queued',
#       u'message_uuid': [u'b795906a-8a79-11e4-9bd8-22000afa12b9'],
#       u'api_id': u'b77af520-8a79-11e4-b153-22000abcaa64'
# }

# Print the message_uuid
print str(response[1]['message_uuid'])

# Sample successful output
# [u'b795906a-8a79-11e4-9bd8-22000afa12b9']

# Print the api_id
print str(response[1]['api_id'])

# Sample successful output
# b77af520-8a79-11e4-b153-22000abcaa64
"""
