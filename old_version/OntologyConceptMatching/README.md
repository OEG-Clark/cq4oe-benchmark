# Ontology Matching: Concept & Property Evaluation

This repository provides comprehensive evaluation frameworks for assessing how well large language models (LLMs) can generate and match ontology concepts and properties against standard ontology definitions.

## Overview

The repository contains two complementary evaluation tasks:

1. **Ontology Concept Matching** - Evaluates concept/class name generation and alignment
2. **Ontology Property Matching** - Evaluates property (relationships) generation, characterization, and domain/range alignment

---

## Part 0: Baseline Ontology Generation

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

## Part 1: Ontology Concept Matching

### Overview

The Ontology Property Matching task evaluates how well LLMs can generate and correctly characterize ontology properties (object properties and datatype properties), including their types, domains, ranges, and functional characteristics. This extends the concept matching evaluation to relationship-level semantics.

### Execution

1. Install [ollama](https://ollama.com/) with corresponding models and start the service
2. Install dependencies: `pip install -r requirements.txt`
3. Run the following command in the `code` folder:

```bash
python eval.py --model_id embeddinggemma,nomic-embed-text --generate_onto_file_path generated_software.owl --ground_onto_file_path ground_software.owl --save_file_folder ../data/odrl/
```

**Evaluation Script Arguments:**

| Argument | Description | Example | Required |
|----------|-------------|---------|----------|
| `--model_id` | Comma-separated list of embedding models to use for semantic evaluation (used by Ollama) | `embeddinggemma` | Yes |
| `--generate_onto_file_path` | Path to the generated ontology OWL/RDF file to be evaluated | `generated_software.owl` | Yes |
| `--ground_onto_file_path` | Path to the ground truth/reference ontology OWL/RDF file | `ground_software.owl` | Yes |
| `--save_file_folder` | Path where evaluation results and analysis report in json format will be saved | `result.json` | Yes |
| `--redundancy_folder` | Path where redundancy evaluation results in TXT format will be saved | `Redundancy_cosine_results.txt` | No |

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

**Report Format:**

The evaluation reports are saved as JSON with the following strucutre:

```json
{
  "hard_match": [
    {
      "Gold Concept": "schema:organization",
      "Exact Match": "yes",
      "Best Candidate Match": "organization",
      "Similarity": 1.0
    },
    {
      "Gold Concept": "constraint",
      "Exact Match": "yes",
      "Best Candidate Match": "constraint",
      "Similarity": 1.0
    },
    ...
  ],
  "sequence_match": [...],
  "levenshtein": [...],
  "jaro_winkler": [...],
  "semantic_embeddinggemma": [...]
}
```

| Field | Description |
|-------|-------------|
| `Gold Concept` | The reference concept/property from the ground truth ontology |
| `Exact Match` | Whether an exact string match was found ("yes" or "") |
| `Best Candidate Match` | The closest matching element from the generated ontology |
| `Similarity` | Numerical similarity score (0.0 to 1.0) based on the matching method |

**Matching Methods in Report:**

- **hard_match**: Exact lexical string comparison
- **sequence_match**: Token-level similarity (robust to reordering)
- **levenshtein**: Character-level edit distance
- **jaro_winkler**: String similarity emphasizing common prefixes
- **semantic_[model]**: Dense vector representation using embedding models (e.g., embeddinggemma, nomic-embed-text)

### Evaluation for Concepts/Classes

#### Evaluation Metrics

To evaluate the models' ability to **recognize**, **name**, and **align** ontology concepts accurately, we employ quantitative metrics that jointly measure the **correctness**, **completeness**, and **consistency** of model outputs with respect to the original ontology.

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **Precision** | TP / (TP + FP) | Higher precision indicates fewer false predictions when identifying ontology classes. The model correctly identifies only the relevant concepts. |
| **Recall** | TP / (TP + FN) | Higher recall means the model retrieves a larger portion of gold ontology concepts, reflecting better coverage of true classes. |
| **F1-score** | 2 × (Precision × Recall) / (Precision + Recall) | Harmonic mean of precision and recall. A higher F1-score indicates the model maintains both high precision and recall in recognizing ontology concepts. |
| **Accuracy** | Correct predictions / Total predictions | Higher accuracy reflects consistent alignment of predicted ontology concepts with the gold ontology. Overall proportion of correctly classified concepts. |
| **Coverage Rate** | Matched gold classes / Total gold classes | Higher coverage rate indicates the model produces accurate labels and covers a broader range of ontology concepts comprehensively. |

#### Evaluation Methods (Computation Techniques for Evaluation Metrics)

The table below summarizes the different techniques used to compute evaluation metrics by comparing generated ontology labels with reference ontologies:

| Method | Reference Name | Method | Application | Characteristics |
|-----------|--------|--------|-------------|-----------------|
| **Hard Match Ratio** | hard_match | Exact lexical string comparison | Evaluates if generated labels exactly match reference labels | Strict string-level comparison; identical labels only count as correct matches; no semantic similarity considered |
| **Information Content** | --- | Semantic-level comparison using WordNet synsets and IC scores | Maps labels to WordNet synsets and retrieves precomputed IC values; uses similarity measures (Resnik, Lin, Jiang-Conrath) | Measures semantic specificity; handles compound terms by decomposing into sub-concepts; **currently excluded from experiments** due to indexing errors with non-WordNet vocabulary |
| **Sequence Match Ratio** | sequence_match | Token-level similarity using Python difflib SequenceMatcher | Captures partially matching or reordered expressions (e.g., "wine region" vs. "region of wine") | Soft-matching approach; TP defined as sum of maximal similarity scores; robust to token reordering |
| **Levenshtein Distance** | levenshtein | Character-level edit distance approximation | Measures minimum operations (insertions, deletions, substitutions) to transform one label into another | Soft-matching approach; captures spelling-level closeness; robust to minor typographical or morphological variations |
| **Jaro–Winkler Distance** | jaro_winkler | String similarity metric emphasizing common prefixes | Evaluates both number and order of matching characters; score range [0,1] | Particularly effective for labels sharing morphological roots or hierarchical naming patterns (e.g., "wineRegion" vs. "wineType") |
| **Synonyms** | synonym | Exact match against WordNet synonym relations | Counts prediction as TP if it matches gold label or one of its WordNet synonyms | Hard matching approach; identifies semantically equivalent concepts expressed through different lexical forms |
| **Semantic Cosine Similarity** | semantic_**model-id** | Dense vector representation using pretrained language models (BERT, RoBERTa, Sentence-BERT) | Each label represented as embedding vector; similarity computed as cosine of angle between vectors | Soft-matching approach; captures meaning-level correspondence even with few/no common tokens (e.g., "human" vs. "person"); TP computed as sum of maximal similarity scores |

---

## Part 2: Ontology Property Matching

### Overview

The Ontology Property Matching task evaluates how well LLMs can generate and correctly characterize ontology properties (object properties and datatype properties), including their types, domains, ranges, and functional characteristics. This extends the concept matching evaluation to relationship-level semantics.

### Task Components

Property matching evaluation consists of five sub-tasks:

1. **Property Names** - Matching generated property names against reference properties
2. **Property Domains** - Evaluating domain class associations for each property
3. **Property Ranges** - Evaluating range class/datatype associations for each property
4. **Property Types** - Assessing correct type classification (ObjectProperty vs DatatypeProperty)
5. **Property Functions** - Detecting functional characteristics and potential conflicts

### Execution

1. Install [ollama](https://ollama.com/) with corresponding embedding models and start the service
2. Install dependencies: `pip install -r requirements.txt`
3. Run the following command in the `code` folder:

```bash
python eval_property.py --model_id embeddinggemma,nomic-embed-text --generate_onto_file_path generated_software.owl --ground_onto_file_path ground_software.owl --save_file_name results_base
```

**Evaluation Script Arguments:**

| Argument | Description | Example | Required |
|----------|-------------|---------|----------|
| `--model_id` | Comma-separated list of embedding models for semantic evaluation (Ollama) | `embeddinggemma` | Yes |
| `--generate_onto_file_path` | Path to the generated ontology OWL/RDF file to be evaluated | `generated_software.owl` | Yes |
| `--ground_onto_file_path` | Path to the ground truth/reference ontology OWL/RDF file | `ground_software.owl` | Yes |
| `--save_file_name` | Base path where evaluation results will be saved (suffixes will be added) | `results_base` | Yes |

**Output Format:**

The evaluation produces multiple JSON files, each containing evaluation results across different matching methods:

```bash
results_base_properties.json        # Property names evaluation
results_base_domains.json           # Property domains evaluation
results_base_ranges.json            # Property ranges evaluation
results_base_property_type.json     # Property type classification metrics
results_base_property_function.json # Property functional characteristic metrics
```

**Sample Output Structure:**

```json
{
  "hard_match": {
    "coverage_rate": 0.82,
    "precision": 0.88,
    "recall": 0.78,
    "accuracy": 0.85,
    "f1": 0.83
  },
  "sequence_match": { ... },
  "levenshtein": { ... },
  "jaro_winkler": { ... },
  "semantic_embeddinggemma": { ... },
  "semantic_nomic-embed-text": { ... }
}
```

For property type and function evaluations:

```json
{
  "accuracy": 0.92,
  "precision": 0.90,
  "recall": 0.94,
  "f1": 0.92
}
```

**Report Format:**

The evaluation reports are saved as JSON with the following strucutre:

```json
{
  "hard_match": [
    {
      "Gold Concept": "schema:organization",
      "Exact Match": "yes",
      "Best Candidate Match": "organization",
      "Similarity": 1.0
    },
    {
      "Gold Concept": "constraint",
      "Exact Match": "yes",
      "Best Candidate Match": "constraint",
      "Similarity": 1.0
    },
    ...
  ],
  "sequence_match": [...],
  "levenshtein": [...],
  "jaro_winkler": [...],
  "semantic_embeddinggemma": [...]
}
```

| Field | Description |
|-------|-------------|
| `Gold Concept` | The reference concept/property from the ground truth ontology |
| `Exact Match` | Whether an exact string match was found ("yes" or "") |
| `Best Candidate Match` | The closest matching element from the generated ontology |
| `Similarity` | Numerical similarity score (0.0 to 1.0) based on the matching method |


### Evaluation for Properties

The property matching evaluation employs the same string similarity metrics as concept matching, applied at different granularities:

- **Property Names**: Direct comparison of property identifiers
- **Property Domains**: Comparison of domain class labels (supporting union types)
- **Property Ranges**: Comparison of range class/datatype labels (supporting union types)
- **Property Type Matching**: Binary classification of ObjectProperty vs DatatypeProperty
- **Property Function Conflict Detection**: Identifies conflicts between incompatible property characteristics (e.g., Symmetric + Asymmetric)

All string matching methods are applied consistently:

| Method | Application to Properties |
|--------|--------------------------|
| **Hard Match** | Exact string matching for property names, domains, and ranges |
| **Sequence Match** | Token-level matching robust to reordering |
| **Levenshtein** | Character-level edit distance for typo tolerance |
| **Jaro–Winkler** | Effective for properties with morphological similarities |
| **Semantic Similarity** | Dense vector matching for meaning-level alignment, especially useful for synonym-like property names |

### Property Extraction Details

The evaluation script automatically extracts:

- **Property Names**: All ObjectProperty and DatatypeProperty URIs with their labels
- **Property Types**: Classification as ObjectProperty or DatatypeProperty
- **Domain/Range**: Complete domain and range specifications, including handling of union types through owl:unionOf
- **Hierarchies**: Parent property relationships via rdfs:subPropertyOf
- **Functional Characteristics**: All OWL property type annotations

---

## Integration and Workflow

### Complete Evaluation Pipeline

```bash
# 1. Generate ontology from competency questions
python generation.py --user_key YOUR_API_KEY --model_id gemini-2.5-pro \
  --input_file_path cqs.json --save_file_path generated_ontology.owl

# 2. Evaluate concept matching
python eval.py --model_id embeddinggemma,nomic-embed-text \
  --generate_onto_file_path generated_ontology.owl \
  --ground_onto_file_path ground_ontology.owl \
  --save_file_path concept_results.json

# 3. Evaluate property matching
python eval_property.py --model_id embeddinggemma,nomic-embed-text \
  --generate_onto_file_path generated_ontology.owl \
  --ground_onto_file_path ground_ontology.owl \
  --save_file_name property_results
```
