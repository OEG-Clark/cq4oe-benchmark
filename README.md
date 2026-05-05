# CQ2Onto: A benchmark for assessing the LLM-assisted ontology generation from competency questions


This repository contains a benchmark for assessing the performance of different LLM-based ontology generation methods from competency questions. The benchmark is built on six domain experts annotated ontologies that are exact mirroring the corresponding competency questions. 

**CQ2Onto:** Given a set of competency questions in any domain, processing by LLM-based ontology generation method, producing a full OWL ontology.

**Annotated Ontologies**:
- [Wine](https://github.com/UCDavisLibrary/wine-ontology): Wine Ontology
- [VGO](https://vocab.linkeddata.es/vgo/): VideoGame Ontolgy
- [SWO](https://obofoundry.org/ontology/swo.html): Software Ontology
- [AWO](https://people.cs.uct.ac.za/~mkeet/OEbook/ontologies/AfricanWildlifeOntology1.owl): African wildlife Ontology
- [ODRL](https://www.w3.org/ns/odrl/2/): Open Digital Rights Language Ontology
- [Water](https://saref.etsi.org/saref4watr/v1.1.1/#clause-4-2-7): SAREF4WATR Ontolgy


## Annotation

The annotated ontologies in this benchmark are not just snapshots of existing ontologies. Every class, property and axiom is explicitly tied back to the competency questions. This section documents how that link was built so anyone adding a new domain can do the same thing.

### Annotation Guideline

For each source ontology, the annotation runs in three stages.

**1. Identify the core terms**: Before processing the competency question, domain experts extracts the conceptual backbone (key concepts and properties) from the source ontology by calculating the degree for each node as the relevance of the concept or property in the ontology. This can kept the backbone of the source ontology with maximum coverage.


**2. Annotated the CQs**: We annotated each CQ with two different terms. Exclude all CQs with external or out-of-the-scope concepts from the domain of the ontology. The two categories of the terms are:
- **Explicit:** terms that appear lexically in the CQ
- **Implicit:** terms expressed through synonymous phrasing
- **Missing Element**: terms are indicates in the CQ however do not mentioned in the ontology



**3. CQ Creation:** 
[Jiayi]
Due to the selection of the CQs after step 2, if there is any missing core concepts, domain experts create brand new CQs based on the missing core concepts.

**4. Axiom:**
[JiaYi]

**5. Annotating Ontology:**
[Jiayi]


Example of the annotation process
```
CQ: Which animals are the predators of [these animals]?
- Explicit Class: animal
- Explicit Property: eaten-by
- Implicit Class: Carnivore
- Implicit Property: None
- Missing Element: Predators is not in the ontology, however, carnivore indicates predators
```


### Dataset Description

We have selected six ontologies in three diferent scales:
| Ontology | Tier | Source CQs | Retained | New ⋆ | CQ2Onto set | CQ2Term set |
|----------|------|-----------:|---------:|------:|------------:|------------:|
| Wine     | small  | 7   | 4   | 1 | 5  | 5  |
| AWO      | small  | 14  | 7   | 0 | 7  | 7  |
| ODRL     | medium | 35  | 13  | 6 | 19 | 19 |
| Water    | medium | 43  | 21  | 0 | 21 | 20 |
| VGO      | large  | 68  | 30  | 1 | 31 | 22 |
| SWO      | large  | 88  | 35  | 0 | 35 | 26 |

## LLM-assiat ontology generation

### Generation Methods

This repository evaluates three different LLM-assiat ontology generation methods.

- **normal**: Give the model all the CQs and ask for the OWL ontology in one shot.
- [Cq-by-Cq Generation](https://github.com/LiUSemWeb/LLMs4OntologyDev-ESWC2024): generate a partial ontology per CQ and merge them. Slower but the model has to think about each question individually.
- [MASEO](https://github.com/oeg-upm/maseo): Multi-Agent System for Explainable Ontology Generation

### Baseline LLMs

- **Qwen-3.6 Series**: 
  - **Qwen-3.6-27B**: Open-source dense 27B parameter model
  - **Qwen-3.6-35B**: Open-source Mixture-of-Experts model, 35B total parameters with only 3B active per token
  - **Qwen-3.6-flash**: Closed-weights API-only low-latency model
  - **Qwen-3.6-plus**: Closed-weight API-only flagship model with 1M context window
- **Gemma-4 Series**:
  - **Gemma-4-26B**: Open-source Mixture-of-Experts model with 4B active per token
  - **Gemma-4-31B**: Open-source dense 31B parameter model 
- **Deepseek Series**:
  - **Deepseek-V3.2-671B**: The previous-generation flagship, Mixture-of-Experts  model from Deepseek.
  - **Deepseek-V4-flash-284B**: Efficient Mixture-of-Experts model with 13B activate parameter
  - **Deepseek-V4-1.6T**: Flagship Mixture-of-Experts model with 49B activate parameter, 1M context window.
  

### Prompts

The prompts that drive every model for each method is under `CQ2Onto/prompts/` and `CQ2Term/prompts/`. They are kept in plain JSON, one file per generation method. Every prompt file is a JSON array of *agent* objects. Each object has three fields:

```json
[
  {
    "agent": "the name of the LLM-based agent",
    "instruction": "the system message of the given agent",
    "prompt": "the user message designed for the task corresponding to the agent"
  }
]
```

## Evaluation

### The metric catalogue
 
`OntoCatalogue/` is the catalogue describing every metric used in this benchmark. Each metric has its own Turtle file under `KG/` and a matching HTML page under `html/`. The catalogue is browsable by opening `OntoCatalogue/html/catalog.html`. 

[idealy we have a web page]
 

### CQ2Onto Evaluation

For a given generated ontology, evaluation runs in stages, each producing its own evaluation file. The script `CQ2Onto/scripts/run_all_evaluation_agent_4datsets.py` runs the whole process across all three strategies and all six ontologies.

1. **Concept** (`CQ2Onto/../scripts/concept/eval_concept.py`):
   - Target: Evaluating if the generated ontology contains the correct classes and properties
   - Metrics:
2. **Property** (`scripts/property/eval_property.py`): characteristics, domains, ranges of object/data properties.
   - Target: Evaluating if the generated ontology contains the correct domains, ranges and object/data properties.
   - Metrics:
3. **Triple** (`scripts/triple/eval_triple.py`): RDF triples (asserted statements).
   - Target: Evaluating if the triples in the generated ontology is correct
   - Metrics:
4. **Axioms** (`scripts/axioms/eval_axioms.py`): 
   - Target: Atomic-level axioms evaluation against the gold standard ontology
   - Metrics:
5. **Hierarchy** (`scripts/hierarchy/eval_hierarchy.py`):
   - Target:
   - Metric


### CQ2Terms Evaluation

[JIayi]

## Execution

CQ-to-terms:
 
```
cd CQ2Term
python scripts/run_all_cq2term.py
```
 
CQ-to-ontology, all three strategies:
 
```
cd CQ2Onto
python scripts/run_all_evaluation_agent_4datsets.py
```
 
Both execution dive in the prediction folders, find the corresponding gold standard files, and write per-dataset and per-model evaluation results into `03_evaluation_results/` and `04_summary/`.


## Ackownledgement

