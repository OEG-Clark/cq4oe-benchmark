from rdflib import Graph, RDF, OWL, RDFS
from rdflib.term import BNode, URIRef, Literal
# Parse the  rdf into ontology file
from rdflib import Graph
from sentence_transformers import util
from langchain_ollama import OllamaEmbeddings
import difflib
import Levenshtein
import textdistance
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from redundancy import * # Removed this import as the file was not provided

import re
import os
import json
import argparse
from collections import defaultdict
from fuzzywuzzy import fuzz


def get_clean_name(uri, graph):
    """Get rdfs:label if available, otherwise extract from URI."""
    if not isinstance(uri, URIRef):
        if isinstance(uri, Literal):
            if '#' in str(uri):
                return str(uri).split('#')[-1]
            return str(uri)
        return str(uri)
        
    labels = list(graph.objects(uri, RDFS.label))
    if labels:
        return str(labels[0])
    
    uri_str = str(uri)
    if '#' in uri_str:
        return uri_str.split('#')[-1]
    else:
        return uri_str.split('/')[-1]


def get_union_classes(node, graph):
    """Handle owl:unionOf constructs (return member classes)."""
    classes = []
    if isinstance(node, BNode):
        for union in graph.objects(node, OWL.unionOf):
            for member in graph.items(union):
                classes.append(member)
    else:
        classes.append(node)
    return classes




def get_property_function(prop_uri, graph):
  
    features = []

    # FunctionalProperty
    if (prop_uri, RDF.type, OWL.FunctionalProperty) in graph:
        features.append("Functional")

    # InverseFunctionalProperty
    if (prop_uri, RDF.type, OWL.InverseFunctionalProperty) in graph:
        features.append("InverseFunctional")

    # SymmetricProperty
    if (prop_uri, RDF.type, OWL.SymmetricProperty) in graph:
        features.append("Symmetric")

    # AsymmetricProperty
    if (prop_uri, RDF.type, OWL.AsymmetricProperty) in graph:
        features.append("Asymmetric")

    # TransitiveProperty
    if (prop_uri, RDF.type, OWL.TransitiveProperty) in graph:
        features.append("Transitive")

    # ReflexiveProperty
    if (prop_uri, RDF.type, OWL.ReflexiveProperty) in graph:
        features.append("Reflexive")

    # IrreflexiveProperty
    if (prop_uri, RDF.type, OWL.IrreflexiveProperty) in graph:
        features.append("Irreflexive")

    return features if features else ["None"]


def extract_property_data(file_path, graph):
    """
    Extract ObjectProperty and DatatypeProperty definitions, 
    including domain/range/subPropertyOf (with unionOf support).
    """
    print(f"Parsing properties from: {file_path}")

    object_properties = list(graph.subjects(RDF.type, OWL.ObjectProperty))
    datatype_properties = list(graph.subjects(RDF.type, OWL.DatatypeProperty))
    all_properties = sorted(object_properties + datatype_properties)

    extracted_data = {}

    for prop_uri in all_properties:
        if isinstance(prop_uri, BNode):
            continue  # skip blank nodes

        prop_name = get_clean_name(prop_uri, graph)
        if not prop_name:
            continue

        # --- Handle union domains ---
        domain_nodes = list(graph.objects(prop_uri, RDFS.domain))
        domain_classes = []
        for d in domain_nodes:
            for c in get_union_classes(d, graph):
                domain_classes.append(get_clean_name(c, graph))
        domain_name = ", ".join(sorted(set(domain_classes))) if domain_classes else "None"

        # --- Handle union ranges ---
        range_nodes = list(graph.objects(prop_uri, RDFS.range))
        range_classes = []
        for r in range_nodes:
            for c in get_union_classes(r, graph):
                range_classes.append(get_clean_name(c, graph))
        range_name = ", ".join(sorted(set(range_classes))) if range_classes else "None"

        # --- Handle subPropertyOf (may have multiple parents) ---
        parent_props = []
        for parent in graph.objects(prop_uri, RDFS.subPropertyOf):
            if not isinstance(parent, BNode):
                parent_props.append(get_clean_name(parent, graph))
        parent_props = sorted(set(parent_props)) if parent_props else []

        # --- Construct final dictionary entry ---
        extracted_data[prop_name] = {
            "type": "ObjectProperty" if prop_uri in object_properties else "DatatypeProperty",
            "domain": domain_name,
            "range": range_name,
            "subProperties": parent_props,
            "function": get_property_function(prop_uri, graph)
        }

    return extracted_data



