import json
import sys
import pickle
from pathlib import Path

from helper import get_ingredients_used


if len(sys.argv) != 2 or sys.argv[1] not in ['all', 'filter']:
    print('Usage: python3 trigger_level_analyze.py all|filter')

services = {}

for service_file in Path('data/service').iterdir():
    with service_file.open() as f:
        service = json.load(f)['data']['channel']

    services[service_file.stem] = service


with open('classificationTriggersNew.json') as f:
    trigger_classification = json.load(f)


non_classified_triggers = {}

private_applet = {}

invalid_applet = []

private_code_count = 0

for applet_file in Path('data/applet').iterdir():

    try:

        with applet_file.open() as f:
            applet = json.load(f)['data']['applet']

        applet_trigger_channel = applet['applet_trigger']['channel_module_name']

        applet_trigger = applet['applet_trigger']['module_name']


    except Exception:
        invalid_applet.append(applet_file.stem)
        continue

    if sys.argv[1] == 'filter':
        if applet['filter_code'] is None or len(applet['filter_code']) == 0:
            continue


    if applet_trigger_channel not in services:
        continue

    trigger_data = next(
        (t for t in services[applet_trigger_channel]['public_triggers'] if t['module_name'] == applet_trigger), None)

    if trigger_data is None:
        continue

    if applet_trigger_channel in trigger_classification and \
            applet_trigger in trigger_classification[applet_trigger_channel]:

        if trigger_classification[applet_trigger_channel][applet_trigger] == 'private' or trigger_classification[applet_trigger_channel][applet_trigger] == 'available':
            used_ingredients = get_ingredients_used(applet)

            all_ingredients = [ingredient['name'] for ingredient in trigger_data['ingredients']]

            private_applet[applet_file.stem] = {'used_ingredients': used_ingredients,
                                                'all_ingredients': all_ingredients}

            if applet['filter_code'] is not None and len(applet['filter_code']) != 0:
                private_code_count += 1
    else:

        if applet_trigger_channel not in non_classified_triggers:
            non_classified_triggers[applet_trigger_channel] = []

        non_classified_triggers[applet_trigger_channel].append(applet_trigger)




def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))


def sensitive(attribute, unique_kw, must_kw, avoid_kw):
    if avoid_kw[0] == '':
        avoid_kw = []

    return any(keyword in attribute for keyword in unique_kw) and any(keyword in attribute for keyword in must_kw) and not any(keyword in attribute for keyword in avoid_kw)


def keyword_count(unique_kw, must_kw, avoid_kw):
    rule_count = 0
    attribute_count = 0
    attribute_total = 0
    for applet_id, data in private_applet.items():
        used_ingredients = data['used_ingredients']
        all_ingredients = data['all_ingredients']

        if any(sensitive(unused_attribute, unique_kw, must_kw, avoid_kw) for unused_attribute in Diff(all_ingredients, used_ingredients)):
            rule_count += 1

        attribute_total += len(Diff(all_ingredients, used_ingredients))
        attribute_count += sum(sensitive(unused_attribute, unique_kw, must_kw, avoid_kw) for unused_attribute in Diff(all_ingredients, used_ingredients))

    return attribute_count / attribute_total, rule_count / len(private_applet)


def keyword_subset(unique_kw, must_kw, avoid_kw):
    subset = []
    for applet_id, data in private_applet.items():
        used_ingredients = data['used_ingredients']
        all_ingredients = data['all_ingredients']


        subset += [unused_attribute for unused_attribute in Diff(all_ingredients, used_ingredients) if sensitive(unused_attribute, unique_kw, must_kw, avoid_kw)]

    return subset



with open('keywords.txt') as f:
    keyword_list = f.readlines()

for line in keyword_list:
    keywords = line.split(';')
    unique_kw = [keyword.strip() for keyword in keywords[0].split(',')]
    must_kw = [keyword.strip() for keyword in keywords[1].split(',')]
    avoid_kw = [keyword.strip() for keyword in keywords[2].split(',')]

subsets = []

for line in keyword_list:
    keywords = line.split(';')
    unique_kw = [keyword.strip() for keyword in keywords[0].split(',')]
    must_kw = [keyword.strip() for keyword in keywords[1].split(',')]
    avoid_kw = [keyword.strip() for keyword in keywords[2].split(',')]
    subsets.append(keyword_subset(unique_kw, must_kw, avoid_kw))


missed = []
subset2 = [set(subset) for subset in subsets]
for applet_id, data in private_applet.items():
    used_ingredients = data['used_ingredients']
    all_ingredients = data['all_ingredients']

    missed += [unused_attribute for unused_attribute in Diff(all_ingredients, used_ingredients) if
               not any(unused_attribute in subset for subset in subset2)]


with open('trigger_level.p', 'wb') as f:
    pickle.dump([private_applet, subset2], f)

