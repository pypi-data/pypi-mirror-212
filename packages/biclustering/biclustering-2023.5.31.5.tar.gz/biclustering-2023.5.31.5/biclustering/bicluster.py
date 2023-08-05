import pandas as pd
def generate_biclusters(FCPs: list, item_name_map: dict, dataset_size: int,dataset_name:str,min_supp, min_support_count = 1, min_size = 2,output_path = './/biclusters'):
    #Output-6: Biclusters   
    data = list()
    data_ids = list()

    for fcp in FCPs:
        if fcp.support_count() >= min_support_count and fcp.size() >= min_size:
            itemset = str([item_name_map[number] for number in fcp.get_itemset()])
            support_count = fcp.support_count()
            support_percentage = 100*support_count/dataset_size
            support_obj = fcp.get_object_as_line()
            data.append([itemset,support_obj, support_count, support_percentage])
            data_ids.append([str(fcp.get_itemset()), support_obj,support_count, support_percentage,])
            
    df = pd.DataFrame(data_ids, columns=["Bi-clusters","Support Object", "Support", "Support(%)", ])
    df_with_names = pd.DataFrame(data, columns=["Bi-clusters","Support Object", "Support", "Support(%)",])
    bicluster_path = f"{output_path}/biclusters.dataset={dataset_name}.minSupport={min_supp}.minSize={min_size}."
    bicluster_names_path = f"{output_path}/biclusters.withNames.dataset={dataset_name}.minSupport={min_supp}.minSize={min_size}."
    df.to_csv(bicluster_path+"csv")
    df.to_json(bicluster_path+"json")
    df_with_names.to_csv(bicluster_names_path+"csv")
    df_with_names.to_json(bicluster_names_path+"json")
    print(f"\nTotal {len(df)} bi-clusters are stored in json and csv format")