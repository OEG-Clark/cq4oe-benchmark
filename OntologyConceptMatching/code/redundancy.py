import owlready2 as owl
import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import re
import math
from nltk.corpus import wordnet as wn
import itertools

class OWLSemanticLibrary:
    def __init__(self, owl_file_path, gen_class, redundancy_folder):
        self.owl_file_path = owl_file_path
        self.gen_class = gen_class
        self.out_folder = redundancy_folder
        # self.hybird_path = redundancy_hybird_path
        self.ontology = None
        self.concepts = {}                    # concept dictionary
        self.concept_hierarchy = nx.DiGraph() # concept hierarchy (DAG)
        self.similarity_cache = {}            # similarity cache (key includes method)
        self.load_ontology()
    
    def load_ontology(self):
        if not os.path.exists(self.owl_file_path):
            raise FileNotFoundError(f"OWL file not found: {self.owl_file_path}")
        # print(f"Loading OWL ontology: {self.owl_file_path}")
        try:
            file_iri = f"file://{os.path.abspath(self.owl_file_path)}"
            self.ontology = owl.get_ontology(file_iri).load()
            # print(f"Loaded ontology: {self.ontology.name}")
            self._extract_concepts()
            self._build_hierarchy()
            # print(f"Extracted {len(self.concepts)} concepts")
            # print(f"Built {self.concept_hierarchy.number_of_edges()} hierarchical relations")
            #print the hierarchy edges
            for u, v in self.concept_hierarchy.edges():
                print(f"{u} -> {v}")   

        except Exception as e:
            print(f"Failed to load OWL ontology: {e}")
            raise
    
    def _extract_concepts(self):
        for cls in self.ontology.classes():
            if cls.name:
                concept_name = cls.name
                label = str(cls.label.first()) if cls.label else concept_name
                comment = str(cls.comment.first()) if cls.comment else ""
                synonyms = []
                if hasattr(cls, 'hasExactSynonym'):
                    synonyms = [str(syn) for syn in cls.hasExactSynonym]
                elif hasattr(cls, 'altLabel'):
                    synonyms = [str(syn) for syn in cls.altLabel]
                self.concepts[concept_name] = {
                    'class_obj': cls,
                    'iri': str(cls.iri),
                    'label': label,
                    'comment': comment,
                    'synonyms': synonyms,
                    'ancestors': set(),
                    'descendants': set(),
                    'depth': 0
                }
    
    def _build_hierarchy(self):
        # print("Building concept hierarchy...")
        for name in self.concepts.keys():
            self.concept_hierarchy.add_node(name)
        for name, info in self.concepts.items():
            cls = info['class_obj']
            for parent in getattr(cls, "is_a", []):
                if hasattr(parent, 'name') and parent.name and parent.name in self.concepts:
                    # edge parent -> child
                    self.concept_hierarchy.add_edge(parent.name, name)
                    #
        self._calculate_concept_properties()
    
    def _calculate_concept_properties(self):
        root_nodes = [n for n in self.concept_hierarchy.nodes()
                      if self.concept_hierarchy.in_degree(n) == 0]
        # print(f"Found {len(root_nodes)} root concepts: {root_nodes[:5]}")
        for name in self.concepts:
            try:
                depths = []
                for root in root_nodes:
                    if nx.has_path(self.concept_hierarchy, root, name):
                        depths.append(nx.shortest_path_length(self.concept_hierarchy, root, name))
                self.concepts[name]['depth'] = max(depths) if depths else 0
                self.concepts[name]['ancestors'] = set(nx.ancestors(self.concept_hierarchy, name))
                self.concepts[name]['descendants'] = set(nx.descendants(self.concept_hierarchy, name))
            except Exception as e:
                # print(f"Error computing properties for concept {name}: {e}")
                self.concepts[name]['depth'] = 0

    # =============== Classical IC: IC(c) = -log p(c) / log N ∈ [0,1] ===============
    def _concept_probability(self, concept_name):
        """
     
          p(c) = (|descendants(c)| + 1) / N
       
        """
        N = max(1, len(self.concepts))
        if concept_name not in self.concepts:
            return 1.0 / N
        desc = len(self.concepts[concept_name]['descendants'])
        p = (desc + 1) / N
   
        return float(np.clip(p, 1.0/(N*1e6), 1.0))

    def _ic(self, concept_name):
        N = max(1, len(self.concepts))
        if N <= 1:
            return 0.0
        p = self._concept_probability(concept_name)
        denom = math.log(N)
        if denom <= 0:
            return 0.0
        ic = -math.log(p) / denom
        return float(np.clip(ic, 0.0, 1.0))
    # ===============================================================================

    #have a function to print all the concepts with their ic values and depth
    def print_concept_ics(self, sort_by="name"):
       
        items = []
        for name in self.concepts:
            items.append((name, self._ic(name), self.concepts[name]['depth']))
        if sort_by == "ic_desc":
            items.sort(key=lambda x: (-x[1], x[0]))
        elif sort_by == "depth":
            items.sort(key=lambda x: (x[2], x[0]))
        else:
            items.sort(key=lambda x: x[0])

        print("Concept IC values:")
        for name, ic, depth in items:
            print(f"{name}\tIC={ic:.6f}\tdepth={depth}")

    # =============== Text similarity (TF-IDF 1-2 grams + cosine) ===============
    def _textual_similarity(self, concept1, concept2):
        """English TF-IDF (word 1–2 grams) + cosine similarity in [0,1]."""
        try:
            t1 = self._build_concept_text(concept1)
            t2 = self._build_concept_text(concept2)
            if not t1 or not t2:
                return 0.0
            vectorizer = TfidfVectorizer(
                analyzer='word', ngram_range=(1, 2),
                lowercase=True, stop_words='english'
            )
            vecs = vectorizer.fit_transform([t1, t2])
            sim = cosine_similarity(vecs[0:1], vecs[1:2])[0][0]
            return float(np.clip(sim, 0.0, 1.0))
        except Exception as e:
            print(f"Textual similarity error: {e}")
            return 0.0
        #havw the exampes by the concept names, wine and Wineregion
        """ddfd 
        
        2. n-gram  segmentation

if ngram_range=(1,2)，then

"Wine"

['w', 'wi', 'i', 'in', 'n', 'ne', 'e']


"WineRegion" 

['w', 'wi', 'i', 'in', 'n', 'ne', 'e', 
 'r', 're', 'e', 'eg', 'g', 'gi', 'i', 
 'io', 'o', 'on', 'n']

3. TF-IDF vectorization eg,

['e', 'eg', 'g', 'gi', 'i', 'in', 'io', 'n', 'ne', 'o', 'on', 
 'r', 're', 'w', 'wi']

4 the the TF-IDF sparse vectors are:

Wine → [0,0,0.3,0,0.3,0.3,0,0.3,0.3,0,0,...]

WineRegion → [0.2,0.2,0.1,0.2,0.3,0.2,0.2,0.2,0.2,0.1,...]
        """

    
    

        

    def _build_concept_text(self, concept_name):
        info = self.concepts[concept_name]
        parts = [concept_name, info['label'] or "", info['comment'] or ""]
        parts.extend(info.get('synonyms', []))
        return re.sub(r'\s+', ' ', ' '.join([p for p in parts if p])).strip()
    # ========================================================================



    def Caculate_redu_hybird(self, list):
        #the total reduceny is caculate by the ic and text similarity, it read from the concept lists, get the parir of concepts
        
        list=self.gen_class
        #get the pair of concepts and caculate the redundancy
        redundancy_results = []
        pariwise=0
        for i in range(len(list)):
            for j in range(i + 1, len(list)):
                c1 = list[i]
                c2 = list[j]
                ic1 = self._ic(c1)
                ic2 = self._ic(c2)
                first_red = abs(ic1 - ic2)  # IC 差值
                text_sim = self._textual_similarity(c1, c2)  # 文本相似度
                hybird_sim = (1 - first_red) * text_sim  # 混合相似度
                # print(f"Pair: ({c1}, {c2}) | ICs: ({ic1:.6f}, {ic2:.6f}) | IC AbsDiff: {first_red:.6f} | Text Sim: {text_sim:.6f} | Hybird Sim: {hybird_sim:.6f}")  
                redundancy_results.append({
                    'Concept 1': c1,
                    'Concept 2': c2,
                    'IC 1': round(ic1, 6),
                    'IC 2': round(ic2, 6),
                    'IC AbsDiff': round(  first_red, 6),
                    'Text Similarity': round(text_sim, 6),
                    'Hybird Similarity': round(hybird_sim, 6)
                })
         #print the redundancy results
         #caculat the average redundancy

        
        
        total_hybird_sim = sum(item['Hybird Similarity'] for item in redundancy_results)
        pariwise=len(redundancy_results)

        avg_hybird_sim = total_hybird_sim / pariwise if pariwise > 0 else 0.0
        #save the redundancy results in a text file
        out_path = self.out_folder + "/Redundancy_hybird_results.txt"
        with open(out_path, 'w') as f:
            f.write(f"Redundancy results:\n")
            for item in redundancy_results:
                f.write(f"{item}\n")
            f.write(f"\nTotal pairs: {pariwise}\n")
            f.write(f"Average Hybird Similarity: {avg_hybird_sim:.6f}\n")
        # print(f"Total pairs: {pariwise}")

        # print(f"Average Hybird Similarity: {avg_hybird_sim:.6f}")
                
    def Caculate_redu_cosine(self, list):
        #the total reduceny is caculate by the ic and text similarity, it read from the concept lists, get the parir of concepts
        
        list=self.gen_class
        #get the pair of concepts and caculate the redundancy
        redundancy_results_cosine = []
        pariwise=0
        for i in range(len(list)):
            for j in range(i + 1, len(list)):
                c1 = list[i]
                c2 = list[j]
                ic1 = self._ic(c1)
                ic2 = self._ic(c2)
         
                text_sim = self._textual_similarity(c1, c2)  
                # print(f"Pair: ({c1}, {c2}) | ICs: ({ic1:.6f}, {ic2:.6f}) | Text Sim: {text_sim:.6f}")
                redundancy_results_cosine.append({
                    'Concept 1': c1,
                    'Concept 2': c2,
                    'IC 1': round(ic1, 6),
                    'IC 2': round(ic2, 6),
                    'Text Similarity': round(text_sim, 6),
                })
        total_hybird_sim = sum(item['Text Similarity'] for item in redundancy_results_cosine)
        pariwise=len(redundancy_results_cosine)
        avg_hybird_sim = total_hybird_sim / pariwise if pariwise > 0 else 0.0
        #save the redundancy results in a text file
        out_path = self.out_folder + "/Redundancy_cosine_results.txt"
        # '/Users/ljymacbook/LLMs_Ontology_experimenst/Wine/Concept_coverage/Redundancy_cosine_results.txt'
        with open(out_path, 'w') as f:
            f.write(f"Redundancy results (Text Similarity only):\n")
            for item in redundancy_results_cosine:
                f.write(f"{item}\n")
            f.write(f"\nTotal pairs: {pariwise}\n")
            f.write(f"Average Text Similarity based on cosine: {avg_hybird_sim:.6f}\n")
         #print the redundancy results
        # print(f"Total pairs: {pariwise}")
        # print(f"Average Text Similarity based on cosine: {avg_hybird_sim:.6f}")


