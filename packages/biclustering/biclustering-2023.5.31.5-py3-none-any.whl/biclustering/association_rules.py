import pandas as pd

class Rule:
    def __init__(self, antecedent_set = set(), consequent_set = set(), support_object = list(),lift = 1.0, confidence = 0.0):
        self._antecedent = antecedent_set
        self._consequent = (consequent_set - antecedent_set)
        self._support_object = support_object
        self._support = len(support_object)
        self._confidence = confidence
        self._lift = lift
    
    def support(self) ->int:
        return self._support
    
    def confidence(self) ->float:
        return self._confidence
    
    def lift(self) -> float:
        return self._lift
    
    def antecedent(self) ->set:
        return self._antecedent
    
    def consequent(self) ->set:
        return self._consequent
    
    def is_valid(self, min_confidence: float) ->bool:
        return self._confidence >= min_confidence
    
    def is_exact(self) ->bool:
        return self._confidence == 1.0

    def find_support_count(itemset: set, FCPs :list) ->int:
        max_count = 0
        for pattern in FCPs:
            sup_count = pattern.support_count()
            if sup_count > max_count and itemset.issubset(pattern.get_itemset()):
                max_count = sup_count
        return max_count
    

        
    def convert_rules_to_csv_and_json(rules,number_table,output_dir,dataset_name,min_supp,min_conf):
        for key in list(rules.keys()):
            res = list()
            res_with_ids = list()
            for rule in rules[key]:
                antecedent = str([number_table[id] for id in rule.antecedent()])
                consequent = str([number_table[id] for id in rule.consequent()])
                confidence = rule.confidence()
                support = rule.support()
                lift = rule.lift()
                res.append([antecedent,consequent,confidence,support,lift])
                res_with_ids.append([str(rule.antecedent()),str(rule.consequent()),confidence,support,lift])

            rule_dataframe = pd.DataFrame(res_with_ids, columns = ["Antecedent", "Consequent", "Confidence", "Support Count", "lift"])
            rule_dataframe_with_names = pd.DataFrame(res, columns = ["Antecedent", "Consequent", "Confidence", "Support Count", "lift"])
            rules_names_path = f"{output_dir}/rule.WithNames.{key}.dataset={dataset_name}.minSupport={min_supp}.minConf={min_conf}."
            rules_path = f"{output_dir}/rule.{key}.dataset={dataset_name}.minSupport={min_supp}.minConf={min_conf}."
            rule_dataframe_with_names.to_csv(rules_names_path+"csv")
            rule_dataframe_with_names.to_json(rules_names_path+"json")
            rule_dataframe.to_csv(rules_path+"csv")
            rule_dataframe.to_json(rules_path+"json")

        for key in list(rules.keys()):
            print("\nTotal "+str(len(rules[key]))+" "+str(key)+" rules generated.")


    def generate_rules(GEN, FCP, dataset_size, min_confidence) ->list:
       

        AR_E = list()
        AR_SB = list()
        AR_PB = list()

        for g in GEN:
            for pattern in FCP:
                consequent = (pattern.get_itemset() - g[0].get_itemset())
                if g[1].get_itemset() == pattern.get_itemset():
                    if(g[0].get_itemset() != pattern.get_itemset()):
                        lift = (pattern.support_count()*dataset_size)/(g[0].support_count()*Rule.find_support_count(consequent, FCP))
                        lift = round(lift,2)
                        rule = Rule(g[0].get_itemset(), pattern.get_itemset(), pattern.get_object(), lift, 1.0)
                        AR_E.append(rule)
                else:
                    if g[1].get_itemset().issubset(pattern.get_itemset()):
                        confidence = float(len(pattern.get_object()))/float(len(g[0].get_object()))
                        confidence = round(confidence,2)
                        if confidence>min_confidence:
                            lift = (pattern.support_count()*dataset_size)/(g[0].support_count()*Rule.find_support_count(consequent, FCP))
                            lift = round(lift,2)
                            rule = Rule(g[0].get_itemset(), pattern.get_itemset(), pattern.get_object(), lift, confidence)
                            AR_SB.append(rule)
        
        for Fi in FCP:
            for Fj in FCP:
                if(Fi.size() < Fj.size() and Fi.get_itemset().issubset(Fj.get_itemset())):
                    confidence = float(len(Fj.get_object()))/float(len(Fi.get_object()))
                    confidence = round(confidence,2)
                    if confidence>min_confidence:
                        lift = (Fj.support_count()*dataset_size)/(Fi.support_count()*Rule.find_support_count(Fj.get_itemset()-Fi.get_itemset(), FCP))
                        lift = round(lift,2)
                        rule = Rule(Fi.get_itemset(), Fj.get_itemset(), Fj.get_object(), lift, confidence)
                        AR_PB.append(rule)
        
        return {
            "Exact": AR_E,
            "SB": AR_SB,
            "PB": AR_PB
        }
    
    def __str__(self):
        return "Rule(\n\t"+str(self._antecedent)+" => "+str(self._consequent)+"\n\tSupport: "+str(self.support())+"\n\tConfidence: "+str(self.lift())+"\n\tConfidence: "+str(self.confidence())+"\n)\n"
    



