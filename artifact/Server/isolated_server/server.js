const fastify = require('fastify')({ logger: true })
const ivm = require('isolated-vm');


// function filter(input) {
//     var Reddit = input.copy()
//     var title = Reddit.newTopPostInSubreddit.Title.trim()
//     title = title.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#039;/g, "'")
//
//     if (title.charAt(0) === '[' && title.indexOf("]") > 0) {
//         title = title.slice(0, title.indexOf("]"))
//     }
//
//     title = title.split('[')[0].trim()
//
// // Try double dash (official format), fallback to single dash:
//     var titleSplit = title.split("--")
//     if (titleSplit.length !== 2) {
//         titleSplit = title.split("-")
//     }
//
//     return titleSplit.length >= 2
// }

function filter_plain(Reddit) {
    var title = Reddit.newTopPostInSubreddit.Title.trim()
    title = title.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#039;/g, "'")

    if (title.charAt(0) === '[' && title.indexOf("]") > 0) {
        title = title.slice(0, title.indexOf("]"))
    }

    title = title.split('[')[0].trim()

// Try double dash (official format), fallback to single dash:
    var titleSplit = title.split("--")
    if (titleSplit.length !== 2) {
        titleSplit = title.split("-")
    }

    return titleSplit.length >= 2
}


const classCode = `
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
`



let isolate = new ivm.Isolate({ memoryLimit: 8 });
// let context =  isolate.createContextSync();

// let script =  isolate.compileScriptSync(filter + '');
// script.runSync(context);
//
// let fnReference =  context.global.getSync('filter');


fastify.post('/filter', async (request, reply) => {
    // let isolate = new ivm.Isolate({ memoryLimit: 8 });
    let context = await isolate.createContext();

    console.log(request.body)

    let filter = request.body.filter
    //
    let script = await isolate.compileScript(classCode + '' + filter + '');
    await script.run(context);

    let fnReference = await context.global.get('filter');

    let input = new ivm.ExternalCopy(request.body.data)

    let result = await fnReference.apply(undefined, [input]);

    if (result == null) {
        return {'result' : 'skip'}
    } else {
        return {'result' : result.copySync()}
    }

})

fastify.post('/plain', async (request, reply) => {
    let result = filter_plain(request.body.data)
    return {'result' : result}
})


fastify.post('/:params', function (request, reply) {
    console.log(request.body)
    console.log(request.query)
    console.log(request.params)
    console.log(request.headers)
    request.log.info('some info')
    return {'result' : 'ok'}
})

// Run the server!
const start = async () => {
    try {
        await fastify.listen(3000, '0.0.0.0')
        fastify.log.info(`server listening on ${fastify.server.address().port}`)
    } catch (err) {
        fastify.log.error(err)
        process.exit(1)
    }
}
start()