def get_property_names(prop_dict):
    """Extracts just the property names (keys) as a list."""
    return sorted(list(prop_dict.keys()))

def get_property_types(prop_dict):
    """
    Extracts property-type pairs (ObjectProperty or DatatypeProperty) 
    as a list of formatted strings.
    """
    type_list = []
    for prop_name, details in prop_dict.items():
       
        prop_type = details.get('type', 'Unknown')
        prop_string = f"Property: {prop_name}\nType: {prop_type}"
        type_list.append(prop_string)
    return sorted(type_list)


def get_property_domains(prop_dict):
    """Extracts property-domain pairs as a list of formatted strings."""
    domain_list = []
    for prop_name, details in prop_dict.items():
        prop_string = f"Property: {prop_name}\nDomain: {details['domain']}"
        domain_list.append(prop_string)
    return sorted(domain_list)

def get_property_ranges(prop_dict):
    """Extracts property-range pairs as a list of formatted strings."""
    range_list = []
    for prop_name, details in prop_dict.items():
        prop_string = f"Property: {prop_name}\nRange: {details['range']}"
        range_list.append(prop_string)
    return sorted(range_list)

def pre_process(gen_props, ground_props, info_type, model_id=None):
    coverage_info = []
    coverage_info_new = []
    res = []
    if model_id and info_type == "semantic":  
        encoder = OllamaEmbeddings(model=model_id)
        all_texts = ground_props + gen_props

        embeddings = encoder.embed_documents(all_texts)

        ground_embed = embeddings[:len(ground_props)]
        
        gen_embed = embeddings[len(ground_props):]
        for idx_g, g in enumerate(ground_props):
            # Handle potential empty list for gen_embed
            if not gen_embed:
                sims = []
            else:
                sims = util.cos_sim(
                    ground_embed[idx_g],
                    gen_embed
                )[0]
                
            if sims is not None and len(sims) > 0:
                best_idx = sims.argmax()
                best_match_prop = gen_props[best_idx]
                best_sim = round(float(sims[best_idx]), 3)
            else:
                best_match_prop = "None"
                best_sim = 0.0

            coverage_info.append({
                "Gold Concept": g,
                "Exact Match": "",
                "Best Candidate Match": best_match_prop,
                "Similarity": best_sim
            })
            
        for pred in {item["Best Candidate Match"] for item in coverage_info}:
            if pred == "None": continue
            best = max(
                (itm for itm in coverage_info if itm["Best Candidate Match"] == pred),
                key=lambda x: x["Similarity"]
            )
            temp = {"pred": pred, "ground": best['Gold Concept'], "sim": best['Similarity']}
            res.append(temp)
            coverage_info_new.append(best)
    else:
        for g in ground_props:
            exact = g in gen_props
            best_match, best_score = None, 0.0
            for c in gen_props:
                if info_type == "sequence_match":
                    sim = difflib.SequenceMatcher(None, g, c).ratio()
                elif info_type == "levenshtein":
                    dist = Levenshtein.distance(g, c)
                    sim = 1 - dist / max(len(g), len(c), 1)
                elif info_type == "jaro_winkler":
                    sim = textdistance.jaro_winkler.normalized_similarity(g, c)
                else:
                    print(f"Metric type '{info_type}' is not properly defined.")
                    sim = 0.0 # Default sim to 0 if type is wrong
                if sim > best_score:
                    best_score, best_match = sim, c
            coverage_info.append({
                "Gold Concept": g,
                "Exact Match": "yes" if exact else "",
                "Best Candidate Match": best_match,
                "Similarity": round(best_score, 3)
            })
            
        for pred in {item["Best Candidate Match"] for item in coverage_info}:
            if pred is None: continue
            
            matching_items = [itm for itm in coverage_info if itm["Best Candidate Match"] == pred]
            if not matching_items:
                continue
                
            best = max(matching_items, key=lambda x: x["Similarity"])
            
            temp = {"pred": pred, "ground": best['Gold Concept'], "sim": best['Similarity']}
            res.append(temp)
            coverage_info_new.append(best)
        
    avg_sim = sum(item["Similarity"] for item in coverage_info_new) / len(ground_props) if ground_props else 0.0
    all_concepts = sorted(set(ground_props) | set(gen_props))
    
    
    res_sorted = sorted(res, key=lambda x: x['sim'], reverse=True)
    
    return coverage_info, coverage_info_new, avg_sim, all_concepts

