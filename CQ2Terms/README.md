# CQ2Terms


### Task Definition

Given a set of Competency Questions (CQs) as the input, the task is to generate the terms that is needed for the ontology. Usually, the terms for each CQ are constructed as a triple indicating a subject, predicate and object. No external context is expected, and hence the CQs must be self-explanatory. For example, if a CQ is "Which players play with whom?" the range of the property is assumed to be player.

Datatypes are represented as primitive types. For example "What is the name of a person?" will have as ground truth: Person, name, string.

The goal of this task is to identify whether the model is able identify the terms (classes and properties) implied in a CQ. A CQ may contain more than 3 terms.

### Dataset
We use the following ontologies in our dataset:

- [Mint Ontology](https://w3id.org/okn/o/sdm): Based on the requirements gathered in Model Catalog Requirements spreadsheet and Mapping Files to Model Variables
- [VideoGame Ontology](http://vocab.linkeddata.es/vgo/): The Video Game Ontology is aimed at modelling video game related information.
- [Software Ontology](https://www.ebi.ac.uk/ols4/ontologies/swo): SWO ontology describes software tools, their types, tasks, versions, licensing, provenance and associated data.

In total, we have <TO DO> competency questions.
  
### Examples and Temp Result
The input to the model must be a competency question. For example: 

```
- Input: Who are the friends that play other games as well with this player?
```

The output is a set of terms, identified in the competency question. These terms are not validated against a final ontology for now (the ontology may have terms that are semantically similar, but adopt other patterns). Example output:

```
- Output: Player, is friend with player, Player; Player, plays game, Game
```

### Evaluation Process

We adopt two types of evaluation process, `triple_semantic_similarity` and `restrict_evalation`

`triple_semantic_similarity`: The evaluation process takes the scope of the entire generation as well as ground_truth.

`restrict_evalation`: The evaluation process takes a finer scope than `triple_semantic_similarity`, it evaluate each term in generation with the term in the ground_truth.


triple_semantic_similarity:
- We adopt the model from [Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) based on the STS Task to calculate the similarity between generated triples and ground truth.
- We applied the model to the entire ground_truth and generation in result
- We average the similarities obtained to access the performance of LLM.

restrict_evalation:
- We adopt the model from [Massive Text Embedding Benchmark](https://huggingface.co/spaces/mteb/leaderboard) based on the STS Task to calculate the similarity between each generate term and corresponding term in the ground truth.
- We apply the similarity to each term pair (ground_truth_term, generation_term) 
- In case of the number of generated terms and ground truth mismatched, we take the minimal number of generation and ground truth as the number of term we evaluate.
- We set the threathold as 0.85 for correct generation, as indicated as restrict_evalation_value, which 1 indicate correct generation and 0 indicate miss generation
- Then calculate the overall accuracy as the restrict_evalation



### Results

The JSON format of output contains the following:

| Field    | Definition | Example |
| -------- | ------- | ------ |
| llm_model_id  | The reference id (perferably huggingface) for the generation model  | meta-llama/Meta-Llama-3-8B-Instruct |
| evalation_model_id | The reference id (perferably huggingface) for the evaluation model | Salesforce/SFR-Embedding-Mistral |
| promtp_template    | The prompt defined for the task |  |
| result    | Generation and Evaluation result per competency question    | |
| triple_semantic_similarity    | The overall semantic textual similairty value based on evaluation model(Avgerage)  | 0.9138303279876709 | 
| restrict_evalation    | The restircted overall semantic textual similairty value based on evaluation model(Avgerage)  | 0.6666666666666666 | 

Example for prompt_template:

```json
{ 
    "role": "system",
    "content": "Please only generate the terms based on the competency question from an ontology perspective."
}
{
    "role": "user",
    "content": "How many experiments are reported per year?"
}
{
    "role": "assistant",
    "content": "Experiment, reportedIn, Report; Report, reportDate, Year; Year, hasCount, Count"
}
...few shot...
{
    "role": "user",
    "content": "To be processed CQ"
}
```

The JSON format for result:

| Field    | Definition | Data Type | Example | 
| -------- | ------- | ------ | ------ |
| CQ_id  | Reference ID for the competency question  | str | MINT_CQ3 |
| CQ | Actual competency question  | str | 'What are the inputs to a model?' |
| ground_truth  | The actual terms for the competency question    | str | 'Model, has input, Input' |
| generation    | The generated terms for the competency question    | str | 'ModelConfiguration, hasInput, DataEntity' |
| eval_sim    | The similiarity between the embedding of the ground_truth and the generation calculated as cosine_similarity  | float | 0.8849964737892151 |
| restrict_evalation_value  | Evaluation per term    | list of int | [1, 1, 0] |
| ground_truth_list | The actual terms in the format of list    | list of str | ['model', 'has input', 'input'] |
| generation_list | The generated terms in the format of list    | list of str | ['modelconfiguration', 'hasinput', 'dataentity'] |



### Example Output

CQ: What is the version number of the model?

Ground Truth: Model, hasVersion, string

- Generation Model and Output:
    >[LLAMA3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B): ModelConfiguration, hasVersion, str

