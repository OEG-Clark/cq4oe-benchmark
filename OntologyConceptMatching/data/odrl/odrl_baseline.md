
# Ontology: odrl
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.296296 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.112676 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.533333 |         0.863992 |       0.81307 |       0.922428 |                   0.99808 |                    0.941969 |  0.533333 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.296296 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.296296 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.235294 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.666667 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.380952 |         0.747104 |      0.661835 |       0.839262 |                  0.831262 |                    0.792222 |  0.380952 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.105263 |          0.80154 |      0.722452 |       0.872715 |                   0.90052 |                    0.851295 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0606061 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.748901 |      0.655258 |       0.831293 |                  0.835723 |                    0.785524 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |       0.0625 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0526316 |          0.90275 |      0.845719 |       0.941815 |                  0.900435 |                    0.952695 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |       0.0625 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0294118 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0571429 |         0.879544 |      0.814733 |       0.926409 |                  0.863039 |                    0.917533 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.105263 |         0.922339 |      0.874389 |       0.945074 |                  0.925882 |                    0.914941 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0606061 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.876533 |      0.819411 |        0.92821 |                  0.872674 |                    0.903389 |
    
    