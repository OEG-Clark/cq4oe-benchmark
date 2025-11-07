from rdflib import Graph, RDF, OWL, RDFS
from rdflib.term import BNode
# Parse the  rdf into ontology file
from rdflib import Graph
from sentence_transformers import util
from langchain_ollama import OllamaEmbeddings
import difflib
import Levenshtein
import textdistance
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from redundancy import *

import re
import os
import json
import argparse
from collections import defaultdict


import nltk
from nltk.corpus import wordnet as wn

nltk.download('wordnet')

nltk.download('omw-1.4') #multilingual wordnet



def get_class_name(uri, graph):
    """Get first rdfs:label if available, otherwise extract from URI"""
    # Try to get the first rdfs:label
    labels = list(graph.objects(uri, RDFS.label))
    if labels:
        return str(labels[0])
    # Fallback: extract from URI
    uri_str = str(uri)
    if '#' in uri_str:
        return uri_str.split('#')[-1]
    else:
        return uri_str.split('/')[-1]

def extract_classes(file_path):
    g = Graph()
    if file_path[-3:] == "rdf":
        g.parse(file_path, format="xml")
    elif file_path[-3:] == "owl":
        g.parse(file_path)
    
    classes_uri = sorted(
        cls for cls in g.subjects(RDF.type, OWL.Class)
        if not isinstance(cls, BNode)
    )
    
    classes = sorted(
        cls for cls in g.subjects(RDF.type, OWL.Class)
        if not isinstance(cls, BNode)
    )
    
    processed_classes = [get_class_name(uri, g) for uri in classes]
    return processed_classes

def pre_process(gen_class, ground_class, info_type, model_id=None):
    coverage_info = []
    coverage_info_new = []
    res = []
    if model_id and info_type == "semantic":  
        encoder = OllamaEmbeddings(model=model_id)
        all_texts = ground_class + gen_class

        embeddings = encoder.embed_documents(all_texts)

        ground_embed = embeddings[:len(ground_class)]
        
        gen_embed = embeddings[len(ground_class):]
        for idx_g, g in enumerate(ground_class):
            sims = util.cos_sim(
                ground_embed[idx_g],
                gen_embed
            )[0]  
            best_idx = sims.argmax()
            coverage_info.append({
                "Gold Concept": g,
                "Exact Match": "",
                "Best Candidate Match": gen_class[best_idx],
                "Similarity": round(float(sims[best_idx]), 3)
            })
        for pred in {item["Best Candidate Match"] for item in coverage_info}:
            best = max(
                (itm for itm in coverage_info if itm["Best Candidate Match"] == pred),
                key=lambda x: x["Similarity"]
            )
            temp = {"pred": pred, "ground": best['Gold Concept'], "sim": best['Similarity']}
            # print(f"{c} -> {best['Gold Concept']} (similarity: {best['Similarity']:.2f})")
            res.append(temp)
            coverage_info_new.append(best)
    else:
        for g in ground_class:
            exact = g in gen_class
            best_match, best_score = None, 0.0
            for c in gen_class:
                if info_type == "sequence_match":
                    sim = difflib.SequenceMatcher(None, g, c).ratio()
                elif info_type == "levenshtein":
                    dist = Levenshtein.distance(g, c)
                    sim = 1 - dist / max(len(g), len(c), 1)
                elif info_type == "jaro_winkler":
                    sim = textdistance.jaro_winkler.normalized_similarity(g, c)
                else:
                    print("Metric type is not proper defined.")
                if sim > best_score:
                    best_score, best_match = sim, c
            coverage_info.append({
                "Gold Concept": g,
                "Exact Match": "yes" if exact else "",
                "Best Candidate Match": best_match,
                "Similarity": round(best_score, 3)
            })
        if info_type == "jaro_winkler":
            for pred in {item["Best Candidate Match"] for item in coverage_info}:
                best = max(
                    (itm for itm in coverage_info if itm["Best Candidate Match"] == pred),
                    key=lambda x: x["Similarity"]
                )
                temp = {"pred": pred, "ground": best['Gold Concept'], "sim": best['Similarity']}
            # print(f"{c} -> {best['Gold Concept']} (similarity: {best['Similarity']:.2f})")
                res.append(temp)
                coverage_info_new.append(best)
        else:
            for c in set(item["Best Candidate Match"] for item in coverage_info):
                best = max(
                    (itm for itm in coverage_info if itm["Best Candidate Match"] == c),
                    key=lambda x: x["Similarity"]
                )
                temp = {"pred": c, "ground": best['Gold Concept'], "sim": best['Similarity']}
            # print(f"{c} -> {best['Gold Concept']} (similarity: {best['Similarity']:.2f})")
                res.append(temp)
                coverage_info_new.append(best)
        
    avg_sim = sum(item["Similarity"] for item in coverage_info_new) / len(ground_class)
    all_concepts = sorted(set(ground_class) | set(gen_class))
    print(info_type)
    print(res)
    return coverage_info, coverage_info_new, avg_sim, all_concepts

