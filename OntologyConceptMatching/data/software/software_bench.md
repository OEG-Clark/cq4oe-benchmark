
# Ontology: software
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0254237 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 | 0.0151515 |
|  0 | neon-deepseek-reasoner |    0.0338983 |         0.481915 |      0.361941 |       0.676559 |                  0.683339 | 0.0189394 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |        0.125 |         0.875658 |      0.821837 |        0.94358 |                  0.961008 |                    0.932353 |     0.125 |
|  0 | neon-deepseek-reasoner |     0.166667 |         0.879367 |      0.815477 |       0.947697 |                  0.969578 |  0.166667 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0258621 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 | 0.0258621 |
|  0 | neon-deepseek-reasoner |    0.0344828 |         0.481915 |      0.361941 |       0.676559 |                  0.683339 | 0.0344828 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0218978 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 |  0.528169 |
|  0 | neon-deepseek-reasoner |    0.0294118 |         0.481915 |      0.361941 |       0.676559 |                  0.683339 |  0.533569 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0428571 |         0.624417 |      0.512057 |       0.800092 |                  0.794488 |                    0.724668 | 0.0428571 |
|  0 | neon-deepseek-reasoner |    0.0571429 |         0.622619 |      0.501359 |       0.789498 |                  0.801674 | 0.0571429 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
|  0 | neon-deepseek-reasoner |            0 |           0.5578 |      0.438017 |       0.726267 |                  0.626483 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.852002 |      0.752419 |       0.867221 |                  0.872009 |                    0.784061 |
|  0 | neon-deepseek-reasoner |            0 |         0.845322 |      0.762697 |       0.922653 |                  0.887936 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
|  0 | neon-deepseek-reasoner |            0 |           0.5578 |      0.438017 |       0.726267 |                  0.626483 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
|  0 | neon-deepseek-reasoner |            0 |           0.5578 |      0.438017 |       0.726267 |                  0.626483 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.667106 |      0.537915 |       0.786763 |                  0.733022 |                     0.66294 |
|  0 | neon-deepseek-reasoner |            0 |         0.672102 |      0.556459 |       0.812765 |                  0.734641 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
|  0 | neon-deepseek-reasoner |            0 |         0.752083 |      0.645117 |       0.882883 |                    0.6519 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.949524 |      0.930669 |       0.967414 |                  0.907582 |                    0.970931 |
|  0 | neon-deepseek-reasoner |            0 |         0.926877 |      0.875823 |       0.965427 |                  0.902659 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
|  0 | neon-deepseek-reasoner |            0 |         0.752083 |      0.645117 |       0.882883 |                    0.6519 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
|  0 | neon-deepseek-reasoner |            0 |         0.752083 |      0.645117 |       0.882883 |                    0.6519 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.857237 |      0.802094 |       0.926642 |                  0.771497 |                    0.892047 |
|  0 | neon-deepseek-reasoner |            0 |         0.830381 |      0.742972 |       0.922312 |                  0.757055 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
|  0 | neon-deepseek-reasoner |            0 |           0.7263 |      0.635517 |       0.878967 |                  0.666533 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.893271 |      0.870545 |       0.962849 |                  0.879495 |                    0.934042 |
|  0 | neon-deepseek-reasoner |            0 |         0.920318 |      0.900973 |       0.964855 |                  0.875577 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
|  0 | neon-deepseek-reasoner |            0 |           0.7263 |      0.635517 |       0.878967 |                  0.666533 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
|  0 | neon-deepseek-reasoner |            0 |           0.7263 |      0.635517 |       0.878967 |                  0.666533 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.79933 |      0.736537 |       0.919971 |                  0.758066 |                    0.859154 |
|  0 | neon-deepseek-reasoner |            0 |         0.811879 |      0.745314 |        0.91991 |                  0.756887 |
    
    