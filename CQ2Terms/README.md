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

### Evaluation metrics
TBD: Clark to clarify
- We do cosim similarity per term. 
- We average the similarities obtained.
- In case there are more than 3 terms, we BLA BLA.


### Results
TBD: 

- Generation Model and Output:
    >[LLAMA-70B](https://huggingface.co/TheBloke/Llama-2-70B-GGML): Player, friend, game

    >[GPT-4](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent): Friends, play, games; Player, play, games

