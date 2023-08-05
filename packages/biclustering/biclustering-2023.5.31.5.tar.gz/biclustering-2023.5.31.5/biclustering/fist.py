
import pandas as pd
import math
import csv
from biclustering.suffix_tree import build_sufix_tree, generate_tree_as_image,generate_tree_JSON
from biclustering.frequent_patterns import get_FCPs, convert_fcp_to_csv, convert_fcp_to_JSON
from biclustering.generators import get_generators, write_generators_to_csv, write_generators_toJSON
from biclustering.association_rules import Rule
from biclustering.bicluster import generate_biclusters

class FIST:
    def __init__(self):
        self.df = None
        self.ID_ATTR = 'ID'
        self.ITEMSET_ATTR = 'Itemsets'
        self.dataset_name = None
        self.output_directory_path = '.'
        self.min_sup_count = 1
        self.min_sup_percent = 1
        self.number_table = None
        self.item_name_table = None
        self.sfd = None
        self.h_tree = None        
        self.fcp_list = None
        self.genarator_closure_pairs = None
    
    def set_input_dataset(self, input_file_dir: str, dataset_name : str, id_attribute: str, itemset_attribute: str, max_entries : int):
        #This will read first given number of entries, by default 10000 entries.
        self.df = pd.read_csv(input_file_dir+dataset_name, nrows=max_entries)
        self.df = self.df.rename(columns={id_attribute: self.ID_ATTR})
        self.df = self.df.rename(columns={itemset_attribute: self.ITEMSET_ATTR})
        self.dataset_name = dataset_name

    def set_output_directory_path(self, output_dir_path):
        self.output_directory_path = output_dir_path

    def set_minmum_support_count(self, count: int):
        self.min_sup_count = count
    
    def set_min_support_count_by_percent(self, percent: float):
        self.min_sup_count =  math.ceil((len(self.df)*percent)/100)
        self.min_sup_percent = percent
        return self.min_sup_count
    
    def form_number_table(self,generate_number_tbl = True):
        attribute_count = dict()
        rows = dict()
        ids = self.df[self.ID_ATTR].to_list()
        itemsets = self.df[self.ITEMSET_ATTR].to_list()
        for i in range(len(self.df)):
            id = ids[i]
            items =itemsets[i]
            item_list = items.split(",")
            arr = list()
            repeat_check = dict()
            for str in item_list:
                if (str not in attribute_count) and (str not in repeat_check):
                    attribute_count[str] = 1
                    repeat_check[str] = True
                elif str not in repeat_check:
                    attribute_count[str]+=1
                arr.append(str)
            rows[id] = arr

        attribute_count = dict(sorted(attribute_count.items(), key=lambda x:x[1]))

        number_table = dict() # Sorted frequent number table (Mapping)
        item_name_table = dict()

        id = 1
        for keys in attribute_count:
            if attribute_count[keys] >= self.min_sup_count:
                item_name_table[keys] = id
                id+=1
        for key in item_name_table:
            number_table[item_name_table[key]] = key
        
        self.number_table = number_table
        self.item_name_table = item_name_table

        if(generate_number_tbl):
            #output-1: Number Table
            ntable_path = f'{self.output_directory_path}/NumberTable.dataset={self.dataset_name}.minSupport={self.min_sup_percent}%.csv'

            # Write the dictionary to CSV file
            with open(ntable_path, 'w', newline='') as file:
                writer = csv.writer(file)    
                # Write the header
                writer.writerow(['ID', 'Name'])    
                # Write each key-value pair as a row in the CSV file
                for key, value in number_table.items():
                    writer.writerow([key, value])
            print("\nNumber Table is stored in file : ",ntable_path)
        return (rows,attribute_count)

    def generate_sfd(self, itemsets, attribute_count,generate_SFD_file = True):
        self.sfd = dict()
        for id in itemsets:
                items = itemsets[id]
                temp_dict = dict()
                for item in items:
                    if item in self.item_name_table:
                        temp_dict[self.item_name_table[item]] = attribute_count[item]
                sorted_row = dict(sorted(temp_dict.items(), key=lambda x:x[1]))
                if len(sorted_row) >= 1:
                    self.sfd[id]=list((sorted_row.keys()))
        if(generate_SFD_file):
            #output-2: SFD
            sfd_path = f'{self.output_directory_path}/SFD.dataset={self.dataset_name}.minSupport={self.min_sup_percent}%.csv'

            with open(sfd_path, 'w', newline='') as file:
                writer = csv.writer(file)    
                for key, value in self.sfd.items():
                    writer.writerow([key, value])

            print("\nSFD is stored in file : ",sfd_path)
        return self.sfd            
    
    def build_tree(self, produce_suffix_tree_image = False):
        self.h_tree = build_sufix_tree(self.sfd)
        tree_path = f'{self.output_directory_path}/suffixTree.dataset={self.dataset_name}.minSupport={self.min_sup_percent}%.'
        generate_tree_JSON(self.h_tree,tree_path+"json")
        if(produce_suffix_tree_image):
            generate_tree_as_image(self.h_tree,tree_path+"png")
        
        return self.h_tree

    def extract_fcp_list(self, min_support_count, generate_fcp_file=True):
        self.fcp_list = get_FCPs(self.h_tree, min_support_count)
        if(generate_fcp_file):
            fcp_path = f'{self.output_directory_path}/FCP.dataset={self.dataset_name}.minSupport={self.min_sup_percent}%.'
            convert_fcp_to_csv(self.fcp_list,fcp_path+"csv")
            convert_fcp_to_JSON(self.fcp_list,fcp_path+"json")
        return self.fcp_list
    
    def get_generator_closure_pairs(self, output_generator = True):
        self.genarator_closure_pairs = get_generators(self.fcp_list)
        if(output_generator):
            gen_path = f'{self.output_directory_path}/Generators.dataset={self.dataset_name}.minSupport={self.min_sup_percent}%.'
            write_generators_to_csv(self.genarator_closure_pairs, gen_path+"csv")
            write_generators_toJSON(self.genarator_closure_pairs, gen_path+"json")

    def set_item_name_table(self, custom_name_table: dict):
        self.item_name_table = custom_name_table
    
    def generate_rules(self, mininum_confidence):
        rules = Rule.generate_rules(self.genarator_closure_pairs,self.fcp_list,len(self.df), mininum_confidence)
        Rule.convert_rules_to_csv_and_json(rules,self.number_table, self.output_directory_path,self.dataset_name,
        self.min_sup_percent,mininum_confidence)
    
    def produce_biclusters(self,min_sup_count_for_cluster, min_size_itemset = 2):
        generate_biclusters(self.fcp_list, self.number_table, len(self.df),self.dataset_name,self.min_sup_percent,
        min_sup_count_for_cluster,min_size_itemset,self.output_directory_path)

    def process(self, input_file_dir: str, input_dataset_name:str,id_attribute: str, itemset_attribute: str, max_entries = 10000,
        min_supp_percent=1.0, min_conf_percent=0.0,min_supp_count_outputs = 1,produce_final_img=False):

        self.set_input_dataset(input_file_dir,input_dataset_name, id_attribute, itemset_attribute,max_entries)
        self.set_min_support_count_by_percent(min_supp_percent)
        self.set_output_directory_path(input_file_dir+"output")
        assert not self.df.empty

        (items,attribute_count) = self.form_number_table()

        self.generate_sfd(items,attribute_count)
        self.build_tree(produce_final_img)
        self.extract_fcp_list(min_supp_count_outputs)
        self.get_generator_closure_pairs()
        self.produce_biclusters(min_supp_count_outputs)
        self.generate_rules(min_conf_percent)
        print('\nprocess completed')