from flask import Flask, request, redirect
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Define a method that processes incoming calls
app.route('/voice', methods=['GET', 'POST'])
def voice():
    res = VoiceResponse()
    gather = Gather(action='/gather', num_digits=1, method='POST')
    gather.say('Welcome to customer support. Press 1 for account information. \
               Press 2 for technical support. Press 3 for billing queries')
    res.append(gather)
    return str(res)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
    response = request.values.get('digits')
    res = VoiceResponse()

    if response == 1:
        res.say('You have selected account information. Please wait \
                while we fetch your account information.')
        
    elif response == 2 or response == 3:
        res.redirect('/forward')
        
    else:
        res.say('Invalid choice. Please try again!')
        gather = Gather(action='/gather', num_digits=1, method='POST')
        gather.say('Welcome to customer support. Press 1 for account information. \
                Press 2 for technical support. Press 3 for billing queries')
        res.append(gather)
    return res


@app.route('/forward', methods=['GET', 'POST'])
def forward():
    res = VoiceResponse()
    res.say('Connecting you to a live agent')
    res.dial(+25495555416)
    return str(res)

if __name__ == "__main__":
    app.run(debug=True)