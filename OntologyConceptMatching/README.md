# Ontology Concept Matching

The Ontology Concept Label Matching task evaluates how well large language models (LLMs) can generate concept names that correctly correspond to the standard class labels defined in ontology.


## Evaluation

To evaluate the models’ ability to **recognize**, **name**, and **align** ontology concepts accurately, we employ the following quantitative metrics:

- **Precision**
- **Recall**
- **F1-score**
- **Accuracy**
- **Coverage Rate**

These metrics jointly measure the **correctness**, **completeness**, and **consistency** of the model outputs with respect to the original ontology.

### Precision

**Precision** measures the proportion of correctly predicted ontology classes among all classes predicted by the model.

**Definition:**

Precision = True Positives (TP) / [True Positives (TP) + False Positives (FP)]

**Interpretation:**

A higher Precision indicates that the model makes fewer false predictions when identifying ontology classes.

---

### Recall

**Recall** measures how many of the actual (gold) ontology classes are correctly identified by the model.

**Definition:**

**Definition:**

Recall = True Positives (TP) / [True Positives (TP) + False Negatives (FN)]

**Interpretation:**

A higher Recall means the model retrieves a larger portion of the gold ontology concepts, reflecting better coverage of true classes.

---

### F1-score

**F1-score** represents the harmonic mean of Precision and Recall, balancing both correctness and completeness.

**Definition:**

F1-score = 2 × (Precision × Recall) / (Precision + Recall)

**Interpretation:**

A higher F1-score indicates the model maintains both high Precision and high Recall in recognizing ontology concepts.

---

### Accuracy

**Accuracy** measures the overall proportion of correctly classified ontology concepts among all predictions.

**Definition:**

Accuracy = Number of correct predictions / Total number of predictions

**Interpretation:**

A higher Accuracy reflects that the model consistently aligns its predicted ontology concepts with the gold ontology.

---

### Coverage Rate

The **Coverage Rate** is introduced to assess how comprehensively the model-generated labels represent the classes in the reference ontology.

**Definition:**

Coverage Rate = Number of matched gold classes / Total number of gold classes

**Interpretation:**

A higher Coverage Rate indicates that the model not only produces accurate labels but also covers a **broader range of ontology concepts**.

---

### Computation Techniques for Evaluation Metrics

**Hard Match Ratio**: Evaluates whether the generated label exactly matches the same label from the original ontology

**Information Content(IC) Score from WordNet**:


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





