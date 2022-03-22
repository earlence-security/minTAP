# minTAP Client

This folder contains the implementation of a minTAP client as a Chrome browser extension.

##  Installation

Please follow the Step 2 in this [Chrome help page](https://support.google.com/chrome/a/answer/2714278?hl=en) to install minTAP's browser extension.


## Usage


**Note: the extension relies on IFTTT's developer portal to modify the rules to be minTAP-compatible. It appears that recently IFTTT's rule/applet creation UI is not working correctly. The workaround is to create a plain IFTTT rule first and then use the edit UI to make the rule minTAP-compatible.**


This extension supports any IFTTT rules/applets that use minTAP-compatible trigger. 

1. Open an existing applet (for example, by going to `https://ifttt.com/p/[user-id]/applets/private`, select one of the applets that uses a minTAP-compatible trigger, and click 'Edit')

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_2.png)

2. Modify the filter code to try out different conditions

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_3.png)

3. Once the `Save` button is clicked, the extension will automatically fill the minimizer and signature fields.

4. Enable the applet by following the `Enable it on IFTTT` link

![alt text](https://raw.githubusercontent.com/EarlMadSec/minTAP/master/screenshots/screenshot_4.png)

If the applet is using the `Toy Trigger` from our `minTAP example service`, see the server's [README](Server/README.md) on how to triggering the applet.