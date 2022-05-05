## Dataset

Due to potential privacy concerns, we did not publish the original dataset we used in the paper.
Instead, we outline the data crawling techniques as below.


### Applet data

You may use the following GraphQL query to fetch the information of an applet

```
curl -X "POST" "https://ifttt.com/api/v3/graph" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
	"query": "query($applet_id:String!){applet(id:$applet_id){id name description published archived filter_code channel_id applet_trigger{channel_module_name module_name fields{name custom_label hidden default_value_json}}applet_actions{channel_module_name module_name fields{name custom_label hidden default_value_json}}applet_queries{channel_module_name module_name fields{name custom_label hidden default_value_json}}}}",
	"variables": {
		"applet_id": "......"
	}
}'
```

### Service data


You may use the following GraphQL query to fetch the information of an IFTTT service

```
curl -X "POST" "https://ifttt.com/api/v3/graph" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
	"query": "query($serviceModuleName:String!){channel(module_name:$serviceModuleName){live_channel{offline}public_triggers{module_name normalized_module_name name description id weight trigger_fields{name label required shareable hideable field_ui_type normalized_field_type helper_text}ingredients{id name normalized_name label note slug value_type example}}public_actions{module_name normalized_module_name name description id weight incompatible_triggers action_fields{name normalized_module_name label required shareable hideable field_ui_type normalized_field_type helper_text}}}}",
	"variables": {
		"serviceModuleName": "twitter"
	}
}'
```


## How to generate Figure 9

1. Make sure the Python packages `pandas` and `matplotlib` are installed

2. Make sure the applets dataset is stored in `./data/applet`  and the service dataset is `./data/service`. Each applet/service should be in a separate `.json` file.

3. Run the Python scripts:

```
$ python3 trigger_level_analyze.py [type]
$ python3 trigger_level_plot.py
```
The second script will generate a `fig_9.pdf` file to reproduce Figure 9 in the paper. 
Set `type` to `all` to generate the left subplot, or set `type` to `filter` to generate the right subplot.