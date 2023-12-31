from pprint import pprint
import pandas as pd
from pandas import DataFrame
df_tennis = pd.read_csv('ID3.csv')
attribute_names = list(df_tennis.columns)
attribute_names.remove('Play Tennis')

print(attribute_names)


def entropy_of_list(lst):
    from collections import Counter
    count = Counter(x for x in lst)
    num_instances = len(lst)*1.
    probs = [x/num_instances for x in count.values()]
    return entropy(probs)


def entropy(probs):
    import math
    return sum([-prob*math.log(prob, 2) for prob in probs])


total_entropy = entropy_of_list(df_tennis['Play Tennis'])


def information_gain(df, split_attribute_name, target_attribute_name, trace=0):
    df_split = df.groupby(split_attribute_name)
    nobs = len(df.index)*1.
    df_agg_ent = df_split.agg(
        {target_attribute_name: [entropy_of_list, lambda x:len(x)/nobs]})
    df_agg_ent.columns = ['Entropy', 'propobservations']
    new_entropy = sum(df_agg_ent['Entropy'] * df_agg_ent['propobservations'])
    old_entropy = entropy_of_list(df[target_attribute_name])
    print(split_attribute_name, 'IG :', old_entropy - new_entropy)
    return old_entropy - new_entropy


def id3(df, target_attribute_name, attribute_names, default_class=None):
    from collections import Counter
    count = Counter(x for x in df[target_attribute_name])
    if len(count) == 1:
        return next(iter(count))
    elif df.empty or (not attribute_names):
        return default_class
    else:
        default_class = max(count.keys())
        gain = [
            information_gain(df, attr, target_attribute_name) for attr in attribute_names
        ]
        print()
        index_of_max = gain.index(max(gain))
        best_attr = attribute_names[index_of_max]

        tree = {best_attr: {}}

        remaining_attribute_names = [
            i for i in attribute_names if i != best_attr]

        for attr_val, data_subset in df.groupby(best_attr):
            subtree = id3(data_subset, target_attribute_name,
                          remaining_attribute_names, default_class)
            tree[best_attr][attr_val] = subtree

        return tree


tree = id3(df_tennis, 'Play Tennis', attribute_names)
print("\n\nThe Resultant Decision Tree is:\n")
pprint(tree)
