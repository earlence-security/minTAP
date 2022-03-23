// const fs = require('fs')
const esrefactor = require('esrefactor')
const helper = require('helper')


function transformFilterCode(code, triggerService, trigger, triggerFields, actionService, action) {
    // var ctx = new esrefactor.Context(code);
    // var code1 = ctx.replaceTriggers(triggerService, trigger)

    // console.log(code1)

    ctx = new esrefactor.Context(code);


    var triggerClass = helper.generateTriggerClass(triggerService, trigger, triggerFields)
    var actionClass = helper.generateDummyActionClass()

    var code1 = ctx.replaceActions(actionService, action)
    var filterFunction = helper.embedFilterCode(code1, triggerService, trigger)

    // console.log(code2)
    return filterFunction;
}


function _arrayBufferToBase64( buffer ) {
    var binary = '';
    var bytes = new Uint8Array( buffer );
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode( bytes[ i ] );
    }
    return window.btoa( binary );
}


/*
Convert a string into an ArrayBuffer
from https://developers.google.com/web/updates/2012/06/How-to-convert-ArrayBuffer-to-and-from-String
*/
function str2ab(str) {
    const buf = new ArrayBuffer(str.length);
    const bufView = new Uint8Array(buf);
    for (let i = 0, strLen = str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}

/*
Import a PEM encoded RSA private key, to use for RSA-PSS signing.
Takes a string containing the PEM encoded key, and returns a Promise
that will resolve to a CryptoKey representing the private key.
*/
function importPrivateKey(pem) {
    // fetch the part of the PEM string between header and footer
    const pemHeader = "-----BEGIN PRIVATE KEY-----";
    const pemFooter = "-----END PRIVATE KEY-----";
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length);
    // base64 decode the string to get the binary data
    const binaryDerString = window.atob(pemContents);
    // convert from a binary string to an ArrayBuffer
    const binaryDer = str2ab(binaryDerString);

    return window.crypto.subtle.importKey(
        "pkcs8",
        binaryDer,
        {
            name: "RSASSA-PKCS1-v1_5",
            hash: "SHA-256",
        },
        true,
        ["sign"]
    );
}



function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}


function waitJS (evt) {
    var jsInitChecktimer = setInterval (checkForJS_Finish, 111);

    function checkForJS_Finish () {
        if (document.querySelector('#partner-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.actions > div > button')
        ) {
            clearInterval (jsInitChecktimer);

            myMain();
        }
    }
}


window.addEventListener ("load", waitJS, false);


function myMain () {
    console.log("script loaded")

    const saveBtn = getElementByXpath('//*[@id="partner-applets-body"]/div[2]/main/div/div[2]/div/div/div[2]/div/div[2]/div/button');

    saveBtn.addEventListener("mouseenter",
        function(event) {

            const editor = getElementByXpath('//*[@id="partner-applets-body"]/div[2]/main/div/div[2]/div/div/div[2]/div/div[1]/div[5]/div[2]/div[1]/div/div/div/div[1]/div/div[1]/div[2]/div[1]/div[4]')
            const triggerParams = document.querySelectorAll('#trigger > div.fieldset.composer-fieldset > div > div.composer-tanda-field-items > div')


            let signatureParam = null;
            let filterCodeParam = null;

            for (let i = 0; i < triggerParams.length; i++) {
                if (triggerParams[i].getElementsByTagName('input')[0].getAttribute('value') === 'Code Signature') {
                    signatureParam = triggerParams[i]
                } else if (triggerParams[i].getElementsByTagName('input')[0].getAttribute('value') === 'Filter Code') {
                    filterCodeParam = triggerParams[i]
                }
            }

            if (editor == null || signatureParam == null) {
                console.log("no filter code or appropriate signature fields")
                return
            }


            event.target.disabled = true
            const originalText = event.target.innerHTML
            event.target.innerHTML = "Signing filter code..."


            const lines = []
            for (let i = 0; i < editor.children.length; i++) {
                const line = editor.children[i]
                lines.push(line.textContent)
            }
            var filterCode = lines.join('\n')


            const triggerAPI = []
            const triggerApiList = document.querySelector('#partner-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.form-section > div:nth-child(5) > div:nth-child(2) > div.platform-filter-code-api-list > div:nth-child(1) > ul')
            for (let i = 0; i < triggerApiList.children.length; i++) {
                triggerAPI.push(triggerApiList.children[i].textContent)
            }

            const actionAPI = []
            const actionApiList = document.querySelector('#partner-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.form-section > div:nth-child(5) > div:nth-child(2) > div.platform-filter-code-api-list > div:nth-child(2) > ul')
            for (let i = 0; i < actionApiList.children.length; i++) {
                actionAPI.push(actionApiList.children[i].textContent)
            }

            let [triggerService, trigger, triggerFields] = helper.readJsonApi(triggerAPI)
            let [actionService, action] = helper.readJsonApi(actionAPI)


            const transformedCode = transformFilterCode(filterCode, triggerService, trigger, triggerFields, actionService, action)

            console.log(transformedCode)

            const filterCodeInput = filterCodeParam.querySelector('div:nth-child(3) > div.input > div > div > div > textarea')


            if (filterCodeInput.textContent === encodeURI(transformedCode)) {
                event.target.innerHTML = originalText
                event.target.disabled = false
                return
            }


            filterCodeInput.focus()
            document.execCommand('selectAll', false, null)
            document.execCommand('delete', false, null)
            document.execCommand('insertText', false, encodeURI(transformedCode))


            event.target.focus()

            const encoder = new TextEncoder()
            const encodedCode = encoder.encode(transformedCode)


            chrome.runtime.sendMessage({type:"sk"}, (response) => {
                console.log(response)

                if (!response.success) {
                    event.target.innerHTML = originalText
                    event.target.disabled = false

                    event.target.focus()

                    event.target.disabled = true

                    new Promise(r => setTimeout(r, 2000)).then(_ => {

                        event.target.disabled = false

                    })

                    alert("No signature is generated. Please authorize with the trigger service first")

                } else {

                    importPrivateKey(response.sk).then((sk) => {
                        console.log(sk);
                        crypto.subtle.sign(
                            "RSASSA-PKCS1-v1_5",
                            sk,
                            encodedCode
                        ).then(signature => {
                            // console.log(signature)

                            const encodedSignature = _arrayBufferToBase64(signature)

                            // console.log(encodedSignature)

                            const input = signatureParam.querySelector('div:nth-child(3) > div.input > div > div > div > textarea')
                            input.focus()
                            document.execCommand('selectAll', false, null)
                            document.execCommand('delete', false, null)
                            document.execCommand('insertText', false, encodedSignature)


                            // console.log('finished signing')


                            event.target.innerHTML = originalText
                            event.target.disabled = false

                            event.target.focus()

                            event.target.disabled = true

                            new Promise(r => setTimeout(r, 2000)).then(_ => {

                                event.target.disabled = false

                            })
                        });
                    });

                }


            });





        }, false);

}


