## Legend used in the speadsheet with the ground truth
The ontologies included in `ground_truth.csv` hav been selected from the [CORAL benchmark](https://coralcorpus.linkeddata.es/#ontologies) and several ontologies developed at the ontology engineering group. For each ontology, we keep the original source document and identifiers. In some cases, some CQs have been reformulated to make explicit the terms implied in the CQ. We include the following fields:
- `id`: identifier of the CQ within OEB
- `original_cq_id`: original identifier in the source ontology
- `source_ontology_uri`: URI of the source ontology
- `cq`: competency question (it may have been slightly modified from the original one in order to clarify terms)
- `ground_truth`: terms extracted from the cq according to the validators
- `validated_by`: person who validated the CQ as part of the benchmark
    - DG: Daniel Garijo
    - CW: Clark Wang
