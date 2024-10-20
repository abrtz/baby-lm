from collections import defaultdict
from datasets import load_dataset
import json

items_per_domain = defaultdict(list)

files = ["testsuite-material_dinamico.csv",
        "testsuite-material_propiedades.csv",
        "testsuite-social_relaciones.csv"
        ]
#read the generated files from templates with load_dataset
dataset = load_dataset("csv", data_files=files) 
for example in dataset["train"]:
    domain = example["Domain"]
    items_per_domain[domain].append(example)

#prepare files for evaluation script
keys = ['MetaTemplateID', 'TemplateID', 'PairID','TemplateName','TemplateIndex','ItemTags']

for domain in items_per_domain.keys():
    with open(f"{domain}.jsonl", 'w',encoding='utf-8') as outfile:
        for item in items_per_domain[domain]:
            for key in keys:
                item.pop(key,None) #remove the fields not relevant
            outfile.write(json.dumps(item,ensure_ascii=False)+"\n")
            swapped_item = item
            # Separate examples where context/target is flipped. Makes it easier to compute accuracies
            swapped_item["Context1"], swapped_item["Context2"] = swapped_item["Context2"], swapped_item["Context1"]
            swapped_item["Target1"], swapped_item["Target2"] = swapped_item["Target2"], swapped_item["Target1"]
            outfile.write(json.dumps(swapped_item,ensure_ascii=False)+"\n") #to write the files with ortographic accent
    print(f"{domain} saved to jsonl file")
