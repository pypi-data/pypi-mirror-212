# Finds generators from the list of FCPs
# Input: List of FCPs
# Output: List of generators


# A Generator element g has two parts:
# g[0] is the generator pattern
# g[1] is the closure pattern

from biclustering.Pattern import Pattern
from json import dumps
import itertools
import csv

def get_generators(FCP: list):
    """Returns the list of generators from the FCP list"""

    FCP.sort(key = comparator)
    GEN = []
    
    for i in range(len(FCP)):
        pattern = FCP[i].get_copy()
        found_gen = False
        generator_size = 1

        while found_gen == False and generator_size < pattern.size():
            subsets = get_all_subsets(pattern.get_itemset(), generator_size)

            for subset in subsets:
                not_generator = False
                for generator in GEN:
                    if generator[0].get_itemset() == subset:
                        not_generator = True
                        break
                if not_generator == False:
                    for j in range(i):
                        if subset.issubset(FCP[j].get_itemset()):
                            not_generator = True
                            break
                if not_generator == False:
                    GEN.append([Pattern(subset, pattern.get_object()), pattern])
                    found_gen = True

            generator_size += 1

        if found_gen == False:
            GEN.append([pattern, pattern.get_copy()])
    
    return GEN


def write_generators_to_csv( GENs: list, gen_path):
    #Output-5 Generators
    with open(gen_path, 'w', newline='') as file:
        writer = csv.writer(file)    
        # Write the header
        writer.writerow(['Genrator', 'Closure', 'Support Objects'])    
        # Write each key-value pair as a row in the CSV file
        for g in GENs:
            writer.writerow([g[0].get_itemset(), g[1].get_itemset(), g[1].get_object()])
    print("\nGenerators are Created in the directory : ",gen_path)

def write_generators_toJSON(GENs:list, gen_path):
    GENJSON = [{ "generator" : list(g[0].get_itemset()), "FCP" : g[1].toJSON()} for g in GENs]
    with open(gen_path, "w") as outputfile:
        outputfile.write(dumps(GENJSON, indent=2))
    print("\nGenerators are Created as json in the directory : ",gen_path)

def comparator(pattern: Pattern) ->int:
    """Custom key funtion that will be used for used for sorting FCPs
    based on the size of the pattern"""
    return pattern.size()

def get_all_subsets(subset: set, n: int) ->list:
    """Returns all possible subsets of size n from the given subset"""
    return [set(tpl) for tpl in itertools.combinations(subset, n)]

