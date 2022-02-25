import re


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever
[]

def flatten(t):
    flat_list = [item for sublist in t for item in sublist]
    return flat_list


def get_ingredients_used(applet):

    actions = applet['applet_actions']

    action_fields = [action['fields'] for action in actions]

    action_fields = flatten(action_fields)

    ingredients_used = [re.findall(r'\{\{(\w*)\}\}', field['default_value_json']) for field in action_fields]

    ingredients_used = flatten(ingredients_used)

    return list(set(ingredients_used))


def get_user_classification(applet):
    trigger_channel = applet['applet_trigger']['channel_module_name']

    trigger = applet['applet_trigger']['module_name']

    name = applet['name']

    desc = applet['description']

    classify = input(f'{name}\n{desc}\n"{trigger_channel}" -> "{trigger}"')

    if classify == '0':
        return 'public'
    elif classify == '1':
        return 'private'
    else:
        print('invalid input --- 0 for public, 1 for private')
        return get_user_classification(applet)