def normalize(concept):
    return concept.lower().strip().replace('_', ' ').replace('-', ' ')

def cal_metrics(gen_class, ground_class, info_type, model_id=None):
    if info_type == "hard_match":
        all_concepts = sorted(set(ground_class) | set(gen_class))
        y_true = [1 if c in ground_class else 0 for c in all_concepts]
        y_pred = [1 if c in gen_class else 0 for c in all_concepts]
        avg_sim = len(set(gen_class) & set(ground_class)) / len(ground_class)
        accuracy  = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall    = recall_score(y_true, y_pred, zero_division=0)
        f1        = f1_score(y_true, y_pred, zero_division=0)

    else:
        coverage_info, coverage_info_new, avg_sim, all_concepts = pre_process(gen_class, ground_class, info_type, model_id)


        sim_map = { itm["Best Candidate Match"]: itm["Similarity"] for itm in coverage_info_new }
        y_true  = [1 if concept in ground_class else 0 for concept in all_concepts]
        y_score = [sim_map.get(concept, 0.0) for concept in all_concepts]

        # TP = sum(y_true[i] * y_score[i]       for i in range(len(all_concepts)))
        # FP = sum((1 - y_true[i]) * y_score[i] for i in range(len(all_concepts)))
        # FN = sum(y_true[i] * (1 - y_score[i]) for i in range(len(all_concepts)))
        # TN = sum((1 - y_true[i]) * (1 - y_score[i]) for i in range(len(all_concepts)))
        # print(f"TP={TP}, FP={FP}, FN={FN}, TN={TN}")

        TP = sum(item["Similarity"] for item in coverage_info_new)
        FN = sum(1 - item["Similarity"] for item in coverage_info_new)
        matched = [item["Best Candidate Match"] for item in coverage_info_new]
        FP = len([c for c in gen_class if c not in matched])
        # FN = len([c for c in matched if c not in gen_class])
        print(f"TP={TP}, FP={FP}, FN={FN}")
        

        precision = TP / (TP + FP) if TP + FP else 0.0
        recall    = TP / (TP + FN) if TP + FN else 0.0
        # accuracy  = (TP + TN) / len(all_concepts)
        accuracy  = TP / len(ground_class) if len(ground_class) else 0.0
        f1        = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

        print(f"Precision: {precision}")
        print(f"Recall:    {recall}")
        print(f"Accuracy:  {accuracy}")
        print(f"F1-score:  {f1}")
    return avg_sim, precision, recall, accuracy, f1

def _normalize(text: str) -> str:
    
    t = (text or "").strip().lower()
    t = t.replace('_', ' ').replace('-', ' ')
    t = re.sub(r'\s+', ' ', t)
    return t

def wordnet_noun_synonyms(term: str) -> set:
    """

    """
    base = _normalize(term)
    syns = set()

    variants = {base, base.replace(' ', '_')}
    for v in variants:
        for s in wn.synsets(v, pos=wn.NOUN):
            for lemma in s.lemmas():
                name = lemma.name()
                norm = _normalize(name)
                if norm and norm != base:
                    syns.add(norm)
    return syns


