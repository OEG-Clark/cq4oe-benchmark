
# Ontology: software
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0254237 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 | 0.0151515 |
|  0 | neon-deepseek-reasoner |    0.0254237 |         0.494483 |      0.380593 |       0.699246 |                  0.683797 | 0.0151515 |
|  0 | deepseek-reasoner |    0.0169492 |         0.472881 |      0.341983 |        0.68178 |                  0.667203 | 0.00757576 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |        0.125 |         0.875658 |      0.821837 |        0.94358 |                  0.961008 |                    0.932353 |     0.125 |
|  0 | neon-deepseek-reasoner |        0.125 |         0.882885 |      0.839675 |       0.952167 |                  0.964256 |     0.125 |
|  0 | deepseek-reasoner |         0.08 |         0.856511 |      0.743099 |       0.934118 |                  0.951167 |      0.08 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0258621 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 | 0.0258621 |
|  0 | neon-deepseek-reasoner |    0.0258621 |         0.494483 |      0.380593 |       0.699246 |                  0.683797 | 0.0258621 |
|  0 | deepseek-reasoner |    0.0172414 |         0.472881 |      0.341983 |        0.68178 |                  0.667203 | 0.0172414 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0218978 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 |  0.528169 |
|  0 | neon-deepseek-reasoner |    0.0218978 |         0.494483 |      0.380593 |       0.699246 |                  0.683797 |  0.528169 |
|  0 | deepseek-reasoner |    0.0143885 |         0.472881 |      0.341983 |        0.68178 |                  0.667203 |  0.522648 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0428571 |         0.624417 |      0.512057 |       0.800092 |                  0.794488 |                    0.724668 | 0.0428571 |
|  0 | neon-deepseek-reasoner |    0.0428571 |         0.633922 |      0.523778 |       0.806338 |                  0.800163 | 0.0428571 |
|  0 | deepseek-reasoner |    0.0283688 |         0.609343 |      0.468402 |       0.788246 |                  0.784273 | 0.0283688 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
|  0 | neon-deepseek-reasoner |            0 |         0.545183 |        0.4279 |       0.716317 |                  0.634967 |
|  0 | deepseek-reasoner |            0 |          0.55965 |      0.449317 |         0.7365 |                  0.652617 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.852002 |      0.752419 |       0.867221 |                  0.872009 |                    0.784061 |
|  0 | neon-deepseek-reasoner |            0 |         0.819599 |      0.753323 |       0.908878 |                  0.869976 |
|  0 | deepseek-reasoner |            0 |          0.79524 |      0.715491 |       0.899487 |                  0.891736 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
|  0 | neon-deepseek-reasoner |            0 |         0.545183 |        0.4279 |       0.716317 |                  0.634967 |
|  0 | deepseek-reasoner |            0 |          0.55965 |      0.449317 |         0.7365 |                  0.652617 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
|  0 | neon-deepseek-reasoner |            0 |         0.545183 |        0.4279 |       0.716317 |                  0.634967 |
|  0 | deepseek-reasoner |            0 |          0.55965 |      0.449317 |         0.7365 |                  0.652617 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.667106 |      0.537915 |       0.786763 |                  0.733022 |                     0.66294 |
|  0 | neon-deepseek-reasoner |            0 |         0.654803 |      0.545785 |       0.801189 |                  0.734122 |
|  0 | deepseek-reasoner |            0 |         0.656963 |      0.551992 |       0.809875 |                  0.753664 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
|  0 | neon-deepseek-reasoner |            0 |          0.74555 |      0.647967 |       0.882017 |                   0.66065 |
|  0 | deepseek-reasoner |            0 |         0.749667 |      0.656917 |       0.884633 |                  0.660883 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.949524 |      0.930669 |       0.967414 |                  0.907582 |                    0.970931 |
|  0 | neon-deepseek-reasoner |            0 |         0.922159 |      0.877627 |       0.961763 |                  0.906905 |
|  0 | deepseek-reasoner |            0 |         0.918859 |      0.856997 |       0.966478 |                  0.890258 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
|  0 | neon-deepseek-reasoner |            0 |          0.74555 |      0.647967 |       0.882017 |                   0.66065 |
|  0 | deepseek-reasoner |            0 |         0.749667 |      0.656917 |       0.884633 |                  0.660883 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
|  0 | neon-deepseek-reasoner |            0 |          0.74555 |      0.647967 |       0.882017 |                   0.66065 |
|  0 | deepseek-reasoner |            0 |         0.749667 |      0.656917 |       0.884633 |                  0.660883 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.857237 |      0.802094 |       0.926642 |                  0.771497 |                    0.892047 |
|  0 | neon-deepseek-reasoner |            0 |         0.824503 |      0.745511 |       0.920165 |                  0.764435 |
|  0 | deepseek-reasoner |            0 |         0.825685 |      0.743735 |       0.923746 |                  0.758611 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
|  0 | neon-deepseek-reasoner |            0 |         0.734317 |      0.649267 |         0.8817 |                  0.668633 |
|  0 | deepseek-reasoner |            0 |         0.730733 |       0.64445 |        0.87985 |                      0.68 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.893271 |      0.870545 |       0.962849 |                  0.879495 |                    0.934042 |
|  0 | neon-deepseek-reasoner |            0 |         0.906844 |      0.869806 |       0.959343 |                  0.855267 |
|  0 | deepseek-reasoner |            0 |         0.903274 |      0.880717 |       0.955683 |                  0.911752 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
|  0 | neon-deepseek-reasoner |            0 |         0.734317 |      0.649267 |         0.8817 |                  0.668633 |
|  0 | deepseek-reasoner |            0 |         0.730733 |       0.64445 |        0.87985 |                      0.68 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
|  0 | neon-deepseek-reasoner |            0 |         0.734317 |      0.649267 |         0.8817 |                  0.668633 |
|  0 | deepseek-reasoner |            0 |         0.730733 |       0.64445 |        0.87985 |                      0.68 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.79933 |      0.736537 |       0.919971 |                  0.758066 |                    0.859154 |
|  0 | neon-deepseek-reasoner |            0 |         0.811512 |      0.743527 |       0.918884 |                  0.750521 |
|  0 | deepseek-reasoner |            0 |         0.807894 |      0.744283 |         0.9162 |                  0.779005 |
    
    