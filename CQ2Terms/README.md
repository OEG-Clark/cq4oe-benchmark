# CQ2Terms


### Task Definition

Given a set of requirements (CQ) as the input, the task is to generate the terms that is needed for the ontology. Commonly, the terms for each requirment are constructed as three terms. The evaluation process is yet to be defined. 

### Dataset

- [Mint Ontology](https://w3id.org/okn/o/sdm): Based on the requirements gathered in Model Catalog Requirements spreadsheet and Mapping Files to Model Variables
- [VideoGame Ontology](http://vocab.linkeddata.es/vgo/): The Video Game Ontology is aimed at modelling video game related information.
- [Software Ontology](https://www.ebi.ac.uk/ols4/ontologies/swo): SWO ontology describes software tools, their types, tasks, versions, licensing, provenance and associated data.
  
### Examples and Temp Result

- Input: Who are the friends that play other games as well with this player?
- Output: Player, is friend with player, Player; Player, plays game, Game
- Generation Model and Output:
    >[LLAMA-70B](https://huggingface.co/TheBloke/Llama-2-70B-GGML): Player, friend, game

    >[GPT-4](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent): Friends, play, games; Player, play, games