def cal_synonym(gen_class, ground_class):
    synonyms_map = { g: wordnet_noun_synonyms(g) for g in ground_class }
    expanded_ground_class = set(ground_class)
    for syns in synonyms_map.values():
        expanded_ground_class.update(syns)
    expanded_ground_class = sorted(expanded_ground_class)
    all_concepts = sorted(set(expanded_ground_class) | set(gen_class))
    y_true = [1 if c in ground_class else 0 for c in all_concepts]
    y_pred = [1 if c in gen_class else 0 for c in all_concepts]
    coverage_rate = len(set(gen_class) & set(expanded_ground_class)) / len(expanded_ground_class)
    TP = sum(y_true[i] * y_pred[i] for i in range(len(all_concepts)))
    FP = sum((1 - y_true[i]) * y_pred[i] for i in range(len(all_concepts)))
    FN = sum(y_true[i] * (1 - y_pred[i]) for i in range(len(all_concepts)))
    TN = sum((1 - y_true[i]) * (1 - y_pred[i]) for i in range(len(all_concepts)))
    print(f"TP={TP}, FP={FP}, FN={FN}, TN={TN}")
    
    precision = TP / (TP + FP) if TP + FP else 0.0
    recall    = TP / (TP + FN) if TP + FN else 0.0
    accuracy  = (TP + TN) / len(all_concepts)
    f1        = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    print(f"Precision: {precision}")
    print(f"Recall:    {recall}")
    print(f"Accuracy:  {accuracy}")
    print(f"F1-score:  {f1}")
    return coverage_rate, precision, recall, accuracy, f1


def strtobool(val):
    """Conver a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_parser():
    parser = argparse.ArgumentParser(description="Evaluation of the generated ontology")
    parser.add_argument('--model_id', default = "embeddinggemma", help="""string of ollama embedding model id, if more models needed, please using "," to seperate them""", type=str)
    parser.add_argument('--generate_onto_file_path', help="the location of generated ontology file ", type=str)
    parser.add_argument('--ground_onto_file_path', help="the location of ground truth ontology file", type=str)
    parser.add_argument('--save_file_path', help="the location of the saved result that contains lexical ", type=str)
    parser.add_argument('--redundancy_folder', default="/home/jovyan/LLMOnto/Benchmark/OntologyConceptMatching/software/redundancy", help="the location of the saved result of redundancy check", type=str)
    return parser


def main():
    para_parser = get_parser()
    args = para_parser.parse_args()
    args_dict = vars(args)
    model_id = args_dict["model_id"]
    gen_class = extract_classes(args_dict["generate_onto_file_path"])
    ground_class = extract_classes(args_dict["ground_onto_file_path"])
    
    normalized_gen_class =  [normalize(c) for c in gen_class]
    normalized_ground_class =  [normalize(c) for c in ground_class]
    info_list = [
        "hard_match",
        "sequence_match",
        "levenshtein",
        "jaro_winkler",
        "semantic",
        "synonym"
    ]
    result = {}
    for info_type in info_list:
        if info_type == "synonym":
            coverage_rate, precision, recall, accuracy, f1 = cal_synonym(normalized_gen_class, normalized_ground_class)
            result[info_type] = {
                "coverage_rate": coverage_rate,
                "precision": precision,
                "recall": recall,
                "accuracy": accuracy,
                "f1": f1
            }
        elif info_type == "semantic":
            for _model_id in model_id.split(","):
                avg_sim, precision, recall, accuracy, f1 = cal_metrics(normalized_gen_class, normalized_ground_class, info_type, _model_id)
                info_id = info_type + "_" + _model_id
                result[info_id] = {
                    "coverage_rate": avg_sim,
                    "precision": precision,
                    "recall": recall,
                    "accuracy": accuracy,
                    "f1": f1
                }
        else:
            avg_sim, precision, recall, accuracy, f1 = cal_metrics(normalized_gen_class, normalized_ground_class, info_type, model_id)
            result[info_type] = {
                "coverage_rate": avg_sim,
                "precision": precision,
                "recall": recall,
                "accuracy": accuracy,
                "f1": f1
            }
    print(result)
    ### Redundancy
    lib = OWLSemanticLibrary(args_dict["generate_onto_file_path"], gen_class, args_dict["redundancy_folder"])
    caculat_redu_hybird = lib.Caculate_redu_hybird(gen_class)
    caculat_redu_cosine = lib.Caculate_redu_cosine(gen_class)
    caculat_redu_sysnonyms = Caculat_redu_sysnonyms(gen_class, args_dict["redundancy_folder"])
    with open(args_dict["save_file_path"], "w") as f:
        json.dump(result, f)


main()