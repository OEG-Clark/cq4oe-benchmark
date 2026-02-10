
# Ontology: videogame
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.568114 |      0.459857 |       0.730086 |                  0.688429 |                    0.652171 | 0.0283688 |
|  0 | neon-deepseek-reasoner |     0.142857 |         0.588629 |      0.473571 |       0.738857 |                  0.700714 |  0.035461 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.307692 |         0.870692 |      0.798442 |       0.917621 |                   0.95509 |                    0.943379 |  0.307692 |
|  0 | neon-deepseek-reasoner |     0.384615 |         0.895506 |      0.841798 |       0.937772 |                  0.945014 |  0.384615 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.568114 |      0.459857 |       0.730086 |                  0.688429 |                    0.652171 |  0.114286 |
|  0 | neon-deepseek-reasoner |     0.142857 |         0.588629 |      0.473571 |       0.738857 |                  0.700714 |  0.142857 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0909091 |         0.568114 |      0.459857 |       0.730086 |                  0.688429 |                    0.652171 |  0.733333 |
|  0 | neon-deepseek-reasoner |     0.116279 |         0.588629 |      0.473571 |       0.738857 |                  0.700714 |  0.744966 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.166667 |         0.687588 |      0.583596 |       0.813181 |                  0.800126 |                    0.771201 |  0.166667 |
|  0 | neon-deepseek-reasoner |     0.208333 |          0.71034 |      0.606144 |       0.826515 |                  0.804732 |  0.208333 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.630219 |      0.504313 |       0.764625 |                   0.70475 |                    0.620687 |
|  0 | neon-deepseek-reasoner |      0.03125 |          0.64725 |      0.544062 |       0.774406 |                  0.707937 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.769939 |      0.658318 |       0.860882 |                  0.846705 |                    0.762691 |
|  0 | neon-deepseek-reasoner |      0.03125 |           0.8183 |      0.696372 |       0.902046 |                  0.899218 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.630219 |      0.504313 |       0.764625 |                   0.70475 |                    0.620687 |
|  0 | neon-deepseek-reasoner |      0.03125 |          0.64725 |      0.544063 |       0.774406 |                  0.707937 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.630219 |      0.504313 |       0.764625 |                   0.70475 |                    0.620687 |
|  0 | neon-deepseek-reasoner |     0.015873 |          0.64725 |      0.544062 |       0.774406 |                  0.707937 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.693107 |      0.571115 |       0.809904 |                  0.769233 |                    0.684401 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.722793 |      0.610866 |       0.833367 |                  0.792195 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.802344 |      0.726563 |       0.893625 |                  0.783219 |                       0.837 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.809938 |      0.737344 |       0.897594 |                  0.774781 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.93184 |      0.864152 |       0.934876 |                  0.882935 |                    0.925725 |
|  0 | neon-deepseek-reasoner |      0.03125 |          0.91677 |      0.892364 |       0.947547 |                  0.905747 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.802344 |      0.726563 |       0.893625 |                  0.783219 |                       0.837 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.809937 |      0.737344 |       0.897594 |                  0.774781 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.802344 |      0.726563 |       0.893625 |                  0.783219 |                       0.837 |
|  0 | neon-deepseek-reasoner |     0.015873 |         0.809938 |      0.737344 |       0.897594 |                  0.774781 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.862257 |      0.789407 |       0.913785 |                  0.830093 |                     0.87913 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.860049 |      0.807481 |       0.921894 |                  0.835161 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.808531 |      0.727844 |       0.892781 |                  0.763594 |                    0.861469 |
|  0 | neon-deepseek-reasoner |            0 |         0.811375 |      0.735531 |       0.898188 |                  0.778156 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.926883 |      0.876458 |       0.941163 |                  0.881843 |                    0.938931 |
|  0 | neon-deepseek-reasoner |            0 |         0.949636 |      0.889195 |       0.965988 |                  0.910657 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.808531 |      0.727844 |       0.892781 |                  0.763594 |                    0.861469 |
|  0 | neon-deepseek-reasoner |            0 |         0.811375 |      0.735531 |       0.898188 |                  0.778156 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.808531 |      0.727844 |       0.892781 |                  0.763594 |                    0.861469 |
|  0 | neon-deepseek-reasoner |            0 |         0.811375 |      0.735531 |       0.898188 |                  0.778156 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.863671 |      0.795268 |       0.916334 |                   0.81847 |                    0.898533 |
|  0 | neon-deepseek-reasoner |            0 |         0.875078 |      0.805097 |       0.930855 |                  0.839209 |
    
    