def Caculat_redu_sysnonyms(concept_list, out_folder):
    """
    if the two conepts are synonyms in the WordNet, then they are redundant
    1. get the pair of concepts and caculate the redundancy
    2. get the 1st concept and its synonyms from WordNet
    3. get the 2nd concept and its synonyms from WordNet
    4. if the 1st concept and the 2nd concept are in the synonyms, then they are redundant,EG: concept1=Region, concept2=Area, they
    """
    redundant_pairs = []

  
    for concept1, concept2 in itertools.combinations(concept_list, 2):
        #
        synonyms1 = set()
        for synset in wn.synsets(concept1):
            for lemma in synset.lemmas():
                synonyms1.add(lemma.name().lower())

        
        synonyms2 = set()
        for synset in wn.synsets(concept2):
            for lemma in synset.lemmas():
                synonyms2.add(lemma.name().lower())

       #print the concept and its synonyms
        # print(f"Concept: {concept1}, Synonyms: {synonyms1}")
        # print(f"Concept: {concept2}, Synonyms: {synonyms2}")



        if (concept1.lower() in synonyms2 or 
            concept2.lower() in synonyms1 or 
            (synonyms1 & synonyms2)):
            redundant_pairs.append((concept1, concept2))
           #print the concept and its synonyms,which are redundant
           #print the concept and its synonyms
            
            # print(f"Redundant pair: ({concept1}, {concept2}) | Synonyms1: {synonyms1} | Synonyms2: {synonyms2}")
            #caculate the total redundant pairs
    total_redundant_pairs = len(redundant_pairs)

    # print(f"Total redundant pairs found: {total_redundant_pairs}")
    #save the redundant pairs in a text file
    avg_redundant_synonyms = total_redundant_pairs / len(concept_list) if len(concept_list) > 0 else 0.0
    #save
    out_path = out_folder + "/Redundancy_synonyms_results.txt"
    # '/Users/ljymacbook/LLMs_Ontology_experimenst/Wine/Concept_coverage/Redundancy_synonyms_results.txt'
    with open(out_path, 'w') as f:
        f.write(f"Redundant pairs based on WordNet synonyms:\n")
      #also save the concept and its synonyms
        for pair in redundant_pairs:
            f.write(f"{pair}\n")
        f.write(f"\nTotal redundant pairs: {total_redundant_pairs}\n")
        f.write(f"Average redundant pairs per concept: {avg_redundant_synonyms:.6f}\n")
    # print(f"Average redundant pairs per concept: {avg_redundant_synonyms:.6f}")
    return redundant_pairs

        #get the pair of concepts and caculate the redundancy
        #get the 1st concept and its synonyms from WordNet
        #get the 2nd concept and its synonyms from WordNet
        #if the 1st concept and the 2nd concept are in the synonyms, then they are redundant,EG: concept1=Region, concept2=Area, they are synonyms

        #check if the concept in the clauede concepts 