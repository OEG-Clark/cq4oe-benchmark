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


## Annotation Guideline

1. How to annotated
2. Example of annotation
3. Dataset description


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