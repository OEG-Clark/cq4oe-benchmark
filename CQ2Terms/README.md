# CQ2Terms


### Task Definition

Given a set of Competency Questions (CQs) as the input, the task is to generate the terms that is needed for the ontology. Usually, the terms for each CQ are constructed as a triple indicating a subject, predicate and object. No external context is expected, and hence the CQs must be self-explanatory. For example, if a CQ is "Which players play with whom?" the range of the property is assumed to be player.

Datatypes are represented as primitive types. For example, if CQ is "What is the name of a person?", the ground truth is "Person, name, string."

The goal of this task is to identify whether the model is able to identify the terms (classes and properties) implied in a CQ. A CQ may contain more than 3 terms.

### Dataset
We use the following ontologies in our dataset:

- [Mint Ontology](https://w3id.org/okn/o/sdm): Based on the requirements gathered in Model Catalog Requirements spreadsheet and Mapping Files to Model Variables
- [VideoGame Ontology](http://vocab.linkeddata.es/vgo/): The Video Game Ontology is aimed at modelling video game related information.
- [Software Ontology](https://www.ebi.ac.uk/ols4/ontologies/swo): SWO ontology describes software tools, their types, tasks, versions, licensing, provenance and associated data.

In total, we have <TO DO> competency questions.
  
### Examples and Temp Result
The input to the model must be a competency question. For example: 

```
- Input: Are there any direct dependencies to other scripts in this configuration?
```
The ground truth is validated by the domain expert in a string format. For example: 

```
- ground truth: Model Configuration, contains, Script; Script, has dependency, direct dependency
```

The output is a set of terms, identified in the competency question. These terms are not validated against a final ontology for now (the ontology may have terms that are semantically similar, but adopt other patterns). Example output:
> **_NOTE:_** [generation model id](https://deepmind.google/technologies/gemini/)
```json
"subject": "Configuration",
"predicate": "hasDependency",
"object": "Scripts"
```

### Evaluation

#### Evaluation Metric Definition

We adopt two types of evaluation process, `string_embedding_cosine_similarity` and `triple_embedding_cosine_similarity`

`string_embedding_cosine_similarity`: The evaluation process takes the scope of the entire generation as well as ground_truth.

`triple_embedding_cosine_similarity`: The evaluation process takes a finer scope than `string_embedding_cosine_similarity`, it evaluate each term in generation with the term in the ground_truth.

#### Detailed Evalution Process

`string_embedding_cosine_similarity`:
- We adopt the model from [Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) based on the STS Task to calculate the similarity between generated triples and ground truth.
- We applied the model to the entire ground_truth and generation in result
- We average the similarities obtained to access the performance of LLM.

`triple_embedding_cosine_similarity`:
- We adopt the model from [Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) based on the STS Task to calculate the similarity between each generate term and corresponding term in the ground truth.
- We apply the similarity to each term pair (ground_truth_term, generation_term) 
- In case of the number of generated terms and ground truth mismatched, we take the minimal number of generation and ground truth as the number of term we evaluate.
- We set the threathold as 0.85 for correct generation, as indicated as restrict_evalation_value, which 1 indicate correct generation and 0 indicate miss generation
- Then calculate the overall accuracy as the restrict_evalation



### Results

The JSON format of output contains the following:

| Field    | Definition | Example |
| -------- | ------- | ------ |
| generation model id  | The reference id for the generation model  | gemini-2.0-flash |
| embedding model id | The reference id for the embedding model | mxbai-embed-large |
| result    | Generation and Evaluation result per competency question    | Given Below |

The JSON format of the `result` part of the output file

| Field    | Definition | Example | DataType |
| -------- | ------- | ------ | ------ |
| ID  | The reference id for the CQ  | MINT_CQ1 | String |
| examples | The few-shot examples | Given Below | String |
| generation | The generated triple | subject: model, predicate: hasVersion, object: VersionNumber | Dictionary |
| string_embedding_cosine_similarity | The `string_embedding_cosine_similarity` evalution value | 0.9249703288078308 | Float |
| triple_embedding_cosine_similarity | The `triple_embedding_cosine_similarity` evalution value | [1.0, 1.0, 0.4874] | List of Float |

An Example of the Few-Shot Example:
> **_NOTE:_** The few-shot example is not from the ontology that is for LLM's inference
```json
competency question: What are the export options for this tool?
semantic triples: Tool, hasExportOptions, string
competency question: Does this tool render a gif?
semantic triples: Tool, renders, GIF
...
```