def normalize(concept):
    return concept.lower().strip().replace('_', ' ').replace('-', ' ')

def cal_metrics(gen_props, ground_props, info_type, model_id=None):
    if info_type == "hard_match":
        all_concepts = sorted(set(ground_props) | set(gen_props))
        
        matches = [c for c in all_concepts if c in ground_props and c in gen_props]
        unmatched_generated = [c for c in all_concepts if c in gen_props and c not in ground_props]
        unmatched_ground = [c for c in all_concepts if c in ground_props and c not in gen_props]

        y_true = [1 if c in ground_props else 0 for c in all_concepts]
        y_pred = [1 if c in gen_props else 0 for c in all_concepts]
        avg_sim = len(matches) / len(ground_props) if ground_props else 0.0
        accuracy  = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall    = recall_score(y_true, y_pred, zero_division=0)
        f1        = f1_score(y_true, y_pred, zero_division=0)

    else:
        coverage_info, coverage_info_new, avg_sim, all_concepts = pre_process(gen_props, ground_props, info_type, model_id)

        sim_map = { itm["Best Candidate Match"]: itm["Similarity"] for itm in coverage_info_new }
        y_true  = [1 if c in ground_props else 0 for c in all_concepts]
        y_score = [sim_map.get(concept, 0.0) for concept in all_concepts]

        TP = sum(item["Similarity"] for item in coverage_info_new)
        FN = sum(1 - item["Similarity"] for item in coverage_info_new)
        
        matched_gen_props = {item["Best Candidate Match"] for item in coverage_info_new}
        FP = len([c for c in gen_props if c not in matched_gen_props])
        
        print(f"TP={TP}, FP={FP}, FN={FN}")
        
        precision = TP / (TP + FP) if TP + FP else 0.0
        recall    = TP / (TP + FN) if TP + FN else 0.0
        accuracy  = TP / len(ground_props) if len(ground_props) else 0.0
        f1        = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

        print(f"\n--- {info_type} Aggregate Scores ---")
        print(f"Precision: {precision}")
        print(f"Recall:    {recall}")
        print(f"Accuracy:  {accuracy}")
        print(f"F1-score:  {f1}")
    
    return avg_sim, precision, recall, accuracy, f1

def evaluate_hard_type_match(gen_props_dict, ground_props_dict):
    match_results = []
    res_check = 0
    
    for ground_name, ground_details in ground_props_dict.items():
        ground_type = ground_details.get('type', '')
        
        match_found_for_this_property = False

        for gen_name, gen_details in gen_props_dict.items():

            if fuzz.token_set_ratio(str(ground_name), str(gen_name)) == 100:
                
                gen_type = gen_details.get('type', '')

                if fuzz.token_set_ratio(str(ground_type), str(gen_type)) == 100:
                    res_check += 1
                    match_results.append(1) # Match found (Name + Type)
                    match_found_for_this_property = True
                    break # Stop searching generated props for this ground prop

        if not match_found_for_this_property:
            match_results.append(0)

    print(f"Internal check count (res_check): {res_check}")
    print(f"Hard type match results (1=Match, 0=Mismatch): {match_results}")
    print(f"Total properties in ground truth: {len(ground_props_dict)}")
    print(f"Total matches: {sum(match_results)}")
    
    return match_results

