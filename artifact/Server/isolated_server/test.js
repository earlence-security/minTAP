const code =   `
class newTestData {

    constructor(data) {
        this.Subreddit_ = data.Subreddit;
        this.Title_ = data.Title;
        this.Content_ = data.Content;
        this.PostUrl_ = data.PostUrl;
        this.monitor = {Subreddit: false, Title: false, Content: false, PostUrl: false, };
    }


    get Subreddit() {
        this.monitor.Subreddit = true;
        return this.Subreddit_;
    }

    get Title() {
        this.monitor.Title = true;
        return this.Title_;
    }

    get Content() {
        this.monitor.Content = true;
        return this.Content_;
    }

    get PostUrl() {
        this.monitor.PostUrl = true;
        return this.PostUrl_;
    }

    accessedFields() {
        var result = []
        for (const [field, accessed] of Object.entries(this.monitor)) {
            if (accessed) {
                result.push(field);
            }
        }
        return result;
    }
}

class DummyAction {
    action(param) {

    }

    skip(param) {

    }
}

function filter(data) {
var data2 = data.copy()
const Trigger = new newTestData(data2);
const RedditTestService = {newTestData: Trigger};
const Action = new DummyAction();

if (RedditTestService.newTestData.Title === "my title") {
  Action.action(RedditTestService.newTestData.Content)
} else if (RedditTestService.newTestData.Title === "my title 2") {
  Action.action(RedditTestService.newTestData.Subreddit)
} else {
  return null;
}

return RedditTestService.newTestData.accessedFields();

}
`

const ivm = require('isolated-vm');

let isolate = new ivm.Isolate({ memoryLimit: 8 });

let context =  isolate.createContextSync();



let script =  isolate.compileScriptSync(code);
 script.runSync(context);

let fnReference =  context.global.getSync('filter');

let input = new ivm.ExternalCopy({
    Subreddit: 'r/test',
    Title: 'my title',
    Content: 'my content',
    PostUrl: 'www.ifttt.com'
})

let result =  fnReference.applySync(undefined, [input]);


console.log(result.copySync())
