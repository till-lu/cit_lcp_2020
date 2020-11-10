from random import shuffle
from copy import deepcopy

def create_items(x_probes, x_targets, x_irrelevants, xtimes):
    # list of dicts with all possible items
    stims_base = []
    for itm in x_probes:
        stims_base.append({'word': itm, 'item_type': 'probe'})
    for itm in x_targets:
        stims_base.append({'word': itm, 'item_type': 'target'})
    for itm in x_irrelevants:
        stims_base.append({'word': itm, 'item_type': 'irrelevant'})
    # this list is added one by one to the full final list
    # each time in a new random order
    full_stim_list = []
    for i in range(xtimes):
        shuffle(stims_base)
        full_stim_list += deepcopy(stims_base)
    return(full_stim_list)
        
# example
        
all_test_items = create_items(['Anna', 'jacket', 'blue'], 
                              ['Till', 'coat', 'yellow'], 
                              ['Magda', 'Gaspar', 'whatever', 'scarf', 'gloves',
                               'etc', 'red', 'grey', 'more', 'evenmore'], 3)
    
print(all_test_items)