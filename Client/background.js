// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


function generateRandomString(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~";
    for (var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

async function sha256(message) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder().encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}


/*
Convert  an ArrayBuffer into a string
from https://developers.google.com/web/updates/2012/06/How-to-convert-ArrayBuffer-to-and-from-String
*/
function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
}

/*
Export the given key and write it into the "exported-key" space.
*/
async function exportPublicKey(key) {
    const exported = await window.crypto.subtle.exportKey(
        "spki",
        key
    );
    const exportedAsString = ab2str(exported);
    const exportedAsBase64 = window.btoa(exportedAsString);
    const pemExported = `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64}\n-----END PUBLIC KEY-----`;

    return pemExported;
}


async function exportPrivateKey(key) {
    const exported = await window.crypto.subtle.exportKey(
        "pkcs8",
        key
    );
    const exportedAsString = ab2str(exported);
    const exportedAsBase64 = window.btoa(exportedAsString);
    const pemExported = `-----BEGIN PRIVATE KEY-----\n${exportedAsBase64}\n-----END PRIVATE KEY-----`;

    return pemExported;
}



let code_verifier = generateRandomString(128);
let code_challenge = code_verifier;

let pk = undefined;
let sk = undefined;


let client_id = '';
let auth_code = '';


let mintap_host = undefined;

chrome.webRequest.onBeforeRequest.addListener(
    function (details) {
        if (details.url.indexOf("ifttt.com/channels/mintap_service/authorize") !== -1) {
            console.log("visited ifttt.com callback\n")
            let callback_url = new URL(details.url);
            console.log(callback_url.search);
            auth_code = callback_url.searchParams.get('code');

            const token_url = new URL(mintap_host + "/mintap/auth/token")

            let formData = new FormData();
            formData.append('client_id', client_id)
            formData.append('grant_type', 'authorization_code')
            formData.append('code', auth_code)
            formData.append('code_verifier', code_verifier)

            crypto.subtle.generateKey(
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
                pk = keyPair.publicKey;
                sk = keyPair.privateKey;

                exportPublicKey(pk).then((export_pk) => {
                    formData.append('public_key', export_pk);

                    console.log('Acquiring token from')
                    console.log(token_url.href);

                    let xhr = new XMLHttpRequest();

                    function onTokenGranted() {
                        if (xhr.readyState === XMLHttpRequest.DONE) {
                            if (xhr.status === 200) {
                                console.log("Token acquired")
                                console.log(xhr.responseText);
                            }
                        }
                    }

                    xhr.open("POST", token_url.href, true);
                    xhr.onreadystatechange = onTokenGranted;
                    xhr.send(formData);

                    chrome.storage.local.set({pk: export_pk}, function() {
                        console.log('Public key is stored ' + export_pk);
                    });


                });

                exportPrivateKey(sk).then((export_sk) => {
                    chrome.storage.local.set({sk: export_sk}, function() {
                        console.log('Private key is stored ' + export_sk);
                    });
                })

            });

            callback_url.searchParams.delete('token_url')
            return {redirectUrl: callback_url.toString()};
        }
        if (details.url.indexOf("/mintap/auth") !== -1) {

            let auth_url = new URL(details.url);
            mintap_host = auth_url.origin

            console.log("visited my server\n")
            console.log(details.url)
            if (details.url.indexOf("/mintap/auth/authorize") !== -1) {
                console.log("append code challenge")
                const url = new URL(details.url);
                client_id = url.searchParams.get('client_id');
                return {redirectUrl: details.url + '&code_challenge=' + code_challenge};
            }

        }
    },
    {
        urls: ["<all_urls>"]
    },
    ["blocking"]
);


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log(request)


        if (request.type === 'sk') {


            chrome.storage.local.get('sk', function(result) {
                if (result.sk == null) {
                    console.log('no sk sent')
                    sendResponse({success: false, sk: ''})

                } else {
                    console.log('sending sk:\n' + exported_sk)
                    sendResponse({success: true, sk: result.sk})
                }
            });




        }
        return true;
    });


