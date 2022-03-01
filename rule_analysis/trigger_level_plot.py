import pickle

import pandas as pd
import matplotlib.pyplot as plt

with open('trigger_level.p', 'rb') as f:
    private_applet, keywords = pickle.load(f)


def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def Flatten(t):
    return [item for sublist in t for item in sublist]

low_kw = Flatten(keywords[:2])
high_kw = Flatten(keywords[2:9])
mix_kw = Flatten(keywords[9:])


attr_count = []

for applet_id, data in private_applet.items():
    used_ingredients = data['used_ingredients']
    all_ingredients = data['all_ingredients']
    unused_ingredients = Diff(all_ingredients, used_ingredients)
    high_count = sum(unused_attribute in high_kw for unused_attribute in unused_ingredients)
    attr_count.append([len(all_ingredients), len(unused_ingredients), high_count])


df = pd.DataFrame(attr_count, columns=['n_total', 'n_unused', 'n_high'])

attr = list(range(15))

cdf_total = [df.loc[df['n_total'] >= n].shape[0] / df.shape[0] for n in attr]
cdf_unused = [df.loc[df['n_unused'] >= n].shape[0] / df.shape[0] for n in attr]
cdf_high = [df.loc[df['n_high'] >= n].shape[0] / df.shape[0] for n in attr]

plt.plot(attr, cdf_total, label='% of rules with >= x total attributes')
plt.plot(attr, cdf_unused, label='% of rules with >= x unused attributes')
plt.plot(attr, cdf_high, label='% of rules with >= x unused high-sensitive attributes')
plt.xlabel('# of trigger attributes')
plt.legend()
plt.show()