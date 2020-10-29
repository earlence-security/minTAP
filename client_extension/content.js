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

function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}


function waitJS (evt) {
    var jsInitChecktimer = setInterval (checkForJS_Finish, 111);

    function checkForJS_Finish () {
        if (document.querySelector('#partners-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.actions > div > button')
        ) {
            clearInterval (jsInitChecktimer);

            myMain();
        }
    }
}


window.addEventListener ("load", waitJS, false);


function myMain () {
    console.log("script loaded")

    const saveBtn = getElementByXpath('//*[@id="partners-applets-body"]/div[2]/main/div/div[2]/div/div/div[2]/div/div[2]/div/button');

    saveBtn.addEventListener("mouseenter",
        function(event) {
            console.log(event.target)

            const editor = document.querySelector('#partners-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.form-section > div:nth-child(4) > div:nth-child(2) > div.fieldset.composer-fieldset > div > div > div > div.monaco-editor-wrapper-inner > div > div.overflow-guard > div.monaco-scrollable-element.editor-scrollable.vs.mac > div.lines-content.monaco-editor-background > div.view-lines')
            const triggerParams = document.querySelectorAll('#trigger > div.fieldset.composer-fieldset > div > div.composer-tanda-field-items > div')


            let signatureParam = null;
            let filterCodeParam = null;

            for (let i = 0; i < triggerParams.length; i++) {
                if (triggerParams[i].getElementsByTagName('label')[0].textContent === 'Code Signature') {
                    signatureParam = triggerParams[i]
                } else if (triggerParams[i].getElementsByTagName('label')[0].textContent === 'Filter Code') {
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
            const filterCode = lines.join('\n')



            const triggerAPI = []
            const triggerApiList = document.querySelector('#partners-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.form-section > div:nth-child(4) > div:nth-child(2) > div.platform-filter-code-api-list > div:nth-child(1) > ul')
            for (let i = 0; i < triggerApiList.children.length; i++) {
                triggerAPI.push(triggerApiList.children[i].textContent)
            }

            const actionAPI = []
            const actionApiList = document.querySelector('#partners-applets-body > div.platform-bg_color-container > main > div > div.main-content-column > div > div > div:nth-child(2) > div > div.form-section > div:nth-child(4) > div:nth-child(2) > div.platform-filter-code-api-list > div:nth-child(2) > ul')
            for (let i = 0; i < actionApiList.children.length; i++) {
                actionAPI.push(actionApiList.children[i].textContent)
            }

            let [triggerService, trigger, triggerFields] = helper.readJsonApi(triggerAPI)
            let [actionService, action] = helper.readJsonApi(actionAPI)


            const transformedCode = transformFilterCode(filterCode, triggerService, trigger, triggerFields, actionService, action)

            console.log(transformedCode)

            const filterCodeInput = filterCodeParam.querySelector('div > div > div > div > div > textarea')


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

            window.crypto.subtle.generateKey(
                {
                    name: "RSASSA-PKCS1-v1_5",
                    // Consider using a 4096-bit key for systems that require long-term security
                    modulusLength: 2048,
                    publicExponent: new Uint8Array([1, 0, 1]),
                    hash: "SHA-256",
                },
                true,
                ["sign", "verify"]
            ).then((keyPair) => {
                crypto.subtle.sign(
                    "RSASSA-PKCS1-v1_5",
                    keyPair.privateKey,
                    encodedCode
                ).then(signature => {
                    console.log(signature)

                    const encodedSignature = _arrayBufferToBase64(signature)

                    console.log(encodedSignature)

                    const input = signatureParam.querySelector('div > div > div > div > div > textarea')
                    input.focus()
                    document.execCommand('selectAll', false, null)
                    document.execCommand('delete', false, null)
                    document.execCommand('insertText', false, encodedSignature)


                    console.log('finished signing')


                    event.target.innerHTML = originalText
                    event.target.disabled = false

                    event.target.focus()
                })
            });



        }, false);

}


