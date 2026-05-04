
# Ontology: odrl
## Concept Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.296296 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.112676 |
|  0 | neon-deepseek-reasoner |     0.111111 |         0.513296 |      0.403519 |       0.690407 |                      0.62 | 0.0422535 |
|  0 | deepseek-reasoner |     0.296296 |         0.642741 |      0.541704 |       0.765556 |                  0.715778 |  0.112676 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.533333 |         0.863992 |       0.81307 |       0.922428 |                   0.99808 |                    0.941969 |  0.533333 |
|  0 | neon-deepseek-reasoner |     0.272727 |         0.781934 |       0.69289 |       0.921499 |                   0.89629 |  0.272727 |
|  0 | deepseek-reasoner |          0.4 |         0.818662 |      0.736492 |       0.881262 |                  0.939341 |       0.4 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.296296 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.296296 |
|  0 | neon-deepseek-reasoner |     0.111111 |         0.513296 |      0.403519 |       0.690407 |                      0.62 |  0.111111 |
|  0 | deepseek-reasoner |     0.296296 |         0.642741 |      0.541704 |       0.765556 |                  0.715778 |  0.296296 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.235294 |         0.658074 |      0.558037 |       0.769852 |                  0.712222 |                    0.683556 |  0.666667 |
|  0 | neon-deepseek-reasoner |    0.0857143 |         0.513296 |      0.403519 |       0.690407 |                      0.62 |  0.594937 |
|  0 | deepseek-reasoner |     0.205128 |         0.642741 |      0.541704 |       0.765556 |                  0.715778 |  0.626506 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |   synonym |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|----------:|
|  0 | gemini_2.5_flash |     0.380952 |         0.747104 |      0.661835 |       0.839262 |                  0.831262 |                    0.792222 |  0.380952 |
|  0 | neon-deepseek-reasoner |     0.157895 |         0.619757 |      0.510018 |       0.789388 |                  0.732973 |  0.157895 |
|  0 | deepseek-reasoner |     0.340426 |         0.720113 |      0.624256 |       0.819344 |                  0.812461 |  0.340426 |
    
## Property Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
|  0 | neon-deepseek-reasoner |            0 |           0.5325 |      0.431312 |       0.724438 |                  0.656562 |
|  0 | deepseek-reasoner |         0.25 |         0.611438 |      0.530938 |       0.754375 |                  0.710625 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.105263 |          0.80154 |      0.722452 |       0.872715 |                   0.90052 |                    0.851295 |
|  0 | neon-deepseek-reasoner |            0 |          0.79985 |      0.759353 |       0.938543 |                  0.951798 |
|  0 | deepseek-reasoner |     0.285714 |         0.789971 |      0.771291 |       0.843466 |                  0.919903 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
|  0 | neon-deepseek-reasoner |            0 |           0.5325 |      0.431312 |       0.724438 |                  0.656562 |
|  0 | deepseek-reasoner |         0.25 |         0.611438 |      0.530938 |       0.754375 |                  0.710625 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0606061 |          0.70275 |        0.5995 |       0.793625 |                  0.779625 |                    0.729188 |
|  0 | neon-deepseek-reasoner |            0 |           0.5325 |      0.431312 |       0.724438 |                  0.656562 |
|  0 | deepseek-reasoner |     0.153846 |         0.611438 |      0.530938 |       0.754375 |                  0.710625 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.748901 |      0.655258 |       0.831293 |                  0.835723 |                    0.785524 |
|  0 | neon-deepseek-reasoner |            0 |         0.639352 |      0.550143 |       0.817707 |                  0.777083 |
|  0 | deepseek-reasoner |     0.266667 |         0.689332 |      0.628933 |       0.796437 |                  0.801834 |
    
## Property Domain Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |       0.0625 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
|  0 | neon-deepseek-reasoner |            0 |         0.719563 |      0.636813 |       0.874938 |                    0.7095 |
|  0 | deepseek-reasoner |       0.0625 |         0.794438 |        0.7215 |        0.90425 |                  0.792937 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0526316 |          0.90275 |      0.845719 |       0.941815 |                  0.900435 |                    0.952695 |
|  0 | neon-deepseek-reasoner |            0 |         0.849856 |       0.82229 |       0.954521 |                  0.928741 |
|  0 | deepseek-reasoner |    0.0714286 |         0.908318 |      0.873883 |       0.962352 |                  0.938318 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |       0.0625 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
|  0 | neon-deepseek-reasoner |            0 |         0.719563 |      0.636813 |       0.874938 |                    0.7095 |
|  0 | deepseek-reasoner |       0.0625 |         0.794438 |        0.7215 |        0.90425 |                  0.792937 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0294118 |           0.8575 |      0.785937 |         0.9115 |                  0.828625 |                    0.884875 |
|  0 | neon-deepseek-reasoner |            0 |         0.719563 |      0.636813 |       0.874938 |                    0.7095 |
|  0 | deepseek-reasoner |    0.0344828 |         0.794438 |        0.7215 |        0.90425 |                  0.792937 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0571429 |         0.879544 |      0.814733 |       0.926409 |                  0.863039 |                    0.917533 |
|  0 | neon-deepseek-reasoner |            0 |         0.779301 |      0.717763 |       0.912998 |                   0.80445 |
|  0 | deepseek-reasoner |    0.0666667 |          0.84757 |      0.790414 |       0.932397 |                  0.859524 |
    
## Property Range Baseline:

### coverage_rate:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
|  0 | neon-deepseek-reasoner |            0 |         0.768125 |      0.688687 |       0.894187 |                  0.723625 |
|  0 | deepseek-reasoner |       0.1875 |         0.802938 |         0.747 |       0.906875 |                  0.801438 |
### precision:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.105263 |         0.922339 |      0.874389 |       0.945074 |                  0.925882 |                    0.914941 |
|  0 | neon-deepseek-reasoner |            0 |         0.918535 |      0.905349 |       0.959107 |                  0.955123 |
|  0 | deepseek-reasoner |     0.214286 |         0.927782 |      0.878178 |       0.959847 |                  0.904366 |
### recall:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |        0.125 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
|  0 | neon-deepseek-reasoner |            0 |         0.768125 |      0.688687 |       0.894188 |                  0.723625 |
|  0 | deepseek-reasoner |       0.1875 |         0.802937 |         0.747 |       0.906875 |                  0.801438 |
### accuracy:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |    0.0606061 |         0.835063 |      0.770938 |       0.911937 |                   0.82525 |                    0.892125 |
|  0 | neon-deepseek-reasoner |            0 |         0.768125 |      0.688687 |       0.894187 |                  0.723625 |
|  0 | deepseek-reasoner |     0.111111 |         0.802938 |         0.747 |       0.906875 |                  0.801438 |
### f1:
|    | model            |   hard_match |   sequence_match |   levenshtein |   jaro_winkler |   semantic_embeddinggemma |   semantic_nomic-embed-text |
|---:|:-----------------|-------------:|-----------------:|--------------:|---------------:|--------------------------:|----------------------------:|
|  0 | gemini_2.5_flash |     0.114286 |         0.876533 |      0.819411 |        0.92821 |                  0.872674 |                    0.903389 |
|  0 | neon-deepseek-reasoner |            0 |         0.836624 |      0.782294 |        0.92551 |                  0.823412 |
|  0 | deepseek-reasoner |          0.2 |         0.860857 |      0.807295 |       0.932609 |                  0.849796 |
    
    