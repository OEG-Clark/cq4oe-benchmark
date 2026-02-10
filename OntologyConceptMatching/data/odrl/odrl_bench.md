
# Ontology: odrl
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.296296 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.112676 |
|  0 | neon-deepseek-reasoner |     0.111111 |          0.52263 |      0.414778 |       0.696704 |                  0.629889 | 0.0422535 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.533333 |         0.863992 |       0.81307 |       0.922428 |                   0.99808 |                    0.941969 |  0.533333 |
|  0 | neon-deepseek-reasoner |       0.1875 |         0.810511 |      0.644102 |        0.86547 |                  0.908106 |    0.1875 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.296296 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.296296 |
|  0 | neon-deepseek-reasoner |     0.111111 |          0.52263 |      0.414778 |       0.696704 |                  0.629889 |  0.111111 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.235294 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.666667 |
|  0 | neon-deepseek-reasoner |        0.075 |          0.52263 |      0.414778 |       0.696704 |                  0.629889 |  0.559524 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.380952 |         0.747104 |      0.661835 |       0.839262 |                  0.831262 |                    0.792222 |  0.380952 |
|  0 | neon-deepseek-reasoner |     0.139535 |         0.635488 |      0.504607 |       0.771971 |                  0.743833 |  0.139535 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
|  0 | neon-deepseek-reasoner |       0.0625 |         0.514687 |      0.404375 |       0.722062 |                   0.64575 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.105263 |          0.80154 |      0.722452 |       0.872715 |                   0.90052 |                    0.851295 |
|  0 | neon-deepseek-reasoner |    0.0909091 |         0.700434 |      0.608712 |       0.897251 |                  0.923077 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
|  0 | neon-deepseek-reasoner |       0.0625 |         0.514687 |      0.404375 |       0.722062 |                   0.64575 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0606061 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
|  0 | neon-deepseek-reasoner |    0.0384615 |         0.514687 |      0.404375 |       0.722062 |                   0.64575 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.748901 |      0.655258 |       0.831293 |                  0.835723 |                    0.785524 |
|  0 | neon-deepseek-reasoner |    0.0740741 |         0.593364 |      0.485936 |        0.80018 |                  0.759901 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |       0.0625 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
|  0 | neon-deepseek-reasoner |            0 |         0.723437 |      0.646812 |       0.887437 |                     0.726 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0526316 |          0.90275 |      0.845719 |       0.941815 |                  0.900435 |                    0.952695 |
|  0 | neon-deepseek-reasoner |            0 |         0.897009 |      0.883247 |       0.952633 |                  0.879733 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |       0.0625 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
|  0 | neon-deepseek-reasoner |            0 |         0.723437 |      0.646812 |       0.887437 |                     0.726 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0294118 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
|  0 | neon-deepseek-reasoner |            0 |         0.723437 |      0.646812 |       0.887437 |                     0.726 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0571429 |         0.879544 |      0.814733 |       0.926409 |                  0.863039 |                    0.917533 |
|  0 | neon-deepseek-reasoner |            0 |         0.800927 |      0.746762 |        0.91888 |                  0.795507 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
|  0 | neon-deepseek-reasoner |            0 |         0.715812 |      0.641937 |       0.885625 |                  0.687875 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.105263 |         0.922339 |      0.874389 |       0.945074 |                  0.925882 |                    0.914941 |
|  0 | neon-deepseek-reasoner |            0 |         0.875478 |      0.871532 |        0.94228 |                  0.872384 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
|  0 | neon-deepseek-reasoner |            0 |         0.715812 |      0.641938 |       0.885625 |                  0.687875 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0606061 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
|  0 | neon-deepseek-reasoner |            0 |         0.715812 |      0.641937 |       0.885625 |                  0.687875 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.876533 |      0.819411 |        0.92821 |                  0.872674 |                    0.903389 |
|  0 | neon-deepseek-reasoner |            0 |         0.787635 |       0.73932 |       0.913074 |                   0.76922 |
    
    