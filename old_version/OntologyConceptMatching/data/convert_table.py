import json
import os

import pandas as pd


def load_json(json_path):
    with open(json_path, "rb") as f:
        data = json.load(f)
    return data

def process_df(json_data):
    df = pd.DataFrame(json_data)
    md = df.to_markdown()
    return md

def process_folder(folder_path, onto_name):
    concept_res_folder = folder_path + "concept/"
    concept_res_file_list = os.listdir(concept_res_folder)
    concept_res_file = concept_res_folder + onto_name + "_result.json"
    if os.path.exists(concept_res_file):
        concept_res = load_json(concept_res_file)
        concept_res_md = process_df(concept_res)
    else:
        print("An error occured during handling concept results.")
        concept_res_md = None

    property_res_folder = folder_path + "property/"
    property_res_domain = property_res_folder + onto_name + "_domains.json"
    property_res_property = property_res_folder + onto_name + "_properties.json"
    property_res_range = property_res_folder + onto_name + "_ranges.json"
    
    if os.path.exists(property_res_domain):
        domain_res = load_json(property_res_domain)
        domain_md = process_df(domain_res)
    else:
        print("An error occured during handling property domain results.")
        domain_md = None
        
    if os.path.exists(property_res_property):
        property_res = load_json(property_res_property)
        property_md = process_df(property_res)
    else:
        print("An error occured during handling property results.")
        property_md = None
        
    if os.path.exists(property_res_range):
        range_res = load_json(property_res_range)
        range_md = process_df(range_res)
    else:
        print("An error occured during handling property range results.")
        range_md = None
    
    return concept_res_md, domain_md, property_md, range_md
    
    
    
        

def get_parser():
    parser = argparse.ArgumentParser(description="Solar Annotation Pipeline")
    parser.add_argument('--user_key', default="sk-VEJr8zCy6x9MlQ0yvh7rtaxSOwf3C7WDeg7CuGOahDrEKQl8", help="Gemini Key", type=str)
    parser.add_argument('--model_id', default = "gemini-2.5-flash", help="gemini ai model reference", type=str)
    # parser.add_argument('--user_key', default="sk-0ed68dc9b79e45509d0923388497f418", help="Gemini Key", type=str)
    # parser.add_argument('--model_id', default = "deepseek-reasoner", help="gemini ai model reference", type=str)
    parser.add_argument('--paper_file_dir', help="the location of the folder of the file being annotated", type=str)
    parser.add_argument('--gt_file_path', help="the location for the ground truth annotation targets json file", type=str)
    parser.add_argument('--save_file_dir', help="the location of the folder for saving the annotated file", type=str)
    return parser