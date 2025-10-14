# Ontology Concept Matching


### Execution

1. install [ollama](https://ollama.com/) with correspond models and start the service
2. pip install -r requirements.txt 
3. run the following command line in the `code` folder
```bash
python eval.py --model_id embeddinggemma,nomic-embed-text --generate_onto_file_path generated_software.owl --ground_onto_file_path ground_software.owl --save_file_path result.json 
```

