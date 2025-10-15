# Ontology Concept Matching

The Ontology Concept Label Matching task evaluates how well large language models (LLMs) can generate concept names that correctly correspond to the standard class labels defined in  ontology.


## Evaluation

### Evaluation Quantitative Measurement

To assess the model’s ability to recognize, name, and match ontology concepts accurately, we use quantitative metrics such as Precision, Recall, F1 score, Accuracy, and Coverage Rate to measure correctness completeness, and consistency with the original ontology. Noted that Coverage Rate is introduced to evaluate how comprehensively the model-generated labels represent the original ontology. Coverage Rate=Number of matched gold classes/Total number of gold classes. ​A higher Coverage Rate indicates that the LLM not only produces accurate labels but also covers a wider range of ontology concepts.

### Evaluation Metrics

**Hard Match Ratio**: Evaluates whether the generated label exactly matches the same label from the original ontology

**Sequence Match Ratio**: Uses sequence alignment techniques to evaluate token-level ordering and overlap between labels.

**Levenshtein Distance**: Measures the minimum number of character edits required to transform one label into another. It reflects spelling-level closeness and robustness to minor typographical variations. [link](https://en.wikipedia.org/wiki/Levenshtein_distance)

**Jaro–Winkler Distance**: Gives higher weight to common prefixes, making it effective for comparing labels that share morphological roots. [link](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)

**Synonyms**: Determines whether predicted and ground_truth labels are synonymous according to WordNet lexical relations. This allows recognition of semantically equivalent labels expressed in different words (e.g., “car” vs. “automobile”).

**Semantic Cosine Similarity**: Captures sentence-level semantic similarity using contextual embeddings derived from embedding models.

## Execution

1. install [ollama](https://ollama.com/) with correspond models and start the service
2. pip install -r requirements.txt 
3. run the following command line in the `code` folder
```bash
python eval.py --model_id embeddinggemma,nomic-embed-text --generate_onto_file_path generated_software.owl --ground_onto_file_path ground_software.owl --save_file_path result.json 
```