def evaluate_function_conflict(gen_props_dict, ground_props_dict):
    conflict_list = []

    ground_names = sorted(list(ground_props_dict.keys()))
    
    if not ground_names:
        print("Ground truth dictionary is empty.")
        return []

    print(f"Checking {len(ground_names)} ground properties.")

    for name in ground_names:

        if name not in gen_props_dict:
            conflict_list.append(0) 
            continue

        gen_functions = set(gen_props_dict[name]["function"]) - {"None"}
        ground_functions = set(ground_props_dict[name]["function"]) - {"None"}

        if not gen_functions or not ground_functions:

            conflict_list.append(1)
            continue

        is_conflict = False

        for a, b in CONFLICT_PAIRS:

            if ((a in gen_functions and b in ground_functions) or
                (b in gen_functions and a in ground_functions)):
                is_conflict = True
                break
        
        if is_conflict:
            conflict_list.append(0)
        else:
            conflict_list.append(1)
            
    print(f"Function conflict results (1=No Conflict, 0=Conflict/Miss): {conflict_list}")
    print(f"Total properties checked (ground truth size): {len(ground_names)}")
    print(f"Total conflicts/misses found: {len(ground_names) - sum(conflict_list)}")
    
    return conflict_list

def calculate_binary_metrics(binary_list):
    if not binary_list:
        return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}
        
    y_true = np.ones(len(binary_list), dtype=int)

    y_pred = np.array(binary_list, dtype=int)

    TP = np.sum(y_pred)
    FN = len(y_true) - TP
    
    accuracy = accuracy_score(y_true, y_pred)

    recall = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
    precision = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
    
    f1 = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
    print(f"  True Positives (Successes): {TP}")
    print(f"  False Negatives (Failures/Misses): {FN}")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1-score: {f1:.4f}")
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

def _normalize(text: str) -> str:
    t = (text or "").strip().lower()
    t = t.replace('_', ' ').replace('-', ' ')
    t = re.sub(r'\s+', ' ', t)
    return t

def strtobool(val):
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_parser():
    """(Original function from eval.py)"""
    parser = argparse.ArgumentParser(description="Evaluation of the generated ontology properties")
    parser.add_argument('--model_id', default = "embeddinggemma", help="""string of ollama embedding model id, if more models needed, please using "," to seperate them""", type=str)
    parser.add_argument('--generate_onto_file_path', help="the location of generated ontology file ", type=str)
    parser.add_argument('--ground_onto_file_path', help="the location of ground truth ontology file", type=str)
    parser.add_argument('--save_file_name', help="the *base* location of the saved result. Will be suffixed with _properties.json, _domains.json, _ranges.json ", type=str)
    return parser

# --- NEW EVALUATION SUITE FUNCTION ---

def run_evaluation_suite(gen_list_raw, ground_list_raw, model_id, info_list):
    """
    NEW: Runs the full set of metrics on a pair of string lists.
    Returns a dictionary of results.
    """
    # Normalize the lists for string comparison
    normalized_gen_list = [normalize(c) for c in gen_list_raw]
    normalized_ground_list = [normalize(c) for c in ground_list_raw]
    
    result_suite = {}
    for info_type in info_list:
        print(f"\n--- Calculating {info_type} metrics ---")
        if info_type == "semantic":
            for _model_id in model_id.split(","):
                avg_sim, precision, recall, accuracy, f1 = cal_metrics(
                    normalized_gen_list, normalized_ground_list, info_type, _model_id
                )
                info_id = info_type + "_" + _model_id
                result_suite[info_id] = {
                    "coverage_rate": avg_sim, "precision": precision,
                    "recall": recall, "accuracy": accuracy, "f1": f1
                }
        else:
            avg_sim, precision, recall, accuracy, f1 = cal_metrics(
                normalized_gen_list, normalized_ground_list, info_type, model_id
            )
            result_suite[info_type] = {
                "coverage_rate": avg_sim, "precision": precision,
                "recall": recall, "accuracy": accuracy, "f1": f1
            }
    
    return result_suite

