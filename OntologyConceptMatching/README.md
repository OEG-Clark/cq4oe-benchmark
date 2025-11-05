# Ontology Concept Matching

The Ontology Concept Label Matching task evaluates how well large language models (LLMs) can generate concept names that correctly correspond to the standard class labels defined in ontology.

## Baseline

### Ontology Generation

To generate ontologies using LLM models based on competency questions:

1. Prepare a JSON file containing competency questions (CQs)
2. Install dependencies: `pip install -r requirements.txt`
3. Run the generation script:

```bash
python generation.py --user_key YOUR_API_KEY --model_id gemini-2.5-pro --input_file_path cqs.json --save_file_path generated_ontology.owl
```

**Generation Script Arguments:**

| Argument | Description | Default |
|----------|-------------|---------|
| `--user_key` | API key for the LLM provider (e.g., Gemini, OpenAI) | `xxx` |
| `--model_id` | Model identifier (e.g., gemini-2.5-pro, gpt-4) | `gemini-2.5-pro` |
| `--input_file_path` | Path to JSON file containing competency questions | Required |
| `--save_file_path` | Path where the generated OWL ontology will be saved | Required |

**How it works:**

- Loads competency questions from the JSON input file
- Sends queries to the specified LLM model with instructions to generate OWL format ontologies
- Validates the generated output against OWL/RDF-XML format
- Converts and serializes the output to a valid OWL file
- Saves the final ontology to the specified location


## Evaluation

### Evaluation Metric

To evaluate the models' ability to **recognize**, **name**, and **align** ontology concepts accurately, we employ quantitative metrics that jointly measure the **correctness**, **completeness**, and **consistency** of model outputs with respect to the original ontology.


| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **Precision** | TP / (TP + FP) | Higher precision indicates fewer false predictions when identifying ontology classes. The model correctly identifies only the relevant concepts. |
| **Recall** | TP / (TP + FN) | Higher recall means the model retrieves a larger portion of gold ontology concepts, reflecting better coverage of true classes. |
| **F1-score** | 2 × (Precision × Recall) / (Precision + Recall) | Harmonic mean of precision and recall. A higher F1-score indicates the model maintains both high precision and recall in recognizing ontology concepts. |
| **Accuracy** | Correct predictions / Total predictions | Higher accuracy reflects consistent alignment of predicted ontology concepts with the gold ontology. Overall proportion of correctly classified concepts. |
| **Coverage Rate** | Matched gold classes / Total gold classes | Higher coverage rate indicates the model produces accurate labels and covers a broader range of ontology concepts comprehensively. |
---

### Evaluation Methods (Computation Techniques for Evaluation Metrics)

The table below summarizes the different techniques used to compute evaluation metrics by comparing generated ontology labels with reference ontologies:

| Method | Reference Name | Method | Application | Characteristics |
|-----------|--------|--------|-------------|-----------------|
| **Hard Match Ratio** | hard_match | Exact lexical string comparison | Evaluates if generated labels exactly match reference labels | Strict string-level comparison; identical labels only count as correct matches; no semantic similarity considered |
| **Information Content** | --- | Semantic-level comparison using WordNet synsets and IC scores | Maps labels to WordNet synsets and retrieves precomputed IC values; uses similarity measures (Resnik, Lin, Jiang-Conrath) | Measures semantic specificity; handles compound terms by decomposing into sub-concepts; **currently excluded from experiments** due to indexing errors with non-WordNet vocabulary |
| **Sequence Match Ratio** | sequence_match | Token-level similarity using Python difflib SequenceMatcher | Captures partially matching or reordered expressions (e.g., "wine region" vs. "region of wine") | Soft-matching approach; TP defined as sum of maximal similarity scores; robust to token reordering |
| **Levenshtein Distance** | levenshtein | Character-level edit distance approximation | Measures minimum operations (insertions, deletions, substitutions) to transform one label into another | Soft-matching approach; captures spelling-level closeness; robust to minor typographical or morphological variations |
| **Jaro–Winkler Distance** | jaro_winkler |String similarity metric emphasizing common prefixes | Evaluates both number and order of matching characters; score range [0,1] | Particularly effective for labels sharing morphological roots or hierarchical naming patterns (e.g., "wineRegion" vs. "wineType") |
| **Synonyms** | synonym | Exact match against WordNet synonym relations | Counts prediction as TP if it matches gold label or one of its WordNet synonyms | Hard matching approach; identifies semantically equivalent concepts expressed through different lexical forms |
| **Semantic Cosine Similarity** | sementic_**model-id** | Dense vector representation using pretrained language models (BERT, RoBERTa, Sentence-BERT) | Each label represented as embedding vector; similarity computed as cosine of angle between vectors | Soft-matching approach; captures meaning-level correspondence even with few/no common tokens (e.g., "human" vs. "person"); TP computed as sum of maximal similarity scores |


### Execution

1. install [ollama](https://ollama.com/) with correspond models and start the service
2. Install dependencies: `pip install -r requirements.txt`
3. run the following command line in the `code` folder
```bash
python eval.py --model_id embeddinggemma,nomic-embed-text --generate_onto_file_path generated_software.owl --ground_onto_file_path ground_software.owl --save_file_path result.json 
```

**Evaluation Script Arguments:**

| Argument | Description | Example | Required |
|----------|-------------|---------|----------|
| `--model_id` | Comma-separated list of embedding models to use for semantic evaluation (used by Ollama) | `embeddinggemma` | Yes |
| `--generate_onto_file_path` | Path to the generated ontology OWL/RDF file to be evaluated | `generated_software.owl` | Yes |
| `--ground_onto_file_path` | Path to the ground truth/reference ontology OWL/RDF file | `ground_software.owl` | Yes |
| `--save_file_path` | Path where evaluation results in JSON format will be saved | `result.json` | Yes |
| `--redundancy_folder` | Path where redundancy evaluation results in TXT format will be saved | `Redundancy_cosine_results.txt` | Yes |

**Output Format:**

The evaluation results are saved as JSON with the following structure:

```json
{
  "hard_match": {
    "coverage_rate": 0.85,
    "precision": 0.90,
    "recall": 0.80,
    "accuracy": 0.88,
    "f1": 0.85
  },
  "sequence_match": { ... },
  "levenshtein": { ... },
  "jaro_winkler": { ... },
  "semantic_embeddinggemma": { ... },
  "semantic_nomic-embed-text": { ... },
  "synonym": { ... }
}
```

Each method generates its own set of metrics, allowing comprehensive evaluation across multiple matching strategies.

