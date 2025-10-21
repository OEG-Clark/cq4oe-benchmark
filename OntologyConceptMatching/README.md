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

A higher Coverage Rate indicates that the model not only produces accurate labels but also covers a broader range of ontology concepts.

---

### Computation Techniques for Evaluation Metrics

To compute the above evaluation metrics, each generated ontology label is compared with the reference ontology to determine whether it constitutes a True Positive (TP), False Positive (FP), False Negative (FN), or True Negative (TN) case.
Since the space of all possible negative ontology terms is unbounded, True Negatives (TN) are not explicitly counted in practice; only TP, FP, and FN are used to derive the quantitative metrics.

**Hard Match Ratio**:
This technique evaluates whether the generated label exactly matches the corresponding label in the original ontology at the lexical level. It applies a strict string comparison only identical labels are counted as correct matches, without considering semantic similarity or morphological variation.

For example, if the LLM generates the concept “wineRegion” while the original ontology contains the label “wine”, the two are considered non-matching because their surface forms differ. In this case, the result produces one False Positive (the extra generated label) and one False Negative (the missing gold label). Conversely, if the model generates “wine”, it is counted as a True Positive match.

**Information Content(IC) from WordNet**:
the Information Content (IC) Score provides a semantic-level comparison between generated and reference ontology labels. This method quantifies how specific a concept is based on its frequency in a reference corpus such as Brown or SemCor, less frequent concepts have higher IC values, indicating greater semantic specificity.

Each ontology label is mapped to its corresponding WordNet synset, and its IC value is retrieved from a precomputed dictionary (e.g., ic-brown.dat). Semantic similarity between generated and gold labels is then computed using measures such as Resnik, Lin, or Jiang-Conrath similarity.

For example, “wine” exists in WordNet as wine.n.01, enabling direct computation of its IC score. In contrast, the compound term “wineRegion” does not appear as a single lemma, resulting in an empty synset list when queried. In such cases, the term is decomposed into its sub-concepts (“wine” and “region”), and their IC values are aggregated (e.g., averaged or summed) to estimate the overall value.
However, since several LLM-generated labels are not included in the WordNet vocabulary, IC computation occasionally triggered an IndexError: list index out of range. To ensure consistency and computational stability, this technique was **excluded** from our experiments.

**Sequence Match Ratio**: 
This technique evaluates the degree of token-level similarity and ordering between the generated and reference ontology labels using sequence alignment. Instead of requiring exact string equality, it measures how closely the character or token sequences align, thereby capturing partially matching or reordered expressions (e.g., “wine region” vs. “region of wine”).

In practice, each gold concept is compared pairwise with all LLM-generated concepts using the SequenceMatcher ratio from Python difflib library.
For every gold label, the generated label that yields the highest similarity score is selected as its candidate match.
This maximum similarity value reflects how well the generated concept semantically corresponds to the gold standard concept.

In the soft-match setting, the True Positive (TP) is defined as the sum of these maximal similarity scores across all gold concepts, representing the overall matching strength. A False Positive (FP) occurs when a generated concept is not selected as the best match for any gold concept, indicating that it has no sufficiently similar counterpart in the gold set. Conversely, a False Negative (FN) denotes the residual dissimilarity of gold concepts that are not adequately represented by any generated label.
For example, given the gold concept “wine” and the generated concepts “wineRegion” and “reaWeine”, the pair (“wine”, “wineRegion”) may achieve the highest similarity score (e.g., 0.92) and is thus treated as a True Positive contribution, while other lower-scoring pairs are ignored.

**Levenshtein Distance**: The lexical similarity between two concept labels is computed using the SequenceMatcher ratio from Python difflib library, which approximates the Levenshtein edit distance.[link](https://en.wikipedia.org/wiki/Levenshtein_distance)
This technique measures the minimum number of character level operations insertions, deletions, or substitutions required to transform one label into another.
It thus captures the degree of spelling-level closeness between two terms and provides robustness to minor typographical or morphological variations in label names.
Following the the soft-match setting in Sequence match technique, for each gold label, the generated concept with the highest similarity score is selected as its match, and these best-matching pairs collectively define the True Positive (TP) through the sum of their maximal similarity scores.

**Jaro–Winkler Distance**: The lexical similarity between two concept labels can also be measured using the Jaro–Winkler distance, an extension of the Jaro metric that gives higher weights to common prefixes between strings. [link](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance)
This technique evaluates both the number and order of matching characters, producing a normalized score in the range [0,1] where 1 indicates an exact match.
By emphasizing the agreement of initial substrings, the Jaro–Winkler distance becomes particularly effective for comparing concept labels that share morphological roots or hierarchical naming patterns (e.g., “wineRegion” and “wineType”).
Following the same soft-match setting as in the SequenceMatcher technique, each gold label is paired with the generated label that achieves the highest Jaro–Winkler similarity, and these best-matching pairs collectively contribute to the True Positive (TP) computation.

**Synonyms from WordNet**:Determines whether predicted and reference labels are semantically synonymous according to lexical relations defined in WordNet. This is also one hard matching to identifie concept pairs that are semantically equivalent even when expressed through different lexical forms.
A prediction is counted as a True Positive (TP) if it exactly matches a gold label or one of its WordNet synonyms, reflecting strict semantic equivalence between generated and gold-standard concepts.

**Semantic Cosine Similarity**: Captures sentence semantic similarity using contextual embeddings generated by pretrained language models such as BERT, RoBERTa, or Sentence-BERT. In this approach, each concept label is represented as a dense vector in a semantic embedding space, and similarity between a gold and a predicted label is computed as the cosine of the angle between their corresponding embedding vectors.
This metric effectively captures meaning level correspondence even when two labels share few or no common tokens (e.g., “human” vs. “person”).
Following the soft-matching setting, each gold concept is paired with the generated label that yields the highest cosine similarity, and these best-matching pairs collectively contribute to the True Positive (TP) computation through the sum of their maximal similarity scores, representing the overall semantic alignment between generated and gold concepts.
## Execution

1. install [ollama](https://ollama.com/) with correspond models and start the service
2. pip install -r requirements.txt 
3. run the following command line in the `code` folder
```bash
python eval.py --model_id embeddinggemma,nomic-embed-text --generate_onto_file_path generated_software.owl --ground_onto_file_path ground_software.owl --save_file_path result.json 
```







