
# Ontology: software
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0254237 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 | 0.0151515 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |        0.125 |         0.875658 |      0.821837 |        0.94358 |                  0.961008 |                    0.932353 |     0.125 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0258621 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 | 0.0258621 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0218978 |         0.485203 |      0.371881 |       0.694483 |                  0.677153 |                    0.592653 |  0.528169 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |    0.0428571 |         0.624417 |      0.512057 |       0.800092 |                  0.794488 |                    0.724668 | 0.0428571 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.852002 |      0.752419 |       0.867221 |                  0.872009 |                    0.784061 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.54815 |      0.418583 |       0.719967 |                   0.63225 |                    0.574233 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.667106 |      0.537915 |       0.786763 |                  0.733022 |                     0.66294 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.949524 |      0.930669 |       0.967414 |                  0.907582 |                    0.970931 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |           0.7813 |      0.704733 |       0.889167 |                    0.6709 |                    0.825017 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.857237 |      0.802094 |       0.926642 |                  0.771497 |                    0.892047 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.893271 |      0.870545 |       0.962849 |                  0.879495 |                    0.934042 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |         0.723267 |      0.638283 |        0.88075 |                    0.6661 |                    0.795383 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |            0 |          0.79933 |      0.736537 |       0.919971 |                  0.758066 |                    0.859154 |
    
    