# --- END NEW EVALUATION SUITE FUNCTION ---


def main():
    para_parser = get_parser()
    args = para_parser.parse_args()
    args_dict = vars(args)
    model_id = args_dict["model_id"]

    # --- Load Graphs ---
    try:
        gen_graph = Graph().parse(args_dict["generate_onto_file_path"], format="xml")
    except Exception as e:
        print(f"Error parsing generated file: {e}")
        return
        
    try:
        ground_graph = Graph().parse(args_dict["ground_onto_file_path"], format="xml")
    except Exception as e:
        print(f"Error parsing ground truth file: {e}")
        return

    # --- 1. Extract Dictionaries ---
    print("Extracting property data from generated ontology...")
    gen_props_dict = extract_property_data(args_dict["generate_onto_file_path"], gen_graph)
    print(f"Found {len(gen_props_dict)} properties.")
    
    print("Extracting property data from ground truth ontology...")
    ground_props_dict = extract_property_data(args_dict["ground_onto_file_path"], ground_graph)
    print(f"Found {len(ground_props_dict)} properties.")
    
    

    
    # Property Names
    gen_prop_names = get_property_names(gen_props_dict)
    ground_prop_names = get_property_names(ground_props_dict)
    
    #Run type & function evaluation
    type_list = evaluate_hard_type_match(gen_props_dict, ground_props_dict)
    func_list = evaluate_function_conflict(gen_props_dict, ground_props_dict)
    
    type_res = calculate_binary_metrics(type_list)
    func_res = calculate_binary_metrics(func_list)
    
    with open(args_dict["save_file_name"] + "_property_type.json", "w") as f:
        json.dump(type_res, f)
        
    with open(args_dict["save_file_name"] + "_property_function.json", "w") as f:
        json.dump(func_res, f)
    
    
    gen_domain_strings = get_property_domains(gen_props_dict)
    ground_domain_strings = get_property_domains(ground_props_dict)

    # Property Ranges
    gen_range_strings = get_property_ranges(gen_props_dict)
    ground_range_strings = get_property_ranges(ground_props_dict)
    
    # --- 3. Run Evaluation Suites ---
    info_list = ["hard_match", "sequence_match", "levenshtein", "jaro_winkler", "semantic"]
    
    print("\n" + "="*40)
    print("  1. EVALUATING PROPERTY NAMES")
    print("="*40)
    prop_results = run_evaluation_suite(gen_prop_names, ground_prop_names, model_id, info_list)
    print(prop_results)
    
    with open(args_dict["save_file_name"] + "_properties.json", "w") as f:
        json.dump(prop_results, f)
    
   
    print("\n" + "="*40)
    print("  2. EVALUATING PROPERTY DOMAINS")
    print("="*40)
    domain_results = run_evaluation_suite(gen_domain_strings, ground_domain_strings, model_id, info_list)
    print(domain_results)
    
    with open(args_dict["save_file_name"] + "_domains.json", "w") as f:
        json.dump(domain_results, f)
        
        
    print("\n" + "="*40)
    print("  3. EVALUATING PROPERTY RANGES")
    print("="*40)
    range_results = run_evaluation_suite(gen_range_strings, ground_range_strings, model_id, info_list)
    print(range_results)
    
    with open(args_dict["save_file_name"] + "_ranges.json", "w") as f:
        json.dump(range_results, f)
    
    print(type_list)
    print(func_list)
    
if __name__ == "__main__":
    main()