
# Ontology: videogame
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.568114 |      0.459857 |       0.730086 |                  0.688429 |                    0.652171 | 0.0283688 |
|  0 | neon-deepseek-reasoner |     0.142857 |         0.575886 |      0.462686 |          0.738 |                    0.6916 |  0.035461 |
|  0 | deepseek-reasoner |     0.142857 |         0.576829 |      0.467457 |       0.731743 |                    0.6914 |  0.035461 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.307692 |         0.870692 |      0.798442 |       0.917621 |                   0.95509 |                    0.943379 |  0.307692 |
|  0 | neon-deepseek-reasoner |     0.416667 |         0.896739 |       0.80877 |       0.936888 |                  0.933765 |  0.416667 |
|  0 | deepseek-reasoner |     0.416667 |         0.923982 |      0.889717 |        0.93882 |                  0.932452 |  0.416667 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.568114 |      0.459857 |       0.730086 |                  0.688429 |                    0.652171 |  0.114286 |
|  0 | neon-deepseek-reasoner |     0.142857 |         0.575886 |      0.462686 |          0.738 |                    0.6916 |  0.142857 |
|  0 | deepseek-reasoner |     0.142857 |         0.576829 |      0.467457 |       0.731743 |                    0.6914 |  0.142857 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0909091 |         0.568114 |      0.459857 |       0.730086 |                  0.688429 |                    0.652171 |  0.733333 |
|  0 | neon-deepseek-reasoner |     0.119048 |         0.575886 |      0.462686 |          0.738 |                    0.6916 |      0.75 |
|  0 | deepseek-reasoner |     0.119048 |         0.576829 |      0.467457 |       0.731743 |                    0.6914 |      0.75 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.166667 |         0.687588 |      0.583596 |       0.813181 |                  0.800126 |                    0.771201 |  0.166667 |
|  0 | neon-deepseek-reasoner |     0.212766 |         0.701359 |      0.588627 |       0.825635 |                  0.794642 |  0.212766 |
|  0 | deepseek-reasoner |     0.212766 |         0.710255 |      0.612898 |       0.822447 |                  0.794035 |  0.212766 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.630219 |      0.504313 |       0.764625 |                   0.70475 |                    0.620687 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.626594 |      0.528719 |        0.77175 |                  0.706844 |
|  0 | deepseek-reasoner |            0 |         0.625062 |      0.518406 |       0.751969 |                  0.700562 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.769939 |      0.658318 |       0.860882 |                  0.846705 |                    0.762691 |
|  0 | neon-deepseek-reasoner |    0.0357143 |         0.850881 |       0.75979 |       0.924701 |                  0.894385 |
|  0 | deepseek-reasoner |            0 |         0.792818 |      0.692189 |       0.902114 |                  0.859026 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.630219 |      0.504313 |       0.764625 |                   0.70475 |                    0.620687 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.626594 |      0.528719 |        0.77175 |                  0.706844 |
|  0 | deepseek-reasoner |            0 |         0.625063 |      0.518406 |       0.751969 |                  0.700562 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.630219 |      0.504313 |       0.764625 |                   0.70475 |                    0.620687 |
|  0 | neon-deepseek-reasoner |    0.0169492 |         0.626594 |      0.528719 |        0.77175 |                  0.706844 |
|  0 | deepseek-reasoner |            0 |         0.625062 |      0.518406 |       0.751969 |                  0.700562 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.693107 |      0.571115 |       0.809904 |                  0.769233 |                    0.684401 |
|  0 | neon-deepseek-reasoner |    0.0333333 |         0.721713 |      0.623535 |       0.841331 |                  0.789632 |
|  0 | deepseek-reasoner |            0 |         0.699016 |      0.592824 |       0.820227 |                  0.771744 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.802344 |      0.726563 |       0.893625 |                  0.783219 |                       0.837 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.803375 |      0.729656 |       0.895375 |                  0.772469 |
|  0 | deepseek-reasoner |            0 |           0.7935 |      0.720438 |       0.892062 |                  0.761656 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.93184 |      0.864152 |       0.934876 |                  0.882935 |                    0.925725 |
|  0 | neon-deepseek-reasoner |    0.0357143 |         0.917651 |      0.893571 |       0.952147 |                  0.901134 |
|  0 | deepseek-reasoner |            0 |         0.946862 |       0.89015 |       0.944356 |                  0.895934 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.802344 |      0.726563 |       0.893625 |                  0.783219 |                       0.837 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.803375 |      0.729656 |       0.895375 |                  0.772469 |
|  0 | deepseek-reasoner |            0 |           0.7935 |      0.720438 |       0.892062 |                  0.761656 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.802344 |      0.726563 |       0.893625 |                  0.783219 |                       0.837 |
|  0 | neon-deepseek-reasoner |    0.0169492 |         0.803375 |      0.729656 |       0.895375 |                  0.772469 |
|  0 | deepseek-reasoner |            0 |           0.7935 |      0.720438 |       0.892062 |                  0.761656 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.862257 |      0.789407 |       0.913785 |                  0.830093 |                     0.87913 |
|  0 | neon-deepseek-reasoner |    0.0333333 |         0.856719 |      0.803337 |       0.922889 |                  0.831855 |
|  0 | deepseek-reasoner |            0 |         0.863424 |      0.796352 |       0.917465 |                  0.823357 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.808531 |      0.727844 |       0.892781 |                  0.763594 |                    0.861469 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.807531 |      0.739156 |       0.899219 |                  0.779375 |
|  0 | deepseek-reasoner |            0 |         0.818906 |      0.743969 |       0.901625 |                     0.774 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.926883 |      0.876458 |       0.941163 |                  0.881843 |                    0.938931 |
|  0 | neon-deepseek-reasoner |    0.0357143 |         0.934001 |      0.902235 |       0.963083 |                   0.92343 |
|  0 | deepseek-reasoner |            0 |         0.949594 |       0.89943 |       0.964337 |                  0.911694 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.808531 |      0.727844 |       0.892781 |                  0.763594 |                    0.861469 |
|  0 | neon-deepseek-reasoner |      0.03125 |         0.807531 |      0.739156 |       0.899219 |                  0.779375 |
|  0 | deepseek-reasoner |            0 |         0.818906 |      0.743969 |       0.901625 |                     0.774 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.808531 |      0.727844 |       0.892781 |                  0.763594 |                    0.861469 |
|  0 | neon-deepseek-reasoner |    0.0169492 |         0.807531 |      0.739156 |       0.899219 |                  0.779375 |
|  0 | deepseek-reasoner |            0 |         0.818906 |      0.743969 |       0.901625 |                     0.774 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.863671 |      0.795268 |       0.916334 |                   0.81847 |                    0.898533 |
|  0 | neon-deepseek-reasoner |    0.0333333 |         0.866174 |      0.812594 |       0.930056 |                  0.845309 |
|  0 | deepseek-reasoner |            0 |         0.879421 |      0.814346 |       0.931927 |                  0.837223 |
    
    