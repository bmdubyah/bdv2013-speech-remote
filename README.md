Model Name: BLU-RAY HOME THEATRE SYSTEM
Model Number: BDV-2013
Remote Model: RM-ADP089 - https://esupport.sony.com/US/perl/model-remote.pl?mdl=RMADP089

Other models may be slightly different. I was able to retrieve command information from the player using the following steps (I suspect it would be a similar process for other models if you wanted to implement your own remote model)

1. Register the device
  http://<deviceIP>:50002/register?name=YourComputer&registrationType=initial&deviceId=MyDevice%3A<mac_address_with_dashes>

2. Call /getRemoteCommandList
   
   GET /getRemoteCommandList HTTP/1.1
   Host: <deviceIP>:50002
   X-CERS-DEVICE-ID: MyDevice:<mac_address_with_dashes>
   X-CERS-DEVICE-INFO: YourComputer
   Connection: close

This package uses the PocketSphinx speech to text recognition library developed by Carnegie Mellon University: https://github.com/cmusphinx/pocketsphinx

2 files are important for extending the speech to text recognition (I have only implemented Eject, Home, and Netflix in this example package):

sony.dict  (Dictionary file containing the dictionary word and the corresponding Phoneme translation)
sony.keyword (keyword used for the keyword spotting)

You can use the CMUdict (http://www.speech.cs.cmu.edu/cgi-bin/cmudict) to obtain the Phoneme translation for the keyword that you want to implement. You will add this value to sony.dict file.
