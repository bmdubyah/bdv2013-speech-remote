import urllib2
import sys, os, pyaudio
from pocketsphinx import *
from sphinxbase.sphinxbase import *

sony_host = "<deviceIP>:50001"
user_agent  = "MyCustomRemote"
ctrl_path = "/upnp/control/IRCC"

commands = {
  "Confirm": "AAAAAwAAAhAAAAB8Aw==",
  "Up": "AAAAAwAAAhAAAAB4Aw==",
  "Down": "AAAAAwAAAhAAAAB5Aw==",
  "Right": "AAAAAwAAAhAAAAB7Aw==",
  "Left": "AAAAAwAAAhAAAAB6Aw==",
  "Home": "AAAAAgAAANAAAAAHAw==",
  "Options": "AAAAAwAAAhAAAABzAw==",
  "Return": "AAAAAwAAAhAAAAB9Aw==",
  "Num1": "AAAAAwAAAhAAAAAAAw==",
  "Num2": "AAAAAwAAAhAAAAABAw==",
  "Num3": "AAAAAwAAAhAAAAACAw==",
  "Num4": "AAAAAwAAAhAAAAADAw==",
  "Num5": "AAAAAwAAAhAAAAAEAw==",
  "Num6": "AAAAAwAAAhAAAAAFAw==",
  "Num7": "AAAAAwAAAhAAAAAGAw==",
  "Num8": "AAAAAwAAAhAAAAAHAw==",
  "Num9": "AAAAAwAAAhAAAAAIAw==",
  "Num0": "AAAAAwAAAhAAAAAJAw==",
  "Power": "AAAAAgAAAFAAAAAVAw==",
  "Display": "AAAAAwAAAhAAAAAYAw==",
  "VolumeUp": "AAAAAgAAAFAAAAASAw==",
  "VolumeDown": "AAAAAgAAAFAAAAATAw==",
  "Mute": "AAAAAgAAAFAAAAAUAw==",
  "Audio": "AAAAAwAAAhAAAAASAw==",
  "SubTitle": "AAAAAwAAAhAAAAARAw==",
  "Angle": "AAAAAwAAAhAAAAATAw==",
  "Favorites": "AAAAAwAABhAAAABLAw==",
  "Yellow": "AAAAAwAABhAAAAAHAw==",
  "Blue": "AAAAAwAABhAAAAAEAw==",
  "Red": "AAAAAwAABhAAAAAFAw==",
  "Green": "AAAAAwAABhAAAAAGAw==",
  "Play": "AAAAAgAAANAAAAACAw==",
  "Stop": "AAAAAgAAANAAAAAAAw==",
  "Pause": "AAAAAgAAANAAAAABAw==",
  "Rewind": "AAAAAwAAAhAAAAAzAw==",
  "Forward": "AAAAAwAAAhAAAAA0Aw==",
  "Prev": "AAAAAwAAAhAAAAAwAw==",
  "Next": "AAAAAwAAAhAAAAAxAw==",
  "Replay": "AAAAAwAAAhAAAAAhAw==",
  "Advance": "AAAAAwAAAhAAAAAgAw==",
  "TopMenu": "AAAAAwAAAhAAAAAZAw==",
  "PopUpMenu": "AAAAAwAAAhAAAAAaAw==",
  "Eject": "AAAAAwAAAhAAAAA8Aw==",
  "BDV:SoundOutput": "AAAAAwAABhAAAABFAw==",
  "Dimmer": "AAAAAgAAAFAAAABNAw==",
  "BDV:Sleep": "AAAAAgAAAFAAAABgAw==",
  "BDV:Function": "AAAAAgAAANAAAABpAw==",
  "BDV:SoundMode": "AAAAAgAAANAAAABuAw==",
  "BDV:SoundModeDown": "AAAAAgAAANAAAABeAw==",
  "BDV:SoundModeUp": "AAAAAgAAANAAAABLAw==",
  "Enter": "AAAAAwAAAhAAAAAMAw==",
  "SEN": "AAAAAwAADhAAAABQAw==",
  "Netflix": "AAAAAwAADhAAAABRAw==",
  "Mode3D": "AAAAAwAABhAAAABMAw==",
  "BDV:KeyControl-": "AAAAAgAAANAAAAAXAw==",
  "BDV:KeyControl+": "AAAAAgAAANAAAAAWAw==",
  "BDV:Echo": "AAAAAgAAANAAAAAUAw==",
  "BDV:MicVol+": "AAAAAgAAANAAAAASAw==",
  "BDV:MicVol-": "AAAAAgAAANAAAAATAw==",
  "BDV:Bluetooth": "AAAAAwAABhAAAABxAw==",
  "BDV:MusicEQ": "AAAAAgAAANAAAABJAw==",
  "BDV:SpeakerIllumination": "AAAAAwAABhAAAABgAw==",
  "BDV:FootBall": "AAAAAwAADhAAAAAXAw=="
}


def ircc_execute(command):

    ircc_code = '<IRCCCode>%s</IRCCCode>' % (commands[command])

    soap_body = '<?xml version="1.0"?>\n'\
    '<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">\n'\
    '<SOAP-ENV:Body>\n'\
    '\t<m:X_SendIRCC xmlns:m="urn:schemas-sony-com:service:IRCC:1">\n'\
    '%s\n'\
    '\t</m:X_SendIRCC>\n'\
    '</SOAP-ENV:Body>\n'\
    '</SOAP-ENV:Envelope>' % (ircc_code)

    headers = {
        'SOAPAction': u'"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
        'Host': u'%s' % sony_host,
        'Content-Type': 'text/xml',
        'Content-Length': len(soap_body),
        'User-Agent': user_agent,
    }
   
    ctrl_url = "http://" + sony_host + ctrl_path

    request = urllib2.Request(ctrl_url, soap_body, headers)
    response = urllib2.urlopen(request)

    print response.read()

# Based off of sample - https://github.com/cmusphinx/pocketsphinx/blob/master/swig/python/test/kws_test.py

config = Decoder.default_config()
config.set_string('-dict', 'sony.dict')
config.set_string('-hmm', '/usr/local/share/pocketsphinx/model/en-us/en-us/')
config.set_float('-kws_threshold', 1e-5)
config.set_string('-kws', 'sony.keyword')

decoder = Decoder(config)
decoder.start_utt()

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

while True:

    buf = stream.read(1024)
    decoder.process_raw(buf, False, False)

    if decoder.hyp() != None and decoder.hyp().hypstr == 'eject':
        print "Detected keyword, ejecting tray"
        decoder.end_utt()
        ircc_execute("Eject")
        decoder.start_utt()
 
    if decoder.hyp() != None and decoder.hyp().hypstr == 'lassie':
        print "Detected keyword, going to home menu"
        decoder.end_utt()
        ircc_execute("Home")
        decoder.start_utt()

    if decoder.hyp() != None and decoder.hyp().hypstr == 'flicks':
        print "Detected keyword, starting netflix"
        decoder.end_utt()
        ircc_execute("Netflix")
        decoder.start_utt()

    if decoder.hyp() != None and decoder.hyp().hypstr == 'confirm':
        print "Detected keyword, going to home menu"
        decoder.end_utt()
        ircc_execute("Confirm")
        decoder.start_utt()