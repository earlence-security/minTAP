




// chrome.runtime.onMessage.addListener(
//     function(request, sender, sendResponse) {
//         if (request.type === 'queryAPI') {
//             console.log('started')
//
//
//
//             let userJwt = document.documentElement.outerHTML.match(/userJWT: '(.+)'/)[1]
//
//             sendResponse(userJwt)
//
//
//             // fetch("https://ifttt.com/api/v3/graph", {
//             //     method: "POST",
//             //     headers: {
//             //         "Authorization": `Token jwt="${userJwt}"`,
//             //         "Content-Type": "application/json; charset=utf-8"
//             //     },
//             //     body: `{\"query\":\"\\n  mutation(\\n    $name: String!\\n    $description: String\\n    $channel_id: ID!\\n    $push_enabled: Boolean\\n    $filter_code: String\\n    $trigger: DiyTandaInput!\\n    $queries: [DiyTandaInput]\\n    $actions: [DiyTandaInput]!\\n  ) {\\n    diyAppletCreate(\\n      input: {\\n        name: $name\\n        description: $description\\n        channel_id: $channel_id\\n        filter_code: $filter_code\\n        push_enabled: $push_enabled\\n        trigger: $trigger\\n        queries: $queries\\n        actions: $actions\\n      }\\n    ) {\\n      errors {\\n        attribute\\n        message\\n      }\\n      normalized_applet {\\n        id\\n      }\\n    }\\n  }\\n\",\"variables\":{\"name\":\"If !!!!!!, then Send me an email at ychen459@wisc.edu\",\"channel_id\":\"1945522301\",\"filter_code\":\"'ffffff'\",\"trigger\":{\"step_identifier\":\"reddit_test_service.new_top_post\",\"fields\":[{\"name\":\"subreddit\",\"hidden\":true,\"value\":\"\\\"t1\\\"\"},{\"name\":\"code_signature\",\"hidden\":true,\"value\":\"\\\"t2\\\"\"},{\"name\":\"filter_code\",\"hidden\":true,\"value\":\"\\\"t3\\\"\"}],\"channel_id\":\"1945522301\"},\"actions\":[{\"step_identifier\":\"email.send_me_email\",\"fields\":[{\"name\":\"subject\",\"hidden\":true,\"value\":\"\\\"a1\\\"\"},{\"name\":\"body\",\"hidden\":true,\"value\":\"\\\"a2\\\"\"}],\"channel_id\":\"6\"}],\"queries\":[]}}`
//             // })
//             //     .then((res) => res.json())
//             //     .then(data => {
//             //         console.log(data)
//             //     })
//
//
//
//
//
//         }
//     }
// )