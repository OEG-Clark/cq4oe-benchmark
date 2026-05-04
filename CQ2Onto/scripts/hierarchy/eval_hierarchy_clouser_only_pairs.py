import argparse
import csv
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

def _norm(text):

    if text is None:
        return ""
    s = str(text).strip()

    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", s)

    s = s.replace("_", " ")
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


def load_axioms(json_path: str) -> List[dict]:

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Axioms JSON not found: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "axioms" in data and isinstance(data["axioms"], list):
        return data["axioms"]
    if "gold_axioms" in data and isinstance(data["gold_axioms"], list):
        return data["gold_axioms"]
    raise ValueError(
        f"Unrecognized JSON in {json_path!r}. "
        f"Expected top-level 'axioms' or 'gold_axioms' list."
    )


def load_cq_definitions(json_path: str) -> List[dict]:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("cq_definitions", [])


def load_alignment_csv(csv_path: str) -> Dict[str, str]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Alignment CSV not found: {csv_path}")
    out: Dict[str, str] = {}
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            g = (row.get("Gold_term") or row.get("gold_term") or "").strip()
            p = (row.get("Pre_term") or row.get("pre_term")
                 or row.get("Pred_term") or row.get("pred_term") or "").strip()
            if g and p and g not in out:
                out[g] = p
    return out


def label_map_from_owl(owl_path: str) -> Dict[str, str]:
    try:
        from rdflib import Graph, RDF, RDFS, OWL, URIRef, Literal
    except ImportError:
        print("[warn] rdflib not installed; cannot read labels from OWL.",
              file=sys.stderr)
        return {}
    if not os.path.exists(owl_path):
        print(f"[warn] OWL file not found: {owl_path}", file=sys.stderr)
        return {}

    g = Graph()
    fmt_used = None
    for fmt in ("xml", "turtle", "n3", "json-ld"):
        try:
            g.parse(owl_path, format=fmt)
            fmt_used = fmt
            break
        except Exception:
            g = Graph()
            continue
    if fmt_used is None:
        try:
            g.parse(owl_path)
            fmt_used = "auto"
        except Exception as e:
            print(f"[warn] Could not parse OWL {owl_path}: {e}",
                  file=sys.stderr)
            return {}

    def _resolve_label(uri_node):
        labels = list(g.objects(uri_node, RDFS.label))
        for lb in labels:
            if isinstance(lb, Literal) and getattr(lb, "language", None) == "en":
                return str(lb).strip()
        for lb in labels:
            if isinstance(lb, Literal) and getattr(lb, "language", None) in (None, ""):
                return str(lb).strip()
        for lb in labels:
            if isinstance(lb, Literal):
                return str(lb).strip()
        s = str(uri_node)
        if "#" in s:
            local = s.split("#")[-1]
        else:
            local = s.rstrip("/").split("/")[-1]
        if local:
            return local
        return s

    out: Dict[str, str] = {}
    for type_class in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty):
        for s in g.subjects(RDF.type, type_class):
            if isinstance(s, URIRef):
                name = (str(s).split("#")[-1] if "#" in str(s)
                        else str(s).rstrip("/").split("/")[-1])
                out[name] = _resolve_label(s)
    return out

def asserted_hierarchy_from_owl(owl_path: str) -> Tuple[set, set, set, set]:
    try:
        from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode
    except ImportError:
        return set(), set(), set(), set()
    if not os.path.exists(owl_path):
        return set(), set(), set(), set()

    g = Graph()
    parsed = False
    for fmt in ("xml", "turtle", "n3", "json-ld"):
        try:
            g.parse(owl_path, format=fmt)
            parsed = True
            break
        except Exception:
            g = Graph()
    if not parsed:
        try:
            g.parse(owl_path)
            parsed = True
        except Exception:
            return set(), set(), set(), set()

    def _local(uri):
        s = str(uri)
        if "#" in s:
            return s.rsplit("#", 1)[1]
        if "/" in s:
            return s.rsplit("/", 1)[1]
        return s

    OWL_THING_NAMES = {"Thing", "Nothing"}

    asserted_class = set()
    derived_class_subjects = set()
    for sub, sup in g.subject_objects(RDFS.subClassOf):
        if not isinstance(sub, URIRef):
            continue   # we can't talk about an anonymous subject
        s = _local(sub)
        if s in OWL_THING_NAMES:
            continue
        if isinstance(sup, URIRef):
            p = _local(sup)
            if p in OWL_THING_NAMES or s == p:
                continue
            asserted_class.add((s, p))
        else:
            derived_class_subjects.add(s)

    asserted_prop = set()
    derived_prop_subjects = set()
    for sub, sup in g.subject_objects(RDFS.subPropertyOf):
        if not isinstance(sub, URIRef):
            continue
        s = _local(sub)
        if isinstance(sup, URIRef):
            p = _local(sup)
            if s == p:
                continue
            asserted_prop.add((s, p))
        else:
            derived_prop_subjects.add(s)


    for sub, sup in g.subject_objects(OWL.equivalentClass):
        if not isinstance(sub, URIRef) or not isinstance(sup, URIRef):

            continue
        s, p = _local(sub), _local(sup)
        if s in OWL_THING_NAMES or p in OWL_THING_NAMES or s == p:
            continue
        asserted_class.add((s, p))

    for sub, sup in g.subject_objects(OWL.equivalentProperty):
        if not isinstance(sub, URIRef) or not isinstance(sup, URIRef):
            continue
        s, p = _local(sub), _local(sup)
        if s == p:
            continue
        asserted_prop.add((s, p))

    return (asserted_class, asserted_prop,
            derived_class_subjects, derived_prop_subjects)


def compute_axiom_closure_hermit(owl_path: str, side_label: str = "") -> dict:
    if not owl_path or not os.path.isfile(owl_path):
        raise ValueError(f"compute_axiom_closure_hermit: invalid owl_path "
                         f"{owl_path!r}")

    try:
        import owlready2
        hermit_jar = os.path.join(os.path.dirname(owlready2.__file__),
                                  "hermit", "HermiT.jar")
    except ImportError as e:
        raise RuntimeError(f"Could not locate HermiT.jar: {e}")
    if not os.path.isfile(hermit_jar):
        raise RuntimeError(f"HermiT.jar not found at {hermit_jar}")

    print(f"[HermiT] Running on {side_label or 'ontology'} "
          f"({owl_path})...", file=sys.stderr)


    with open(owl_path, "r", encoding="utf-8") as f:
        owl_text = f.read()

    owl2_datatype_set = {
        "string", "boolean", "decimal", "integer", "double", "float",
        "long", "int", "short", "byte", "unsignedLong", "unsignedInt",
        "unsignedShort", "unsignedByte", "positiveInteger",
        "nonNegativeInteger", "negativeInteger", "nonPositiveInteger",
        "anyURI", "language", "dateTime", "dateTimeStamp",
        "Name", "NCName", "NMTOKEN", "token", "normalizedString",
    }


    deleted_datatypes = []      
    max_retries = 10
    classified_text = None

    def _run_hermit(text):
        with tempfile.NamedTemporaryFile(suffix=".owl", mode="w",
                                          encoding="utf-8", delete=False) as tmp:
            tmp.write(text)
            tmp_path = tmp.name
        try:
            cmd = [
                "java", "-Xmx2G",
                "-cp", hermit_jar,
                "org.semanticweb.HermiT.cli.CommandLine",
                "--classify",
                "-O",
                f"file:{tmp_path}",
            ]
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=300)
                return proc.returncode, proc.stdout, proc.stderr
            except subprocess.TimeoutExpired:
                return 1, "", "HermiT timeout (>300s)"
            except FileNotFoundError as e:
                return 1, "", f"java executable not found: {e}"
        finally:
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    def _extract_unsupported_iri(err_text):
        m = re.search(
            r"UnsupportedDatatypeException[^']*'([^']+)'", err_text)
        if m:
            return m.group(1)
        m = re.search(r"datatype\s+'([^']+)'\s+is\s+not", err_text,
                      flags=re.IGNORECASE)
        if m:
            return m.group(1)
        m = re.search(r"<(http[^>]+)>", err_text)
        if m:
            return m.group(1)
        return None

    def _classify_severity(removed_lines: List[str]) -> Tuple[str, int]:
        for line in removed_lines:
            line_lower = line.lower()
            if "datatypedefinition" in line_lower:
                return ("datatype_definition", len(removed_lines))
            if any(tag in line_lower for tag in [
                "datasomevaluesfrom", "dataallvaluesfrom",
                "datamincardinality", "datamaxcardinality",
                "dataexactcardinality", "datahasvalue",
            ]):
                return ("class_restriction", len(removed_lines))
        for line in removed_lines:
            ln = line.lower()
            if "datapropertyrange" in ln or "datapropertydomain" in ln:
                if "datapropertyrange" in ln:
                    return ("data_property_range", len(removed_lines))
                return ("data_property_domain", len(removed_lines))
        for line in removed_lines:
            if "<" not in line and (line.strip().startswith("\"")
                                     or "literal" in line.lower()):
                return ("abox_literal", len(removed_lines))
        return ("unknown", len(removed_lines))
    rc, classified_text, stderr_text = _run_hermit(owl_text)

    retry = 0
    while rc != 0 and retry < max_retries:
        # Check for an UnsupportedDatatype error
        bad_iri = _extract_unsupported_iri(stderr_text)
        if not bad_iri:
            # Not a datatype error — propagate
            err = stderr_text.strip()[:500] if stderr_text else f"rc={rc}"
            raise RuntimeError(f"HermiT CLI failed (rc={rc}): {err}")

        bad_local = bad_iri.split("#")[-1].split("/")[-1]
        if bad_local in owl2_datatype_set:
            err = stderr_text.strip()[:500] if stderr_text else f"rc={rc}"
            raise RuntimeError(
                f"HermiT rejected OWL-2 datatype xsd:{bad_local}, which "
                f"should be supported. This is unusual. rc={rc}, err={err}")

        # Remove every line containing this IRI
        old_lines = owl_text.split("\n")
        kept = []
        removed = []
        for line in old_lines:
            if bad_iri in line:
                removed.append(line)
            else:
                kept.append(line)
        owl_text = "\n".join(kept)

        severity, n = _classify_severity(removed)
        sample = removed[0].strip()[:120] if removed else "<empty>"
        deleted_datatypes.append((bad_iri, n, severity, sample))
        print(f"  [HermiT preprocess] HermiT rejected {bad_iri!r}; removed "
              f"{n} line(s). [severity: {severity}]",
              file=sys.stderr)

        retry += 1
        rc, classified_text, stderr_text = _run_hermit(owl_text)

    if rc != 0:
        raise RuntimeError(
            f"HermiT failed after {max_retries} datatype-removal retries: "
            f"{stderr_text.strip()[:500]}")

    if deleted_datatypes:
        risky = sum(1 for (_, _, sev, _) in deleted_datatypes
                    if sev in ("class_restriction", "datatype_definition"))
        moderate = sum(1 for (_, _, sev, _) in deleted_datatypes
                       if sev in ("data_property_range",
                                  "data_property_domain"))
        total_lines = sum(n for (_, n, _, _) in deleted_datatypes)
        print(f"  [HermiT preprocess] Total removed: {total_lines} line(s) "
              f"across {len(deleted_datatypes)} datatype(s). "
              f"Risky (may affect class hierarchy): {risky}; "
              f"moderate (data property def): {moderate}; "
              f"the rest are typically harmless ABox literals or unused.",
              file=sys.stderr)
        if risky > 0:
            print(f"  [HermiT preprocess] WARNING: {risky} of these lines "
                  f"appear inside class restrictions or datatype definitions. "
                  f"Their deletion may change the inferred class hierarchy. "
                  f"Treat results with caution; the dropped axioms are "
                  f"reported above so you can verify they don't affect "
                  f"the gold/pred properties under evaluation.",
                  file=sys.stderr)
        elif moderate > 0:
            print(f"  [HermiT preprocess] Note: {moderate} line(s) were "
                  f"DataProperty Domain/Range declarations. Class hierarchy "
                  f"inference is unaffected unless these properties appear "
                  f"inside a class restriction (typically they don't).",
                  file=sys.stderr)

    iri_pattern = r"<([^>]+)>"

    class_pairs_raw = set()
    prop_pairs_raw = set()

    for line in classified_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("SubClassOf("):
            iris = re.findall(iri_pattern, line)
            if len(iris) == 2:
                class_pairs_raw.add((iris[0], iris[1]))
        elif line.startswith("SubObjectPropertyOf(") or \
             line.startswith("SubDataPropertyOf("):
            iris = re.findall(iri_pattern, line)
            if len(iris) == 2:
                prop_pairs_raw.add((iris[0], iris[1]))

    if not class_pairs_raw and not prop_pairs_raw:
        non_empty_lines = [ln for ln in classified_text.splitlines()
                           if ln.strip()]
        if non_empty_lines:
            preview = "\n".join(non_empty_lines[:20])
            print(f"[warn] HermiT classification produced output but "
                  f"no SubClassOf/SubPropertyOf hierarchy pairs were "
                  f"parsed for {side_label or 'ontology'}. The parser "
                  f"may not match HermiT's output format. First lines "
                  f"of output:\n{preview}\n", file=sys.stderr)

    def _local_name(iri: str) -> str:
        if "#" in iri:
            return iri.rsplit("#", 1)[1]
        if "/" in iri:
            return iri.rsplit("/", 1)[1]
        return iri

    OWL_THING = {"Thing", "Nothing"}

    class_hierarchy = set()
    for s_iri, p_iri in class_pairs_raw:
        s, p = _local_name(s_iri), _local_name(p_iri)
        if s in OWL_THING or p in OWL_THING or s == p:
            continue
        class_hierarchy.add((s, p))

    property_hierarchy = set()
    for s_iri, p_iri in prop_pairs_raw:
        s, p = _local_name(s_iri), _local_name(p_iri)
        if s == p:
            continue
        property_hierarchy.add((s, p))

    name_to_label = {}
    try:
        name_to_label = label_map_from_owl(owl_path)
    except Exception:
        pass


    (asserted_class, asserted_prop,
     derived_class_subjects, derived_prop_subjects) = \
        asserted_hierarchy_from_owl(owl_path)

    asserted_class = asserted_class & class_hierarchy
    asserted_prop = asserted_prop & property_hierarchy

    print(f"  [HermiT] {side_label}: {len(class_hierarchy)} class + "
          f"{len(property_hierarchy)} property entailments "
          f"({len(asserted_class)} asserted class, "
          f"{len(asserted_prop)} asserted prop, "
          f"{len(derived_class_subjects)} class subjects with "
          f"complex-sup axioms)",
          file=sys.stderr)

    return {
        "class_hierarchy": class_hierarchy,
        "property_hierarchy": property_hierarchy,
        "asserted_class": asserted_class,
        "asserted_prop": asserted_prop,
        "derived_class_subjects": derived_class_subjects,
        "derived_prop_subjects":  derived_prop_subjects,
        "name_to_label": name_to_label,
        "reasoner": "HermiT",
        "soundness": "complete",
    }


def _split_camel(name: str) -> str:
    if not name:
        return name
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", spaced)
    return spaced

def compute_hermit_evaluation(
    gold_owl_path: str, pred_owl_path: str,
    class_align: Dict[str, str], prop_align: Dict[str, str],
) -> dict:

    if not gold_owl_path:
        raise RuntimeError("Need --gold_owl. HermiT requires an OWL file.")
    if not pred_owl_path:
        raise RuntimeError("Need --pred_owl. HermiT requires an OWL file.")

    print("\n[HermiT] Computing gold closure...", file=sys.stderr)
    gold_clos = compute_axiom_closure_hermit(gold_owl_path,
                                             side_label="gold")
    print("[HermiT] Computing pred closure...", file=sys.stderr)
    pred_clos = compute_axiom_closure_hermit(pred_owl_path,
                                             side_label="pred")


    inv_class_to_label = {v: k for k, v in class_align.items()}
    inv_prop_to_label = {v: k for k, v in prop_align.items()}
    inv_class_to_label_norm = {_norm(v): k for k, v in class_align.items()}
    inv_prop_to_label_norm = {_norm(v): k for k, v in prop_align.items()}

    gold_label_to_iri = {}
    gold_label_to_iri_ci = {}
    for iri, lbl in gold_clos["name_to_label"].items():
        if lbl not in gold_label_to_iri:
            gold_label_to_iri[lbl] = iri
        if iri not in gold_label_to_iri:
            gold_label_to_iri[iri] = iri
        gold_label_to_iri_ci.setdefault(_norm(lbl), iri)
        gold_label_to_iri_ci.setdefault(_norm(iri), iri)

    def _normalize_to_gold_iri(name: str) -> str:
        if name in gold_label_to_iri:
            return gold_label_to_iri[name]
        if _norm(name) in gold_label_to_iri_ci:
            return gold_label_to_iri_ci[_norm(name)]
        return name

    def _pred_to_gold_iri(pred_name: str,
                          inv_map: Dict[str, str]) -> Optional[str]:
        if inv_map is inv_class_to_label:
            inv_norm = inv_class_to_label_norm
        elif inv_map is inv_prop_to_label:
            inv_norm = inv_prop_to_label_norm
        else:
            inv_norm = {_norm(k): v for k, v in inv_map.items()}

        pred_label = pred_clos["name_to_label"].get(pred_name, pred_name)
        split_form = _split_camel(pred_name)
        variants = [pred_name]
        for v in (pred_label, split_form):
            if v and v not in variants:
                variants.append(v)
        for key in variants:
            gold_term = inv_map.get(key)
            if gold_term is not None:
                return _normalize_to_gold_iri(gold_term)
            gold_term = inv_norm.get(_norm(key))
            if gold_term is not None:
                return _normalize_to_gold_iri(gold_term)
        return None

    def _translate_set(pred_pairs, inv_map):
        translated = set()
        untranslated = set()

        gold_to_pred_pairs: Dict[Tuple[str, str], List[Tuple[str, str]]] = {}
        for sub, sup in pred_pairs:
            g_sub = _pred_to_gold_iri(sub, inv_map)
            g_sup = _pred_to_gold_iri(sup, inv_map)
            if g_sub is not None and g_sup is not None:
                gold_pair = (g_sub, g_sup)
                translated.add(gold_pair)
                gold_to_pred_pairs.setdefault(gold_pair, []).append(
                    (sub, sup))
            else:
                untranslated.add((sub, sup))
        return translated, untranslated, gold_to_pred_pairs

    pred_class_translated, pred_class_untrans, class_pred_origin = \
        _translate_set(pred_clos["class_hierarchy"], inv_class_to_label)
    pred_prop_translated, pred_prop_untrans, prop_pred_origin = \
        _translate_set(pred_clos["property_hierarchy"], inv_prop_to_label)

    pred_asserted_class_translated, _, _ = \
        _translate_set(pred_clos.get("asserted_class", set()),
                       inv_class_to_label)
    pred_asserted_prop_translated, _, _ = \
        _translate_set(pred_clos.get("asserted_prop", set()),
                       inv_prop_to_label)

    def _metrics(gold_set, pred_translated, n_untranslated=0):
        tp = gold_set & pred_translated
        fn = gold_set - pred_translated
        fp = pred_translated - gold_set

        n_tp = len(tp)
        n_fp = len(fp) + n_untranslated
        n_fn = len(fn)
        p = n_tp / (n_tp + n_fp) if (n_tp + n_fp) else 0.0
        r = n_tp / (n_tp + n_fn) if (n_tp + n_fn) else 0.0
        f = 2 * p * r / (p + r) if (p + r) else 0.0
        return {"tp": tp, "fp": fp, "fn": fn,
                "n_tp": n_tp, "n_fp": n_fp, "n_fn": n_fn,
                "n_untranslated_in_fp": n_untranslated,
                "precision": p, "recall": r, "f1": f}

    cls_metrics = _metrics(gold_clos["class_hierarchy"],
                           pred_class_translated,
                           n_untranslated=len(pred_class_untrans))
    prp_metrics = _metrics(gold_clos["property_hierarchy"],
                           pred_prop_translated,
                           n_untranslated=len(pred_prop_untrans))

    combined_gold = gold_clos["class_hierarchy"] | {
        ("PROP:" + s, "PROP:" + p) for s, p in gold_clos["property_hierarchy"]
    }
    combined_pred = pred_class_translated | {
        ("PROP:" + s, "PROP:" + p) for s, p in pred_prop_translated
    }
    combined_metrics = _metrics(
        combined_gold, combined_pred,
        n_untranslated=len(pred_class_untrans) + len(pred_prop_untrans))

    return {
        "gold_closure": gold_clos,
        "pred_closure": pred_clos,
        "gold_reasoner": gold_clos.get("reasoner", "HermiT (CLI)"),
        "pred_reasoner": pred_clos.get("reasoner", "HermiT (CLI)"),
        "pred_class_translated": pred_class_translated,
        "pred_prop_translated": pred_prop_translated,
        "pred_asserted_class_translated": pred_asserted_class_translated,
        "pred_asserted_prop_translated": pred_asserted_prop_translated,
        "untranslated_class": pred_class_untrans,
        "untranslated_prop": pred_prop_untrans,
        "class_metrics": cls_metrics,
        "property_metrics": prp_metrics,
        "combined_metrics": combined_metrics,
        "_inv_class_to_label": inv_class_to_label,
        "_inv_prop_to_label": inv_prop_to_label,
        "_pred_label_map": pred_clos.get("name_to_label", {}),
        "_class_pred_origin": class_pred_origin,
        "_prop_pred_origin": prop_pred_origin,
    }

def compute_cq_coverage_closure(result: dict, gold_axioms: List[dict],
                                cq_definitions: List[dict],
                                strict_covered_cqs=None) -> dict:
    if strict_covered_cqs is None:
        strict_any = set()
        strict_fully = set()
        strict_rate: Dict[str, float] = {}
        strict_missing_axioms: Dict[str, list] = {}
        strict_tp_axioms: Dict[str, list] = {}
        strict_n_axioms: Dict[str, int] = {}
        strict_n_tp: Dict[str, int] = {}
    elif isinstance(strict_covered_cqs, dict):
        strict_any = set(strict_covered_cqs.get("any") or set())
        strict_fully = set(strict_covered_cqs.get("fully") or set())
        strict_rate = dict(strict_covered_cqs.get("rate") or {})
        strict_missing_axioms = dict(
            strict_covered_cqs.get("missing_axioms") or {})
        strict_tp_axioms = dict(
            strict_covered_cqs.get("tp_axioms") or {})
        strict_n_axioms = dict(strict_covered_cqs.get("n_axioms") or {})
        strict_n_tp = dict(strict_covered_cqs.get("n_tp") or {})
    else:
        strict_any = set(strict_covered_cqs)
        strict_fully = set()
        strict_rate = {}
        strict_missing_axioms = {}
        strict_tp_axioms = {}
        strict_n_axioms = {}
        strict_n_tp = {}

    gold_class_clos = result["gold_closure"]["class_hierarchy"]
    gold_prop_clos = result["gold_closure"]["property_hierarchy"]
    pred_class_trans = result["pred_class_translated"]
    pred_prop_trans = result["pred_prop_translated"]

    frag_to_label: Dict[str, str] = (
        result["gold_closure"].get("name_to_label") or {}
    )
    def _as_label(name: str) -> str:
        return frag_to_label.get(name, name)

    def _extract_names_from_struct(struct):
        if not struct or not isinstance(struct, dict):
            return
        et = struct.get("expr_type", "")
        if et in ("Class", "ObjectProperty", "DatatypeProperty",
                  "NamedEntity", "InverseObjectProperty"):
            name = struct.get("name")
            if name:
                yield name
            return

        if "property" in struct:
            p = struct.get("property")
            if p:
                yield p
        if "filler" in struct:
            yield from _extract_names_from_struct(struct["filler"])
        if "operand" in struct:
            yield from _extract_names_from_struct(struct["operand"])
        if "operands" in struct:
            for op in struct["operands"] or []:
                yield from _extract_names_from_struct(op)
        if "chain" in struct:
            for op in struct["chain"] or []:
                yield from _extract_names_from_struct(op)
        if et == "ObjectOneOf":
            for ind in struct.get("individuals") or []:
                if ind:
                    yield ind


    label_to_frag: Dict[str, str] = {}
    label_to_frag_norm: Dict[str, str] = {}
    for frag, label in frag_to_label.items():
        label_to_frag.setdefault(label, frag)
        label_to_frag_norm.setdefault(_norm(label), frag)
        label_to_frag_norm.setdefault(_norm(frag), frag)

    def _to_frag(name: str) -> str:
        if name in label_to_frag:
            return label_to_frag[name]
        n = _norm(name)
        if n in label_to_frag_norm:
            return label_to_frag_norm[n]
        return name

    def _is_atomic_class(struct) -> bool:
        return (isinstance(struct, dict)
                and struct.get("expr_type") == "Class"
                and struct.get("name"))

    def _is_atomic_property(struct) -> bool:
        return (isinstance(struct, dict)
                and struct.get("expr_type") in ("ObjectProperty",
                                                "DatatypeProperty",
                                                "NamedEntity")
                and struct.get("name"))

    def axiom_required_pair(ax):
        ax_type = ax.get("axiom_type") or ""
        sub_label = ax.get("subject")
        if not sub_label:
            return None
        rhs = ax.get("rhs_struct")

        if ax_type == "SubClassOf":
            if _is_atomic_class(rhs):
                return ("class", _to_frag(sub_label),
                        _to_frag(rhs["name"]))
            return None
        if ax_type in ("SubPropertyOf", "SubObjectPropertyOf",
                       "SubDataPropertyOf"):
            obj = ax.get("object")
            if obj:
                return ("property", _to_frag(sub_label), _to_frag(obj))
            return None
        if ax_type == "EquivalentClasses":
            if _is_atomic_class(rhs):
                return ("class", _to_frag(sub_label),
                        _to_frag(rhs["name"]))
            return None
        if ax_type in ("EquivalentObjectProperties",
                       "EquivalentDataProperties",
                       "EquivalentProperties"):
            obj = ax.get("object")
            if obj:
                return ("property", _to_frag(sub_label), _to_frag(obj))
            return None
        return None

    def bfs_shortest_path(start, end, edges, max_depth=6):
        if start == end or start is None or end is None:
            return None
        adj: Dict[str, list] = {}
        for a, b in edges:
            adj.setdefault(a, []).append(b)
        if start not in adj:
            return None
        from collections import deque
        visited = {start}
        parent: Dict[str, Tuple[str, Tuple[str, str]]] = {}
        queue = deque([(start, 0)])
        found = False
        while queue:
            node, depth = queue.popleft()
            if depth >= max_depth:
                continue
            for nxt in adj.get(node, []):
                if nxt in visited:
                    continue
                visited.add(nxt)
                parent[nxt] = (node, (node, nxt))
                if nxt == end:
                    found = True
                    break
                queue.append((nxt, depth + 1))
            if found:
                break
        if not found:
            return None
        path = []
        cur = end
        while cur in parent:
            prev, edge = parent[cur]
            path.append(edge)
            cur = prev
        path.reverse()
        return path

    pred_asserted_class_trans = result.get(
        "pred_asserted_class_translated", set())
    pred_asserted_prop_trans = result.get(
        "pred_asserted_prop_translated", set())

    def evaluate_axiom_rescue(ax):
        req = axiom_required_pair(ax)
        if req is None:
            return {"eligible": False, "rescued": False,
                    "mode": "not_eligible", "pair": None, "path": None}
        kind, sub, sup = req
        pair = (sub, sup)
        if kind == "class":
            asserted_set = pred_asserted_class_trans
            closure_set = pred_class_trans
            edges = pred_asserted_class_trans
        else:
            asserted_set = pred_asserted_prop_trans
            closure_set = pred_prop_trans
            edges = pred_asserted_prop_trans

        if pair in asserted_set:
            return {"eligible": True, "rescued": True,
                    "mode": "direct_asserted", "pair": req, "path": None}
        if pair in closure_set:
            path = bfs_shortest_path(sub, sup, edges)
            if path:
                return {"eligible": True, "rescued": True,
                        "mode": "simple_hierarchy_inferred",
                        "pair": req, "path": path}
            return {"eligible": True, "rescued": True,
                    "mode": "complex_inferred", "pair": req, "path": None}
        return {"eligible": True, "rescued": False,
                "mode": "uncovered", "pair": req, "path": None}

    gold_axiom_by_id = {ax["id"]: ax for ax in gold_axioms if ax.get("id")}

    gold_axioms_by_subject_index: Dict[str, list] = {}
    for ax in gold_axioms:
        s = ax.get("subject")
        if not s:
            continue
        s_frag = _to_frag(s)
        gold_axioms_by_subject_index.setdefault(s_frag, []).append({
            "id": ax.get("id", ""),
            "axiom_type": ax.get("axiom_type", ""),
            "dl": ax.get("dl", ""),
        })

    def gold_axioms_to_hierarchy_pairs_for_cq(cq_id):

        class_pairs = set()
        prop_pairs = set()
        used_axioms = []
        pair_to_axioms: Dict[Tuple[str, str, str], list] = {}

        def _record_pair(kind, sub, sup, ax_id):
            key = (kind, sub, sup)
            if ax_id not in pair_to_axioms.setdefault(key, []):
                pair_to_axioms[key].append(ax_id)

        for ax in gold_axioms:
            if cq_id not in (ax.get("cq_numbers") or []):
                continue
            ax_type = ax.get("axiom_type") or ""
            sub = ax.get("subject")
            if not sub:
                continue
            rhs = ax.get("rhs_struct")
            ax_id = ax.get("id", "?")

            if ax_type == "SubClassOf":

                if _is_atomic_class(rhs):
                    s_frag = _to_frag(sub)
                    p_frag = _to_frag(rhs["name"])
                    class_pairs.add((s_frag, p_frag))
                    _record_pair("class", s_frag, p_frag, ax_id)
                    used_axioms.append(ax_id)


            elif ax_type in ("SubPropertyOf",
                             "SubObjectPropertyOf",
                             "SubDataPropertyOf"):

                obj = ax.get("object")
                if obj:
                    s_frag = _to_frag(sub)
                    p_frag = _to_frag(obj)
                    prop_pairs.add((s_frag, p_frag))
                    _record_pair("property", s_frag, p_frag, ax_id)
                    used_axioms.append(ax_id)

            elif ax_type == "EquivalentClasses":

                if _is_atomic_class(rhs):
                    a = _to_frag(sub)
                    b = _to_frag(rhs["name"])
                    class_pairs.add((a, b))
                    _record_pair("class", a, b, ax_id)
                    used_axioms.append(ax_id)

            elif ax_type in ("EquivalentObjectProperties",
                             "EquivalentDataProperties",
                             "EquivalentProperties"):
                obj = ax.get("object")
                if obj:
                    a = _to_frag(sub)
                    b = _to_frag(obj)
                    prop_pairs.add((a, b))
                    _record_pair("property", a, b, ax_id)
                    used_axioms.append(ax_id)



        return class_pairs, prop_pairs, used_axioms, pair_to_axioms

    if cq_definitions:
        cq_ids = [c["id"] for c in cq_definitions]
        cq_q = {c["id"]: c.get("question", "") for c in cq_definitions}
    else:
        cq_ids_seen = set()
        for ax in gold_axioms:
            cq_ids_seen.update(ax.get("cq_numbers") or [])
        cq_ids = sorted(cq_ids_seen, key=lambda x: (len(x), x))
        cq_q = {cq: "" for cq in cq_ids}

    per_cq = {}
    n_fully = 0
    n_any = 0
    sum_rate = 0.0
    n_with_relevant = 0
    for cq_id in cq_ids:
        (gold_relevant_class, gold_relevant_prop,
         used_axiom_ids, pair_to_axioms) = \
            gold_axioms_to_hierarchy_pairs_for_cq(cq_id)

        gold_relevant_class &= gold_class_clos
        gold_relevant_prop  &= gold_prop_clos

        matched_class = gold_relevant_class & pred_class_trans
        matched_prop  = gold_relevant_prop  & pred_prop_trans
        missing_class = gold_relevant_class - pred_class_trans
        missing_prop  = gold_relevant_prop  - pred_prop_trans
        n_relevant = len(gold_relevant_class) + len(gold_relevant_prop)
        n_matched  = len(matched_class) + len(matched_prop)

        is_strict_any = cq_id in strict_any
        is_strict_fully = cq_id in strict_fully
        strict_rate_value = strict_rate.get(cq_id)

        is_closure_any = n_matched > 0
        is_closure_fully = (n_relevant > 0 and n_matched == n_relevant)
        rate_closure = (n_matched / n_relevant) if n_relevant else 0.0

        is_fully = is_strict_fully or is_closure_fully
        is_any = is_strict_any or is_closure_any
        if strict_rate_value is not None:
            rate = max(strict_rate_value, rate_closure)
        else:
            rate = rate_closure

        if is_fully:
            n_fully += 1
        if is_any:
            n_any += 1

        sum_rate += rate
        if n_relevant > 0 or is_strict_any:
            n_with_relevant += 1

        matched_typed = (
            [{"kind": "class", "sub": s, "sup": p}
             for (s, p) in sorted(matched_class)]
            + [{"kind": "property", "sub": s, "sup": p}
               for (s, p) in sorted(matched_prop)]
        )
        missing_typed = (
            [{"kind": "class", "sub": s, "sup": p}
             for (s, p) in sorted(missing_class)]
            + [{"kind": "property", "sub": s, "sup": p}
               for (s, p) in sorted(missing_prop)]
        )

        cq_missing_ax_ids = strict_missing_axioms.get(cq_id, [])
        cq_n_axioms = strict_n_axioms.get(cq_id)
        rescue_records = []
        n_rescued = 0
        for ax_id in cq_missing_ax_ids:
            ax = gold_axiom_by_id.get(ax_id)
            if not ax:
                rescue_records.append({
                    "axiom_id": ax_id, "eligible": False,
                    "rescued": False, "mode": "not_eligible",
                    "reason": "axiom not found in gold JSON",
                })
                continue
            r = evaluate_axiom_rescue(ax)
            rec = {
                "axiom_id": ax_id,
                "axiom_type": ax.get("axiom_type"),
                "eligible": r["eligible"],
                "rescued": r["rescued"],
                "mode": r["mode"],
            }
            if r["pair"]:
                kind, sub, sup = r["pair"]
                rec["kind"] = kind
                rec["sub"] = sub
                rec["sup"] = sup
            if r["path"]:
                rec["path"] = [{"sub": a, "sup": b} for (a, b) in r["path"]]
                rec["path_length"] = len(r["path"])
            rescue_records.append(rec)
            if r["rescued"]:
                n_rescued += 1

        n_strict_tp = None
        rescued_rate = None
        if cq_n_axioms and cq_n_axioms > 0:
            cq_tp_ids = strict_tp_axioms.get(cq_id)
            cq_n_tp = strict_n_tp.get(cq_id)
            if cq_n_tp is not None:
                n_strict_tp = cq_n_tp
            elif cq_tp_ids is not None:
                n_strict_tp = len(cq_tp_ids)
            else:

                n_strict_tp = cq_n_axioms - len(cq_missing_ax_ids)
            rescued_rate = (n_strict_tp + n_rescued) / cq_n_axioms
            if is_fully:
                n_fully -= 1
            if is_any:
                n_any -= 1
            sum_rate -= rate

            rate = rescued_rate
            is_fully = (rescued_rate >= 1.0 - 1e-9)
            is_any = ((n_strict_tp + n_rescued) > 0)

            sum_rate += rate
            if is_fully:
                n_fully += 1
            if is_any:
                n_any += 1

        if cq_n_axioms is not None:
            has_rescue = (n_rescued > 0)
            if is_strict_any and has_rescue:
                source = "strict + rescued"
            elif is_strict_any:
                source = "strict-only"
            elif has_rescue:
                source = "rescued-only"
            else:
                source = "none"
        else:
            if is_strict_any and is_closure_any:
                source = "both"
            elif is_strict_any:
                source = "strict"
            elif is_closure_any:
                source = "closure-new"
            else:
                source = "none"

        per_cq[cq_id] = {
            "id": cq_id,
            "question": cq_q.get(cq_id, ""),
            "n_relevant": n_relevant,
            "n_matched": n_matched,
            "n_missing": len(missing_class) + len(missing_prop),
            "rate": rate,
            "fully_covered": is_fully,
            "any_covered": is_any,
            "covered": is_any,
            "source": source,
            "matched_examples": sorted(matched_class | matched_prop),
            "matched_entailments": matched_typed,
            "missing_entailments": missing_typed,
            "source_axioms": sorted(set(used_axiom_ids)),
            "pair_axiom_records": [
                {"kind": kind, "sub": sub, "sup": sup,
                 "axioms": list(axs)}
                for (kind, sub, sup), axs in pair_to_axioms.items()
            ],
            "axiom_rescue": rescue_records,
            "n_strict_tp": n_strict_tp,
            "n_closure_rescued": n_rescued,
            "n_axioms_total": cq_n_axioms,
        }

    n_total = len(cq_ids)
    avg_rate = (sum_rate / n_total) if n_total else 0.0

    return {
        "per_cq": per_cq,
        "n_total": n_total,
        "n_fully_covered": n_fully,
        "n_any_covered": n_any,
        "average_rate": avg_rate,
        "fully_coverage": (n_fully / n_total) if n_total else 0.0,
        "any_coverage":   (n_any / n_total) if n_total else 0.0,
        "n_covered": n_any,
        "coverage":  (n_any / n_total) if n_total else 0.0,
        "axiom_origin": {
            cq_id: per_cq[cq_id].get("source_axioms", [])
            for cq_id in per_cq
        },
        "gold_axioms_by_subject": gold_axioms_by_subject_index,
        "concept_origin": {},
    }


def load_strict_covered_cqs(strict_csv_path: str) -> dict:
    out = {"any": set(), "fully": set(), "rate": {},
           "missing_axioms": {}, "tp_axioms": {},
           "n_axioms": {}, "n_tp": {}}
    if not strict_csv_path or not os.path.exists(strict_csv_path):
        return out
    try:
        with open(strict_csv_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cq_id = (row.get("cq_id") or row.get("id")
                         or row.get("CQ") or "").strip()
                if not cq_id:
                    continue
                cov = (row.get("covered") or row.get("Covered")
                       or row.get("status") or "").strip().lower()
                fully = (row.get("fully_covered")
                         or row.get("Fully_covered") or "").strip().lower()
                rate_raw = (row.get("rate") or row.get("Rate")
                            or "").strip()
                if cov in ("true", "yes", "1", "covered"):
                    out["any"].add(cq_id)
                if fully in ("true", "yes", "1"):
                    out["fully"].add(cq_id)
                if rate_raw:
                    try:
                        out["rate"][cq_id] = float(rate_raw)
                    except ValueError:
                        pass
                miss_raw = (row.get("missing_axiom_ids")
                            or row.get("Missing_axiom_ids") or "").strip()
                if miss_raw:
                    out["missing_axioms"][cq_id] = [
                        x.strip() for x in miss_raw.split(";") if x.strip()]
                tp_raw = (row.get("tp_axiom_ids")
                          or row.get("TP_axiom_ids") or "").strip()
                if tp_raw:
                    out["tp_axioms"][cq_id] = [
                        x.strip() for x in tp_raw.split(";") if x.strip()]
                n_raw = (row.get("n_axioms")
                         or row.get("N_axioms") or "").strip()
                if n_raw:
                    try:
                        out["n_axioms"][cq_id] = int(n_raw)
                    except ValueError:
                        pass
                n_tp_raw = (row.get("n_tp")
                            or row.get("N_tp") or "").strip()
                if n_tp_raw:
                    try:
                        out["n_tp"][cq_id] = int(n_tp_raw)
                    except ValueError:
                        pass
                if cq_id in out["any"] and cq_id not in out["rate"]:
                    pass
    except Exception as e:
        print(f"[warn] Could not parse strict_cq_csv: {e}", file=sys.stderr)
    return out


def _serialize_pairs(s: set) -> list:
    return [{"sub": sub, "sup": sup} for sub, sup in sorted(s)]


def build_json_output(result: dict, args: argparse.Namespace,
                      cq_closure: Optional[dict] = None) -> dict:
    g = result["gold_closure"]
    p = result["pred_closure"]
    cm = result["class_metrics"]
    pm = result["property_metrics"]
    om = result["combined_metrics"]

    config = {
        "gold_owl": args.gold_owl,
        "pred_owl": args.pred_owl,
        "class_csv": args.class_csv,
        "property_csv": args.property_csv,
        "reasoner": result.get("gold_reasoner", "HermiT (CLI)"),
    }

    results_list = [
        {
            "id": "gold_closure",
            "n_class_pairs": len(g["class_hierarchy"]),
            "n_property_pairs": len(g["property_hierarchy"]),
            "class_pairs": _serialize_pairs(g["class_hierarchy"]),
            "property_pairs": _serialize_pairs(g["property_hierarchy"]),
        },
        {
            "id": "pred_closure",
            "n_class_pairs": len(p["class_hierarchy"]),
            "n_property_pairs": len(p["property_hierarchy"]),
            "class_pairs": _serialize_pairs(p["class_hierarchy"]),
            "property_pairs": _serialize_pairs(p["property_hierarchy"]),
        },
        {
            "id": "translation",
            "n_class_translated": len(result["pred_class_translated"]),
            "n_property_translated": len(result["pred_prop_translated"]),
            "n_class_untranslated": len(result["untranslated_class"]),
            "n_property_untranslated": len(result["untranslated_prop"]),
            "class_translated": _serialize_pairs(result["pred_class_translated"]),
            "property_translated": _serialize_pairs(result["pred_prop_translated"]),
            "class_untranslated": _serialize_pairs(result["untranslated_class"]),
            "property_untranslated": _serialize_pairs(result["untranslated_prop"]),
        },
        {
            "id": "class_metrics",
            "tp": cm["n_tp"], "fp": cm["n_fp"], "fn": cm["n_fn"],
            "precision": round(cm["precision"], 4),
            "recall": round(cm["recall"], 4),
            "f1": round(cm["f1"], 4),
            "tp_pairs": _serialize_pairs(cm["tp"]),
            "fp_pairs": _serialize_pairs(cm["fp"]),
            "fn_pairs": _serialize_pairs(cm["fn"]),
        },
        {
            "id": "property_metrics",
            "tp": pm["n_tp"], "fp": pm["n_fp"], "fn": pm["n_fn"],
            "precision": round(pm["precision"], 4),
            "recall": round(pm["recall"], 4),
            "f1": round(pm["f1"], 4),
            "tp_pairs": _serialize_pairs(pm["tp"]),
            "fp_pairs": _serialize_pairs(pm["fp"]),
            "fn_pairs": _serialize_pairs(pm["fn"]),
        },
        {
            "id": "combined_metrics",
            "tp": om["n_tp"], "fp": om["n_fp"], "fn": om["n_fn"],
            "precision": round(om["precision"], 4),
            "recall": round(om["recall"], 4),
            "f1": round(om["f1"], 4),
        },
    ]

    if cq_closure is not None:
        results_list.append({
            "id": "cq_coverage_closure",
            "n_total": cq_closure["n_total"],
            "n_fully_covered": cq_closure["n_fully_covered"],
            "n_any_covered":   cq_closure["n_any_covered"],
            "fully_coverage":  round(cq_closure["fully_coverage"], 4),
            "any_coverage":    round(cq_closure["any_coverage"], 4),
            "average_rate":    round(cq_closure["average_rate"], 4),
            "n_covered": cq_closure["n_covered"],
            "coverage":  round(cq_closure["coverage"], 4),
            "per_cq": list(cq_closure["per_cq"].values()),
        })

    return {"config": config, "results": results_list}


def save_csv_output(result: dict, csv_path: str) -> None:

    rows = []
    cm = result["class_metrics"]
    pm = result["property_metrics"]

    for sub, sup in sorted(result["gold_closure"]["class_hierarchy"]):
        if (sub, sup) in cm["tp"]:
            status = "TP"
        else:
            status = "FN"
        rows.append({
            "side": "gold", "dimension": "class",
            "sub": sub, "sup": sup, "status": status,
            "raw_pred_sub": "", "raw_pred_sup": "",
        })

    for sub, sup in sorted(result["pred_class_translated"]):
        if (sub, sup) in cm["tp"]:
            continue
        if (sub, sup) in cm["fp"]:
            rows.append({
                "side": "pred", "dimension": "class",
                "sub": sub, "sup": sup, "status": "FP",
                "raw_pred_sub": "", "raw_pred_sup": "",
            })

    for sub, sup in sorted(result["untranslated_class"]):
        rows.append({
            "side": "pred", "dimension": "class",
            "sub": "", "sup": "", "status": "untranslated",
            "raw_pred_sub": sub, "raw_pred_sup": sup,
        })

    for sub, sup in sorted(result["gold_closure"]["property_hierarchy"]):
        if (sub, sup) in pm["tp"]:
            status = "TP"
        else:
            status = "FN"
        rows.append({
            "side": "gold", "dimension": "property",
            "sub": sub, "sup": sup, "status": status,
            "raw_pred_sub": "", "raw_pred_sup": "",
        })

    for sub, sup in sorted(result["pred_prop_translated"]):
        if (sub, sup) in pm["tp"]:
            continue
        if (sub, sup) in pm["fp"]:
            rows.append({
                "side": "pred", "dimension": "property",
                "sub": sub, "sup": sup, "status": "FP",
                "raw_pred_sub": "", "raw_pred_sup": "",
            })

    for sub, sup in sorted(result["untranslated_prop"]):
        rows.append({
            "side": "pred", "dimension": "property",
            "sub": "", "sup": "", "status": "untranslated",
            "raw_pred_sub": sub, "raw_pred_sup": sup,
        })

    fields = ["side", "dimension", "sub", "sup", "status",
              "raw_pred_sub", "raw_pred_sup"]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nHermiT entailment pairs CSV saved to: {csv_path}")


def build_md_report(result: dict, cq_closure: Optional[dict] = None) -> str:
    L = []

    gold_label_map = result.get("gold_closure", {}).get("name_to_label") or {}
    pred_label_map = (result.get("_pred_label_map")
                      or result.get("pred_closure", {}).get("name_to_label")
                      or {})

    gold_label_map_norm = {_norm(k): v for k, v in gold_label_map.items()}
    pred_label_map_norm = {_norm(k): v for k, v in pred_label_map.items()}

    def _fmt_gold(name: str) -> str:
        if name in gold_label_map:
            return gold_label_map[name]
        n = _norm(name)
        if n in gold_label_map_norm:
            return gold_label_map_norm[n]
        return name

    def _fmt_pred(name: str) -> str:
        if name in pred_label_map:
            return pred_label_map[name]
        n = _norm(name)
        if n in pred_label_map_norm:
            return pred_label_map_norm[n]
        return name

    L.append("# HermiT Closure Evaluation Report")
    L.append("")
    L.append("_Generated by `eval_hermit.py`_  ")
    L.append(f"_Reasoner: `{result.get('gold_reasoner', 'HermiT')}`_")
    L.append("")
    L.append(
    "This report evaluates the predicted ontology against the gold ontology "
    "at the hierarchy level, using HermiT to compute the deductive closure "
    "of `SubClassOf` and `SubPropertyOf` entailments."
)
    L.append("")
    L.append(
    "Both class and property hierarchies are considered: `EquivalentClasses` "
    "and `EquivalentProperties` are treated as bidirectional entailments. "
    "Predicted entailments are aligned to the gold vocabulary, and their "
    "intersection with gold entailments yields the final metrics."
)
    L.append("")

    g = result["gold_closure"]
    p = result["pred_closure"]
    L.append("## Closure sizes")
    L.append("")
    L.append("| Side | Class entailments | Property entailments |")
    L.append("|---|---:|---:|")
    L.append(f"| Gold | {len(g['class_hierarchy'])} | "
             f"{len(g['property_hierarchy'])} |")
    L.append(f"| Pred | {len(p['class_hierarchy'])} | "
             f"{len(p['property_hierarchy'])} |")
    L.append(f"| Pred translated | {len(result['pred_class_translated'])} | "
             f"{len(result['pred_prop_translated'])} |")
    L.append(f"| Pred untranslated | {len(result['untranslated_class'])} | "
             f"{len(result['untranslated_prop'])} |")
    L.append("")
    L.append("_Untranslated pred entailments (pred-side facts that "
             "couldn't be mapped to gold vocabulary) are counted as "
             "FP — they live outside the evaluator's vocabulary and "
             "are noise from gold's perspective._")
    L.append("")

    cm = result["class_metrics"]
    pm = result["property_metrics"]
    om = result["combined_metrics"]
    L.append("## Metrics")
    L.append("")
    L.append("| Dimension | TP | FP (incl. untranslated) | FN | "
             "Precision | Recall | F1 |")
    L.append("|---|---:|---:|---:|---:|---:|---:|")
    for label, m in [("Class hierarchy", cm),
                     ("Property hierarchy", pm),
                     ("Overall", om)]:
        if (m["n_tp"] + m["n_fp"] + m["n_fn"]) == 0:
            L.append(f"| {label} | — | — | — | — | — | — |")
        else:
            n_unt = m.get("n_untranslated_in_fp", 0)
            n_translated_fp = m["n_fp"] - n_unt
            if n_unt > 0:
                fp_disp = (f"{m['n_fp']} "
                           f"({n_translated_fp}+{n_unt} untranslated)")
            else:
                fp_disp = str(m["n_fp"])
            p_str = "—" if (m["n_tp"] + m["n_fp"]) == 0 else f"{m['precision']*100:.1f}%"
            r_str = "—" if (m["n_tp"] + m["n_fn"]) == 0 else f"{m['recall']*100:.1f}%"
            f_str = "—" if ((m["n_tp"] + m["n_fp"]) == 0 or (m["n_tp"] + m["n_fn"]) == 0) else f"{m['f1']*100:.1f}%"
            L.append(f"| {label} | {m['n_tp']} | {fp_disp} | "
                     f"{m['n_fn']} | {p_str} | {r_str} | {f_str} |")
    L.append("")

    gold_asserted_class = result["gold_closure"].get("asserted_class", set())
    gold_asserted_prop  = result["gold_closure"].get("asserted_prop", set())
    gold_derived_class_subjects = result["gold_closure"].get(
        "derived_class_subjects", set())
    gold_derived_prop_subjects  = result["gold_closure"].get(
        "derived_prop_subjects", set())

    pred_asserted_class = result["pred_closure"].get("asserted_class", set())
    pred_asserted_prop  = result["pred_closure"].get("asserted_prop", set())
    pred_derived_class_subjects = result["pred_closure"].get(
        "derived_class_subjects", set())
    pred_derived_prop_subjects  = result["pred_closure"].get(
        "derived_prop_subjects", set())

    class_pred_origin = result.get("_class_pred_origin", {})
    prop_pred_origin  = result.get("_prop_pred_origin", {})

    def _src_tag(pair, asserted_set, derived_subjects=None):

        if pair in asserted_set:
            return "[asserted]"
        return "[inferred]"

    def _gold_src_tag(gold_pair, asserted_set):

        if asserted_set is gold_asserted_class:
            return _src_tag(gold_pair, asserted_set,
                            gold_derived_class_subjects)
        if asserted_set is gold_asserted_prop:
            return _src_tag(gold_pair, asserted_set,
                            gold_derived_prop_subjects)
        if asserted_set is pred_asserted_class:
            return _src_tag(gold_pair, asserted_set,
                            pred_derived_class_subjects)
        if asserted_set is pred_asserted_prop:
            return _src_tag(gold_pair, asserted_set,
                            pred_derived_prop_subjects)
        return ("[asserted]" if gold_pair in asserted_set
                else "[inferred]")

    def _pred_origin_str(gold_pair, origin_map, asserted_set):

        pred_pairs = origin_map.get(gold_pair, [])
        if not pred_pairs:
            return ""

        if asserted_set is pred_asserted_class:
            derived = pred_derived_class_subjects
        elif asserted_set is pred_asserted_prop:
            derived = pred_derived_prop_subjects
        else:
            derived = set()
        bits = []
        for p_sub, p_sup in pred_pairs:
            tag = _src_tag((p_sub, p_sup), asserted_set, derived)
            if (p_sub, p_sup) == gold_pair:
                bits.append(tag)
            else:
                bits.append(f"from pred `{_fmt_pred(p_sub)}` ⊑ "
                            f"`{_fmt_pred(p_sup)}` {tag}")
        return "  — " + "; ".join(bits) if bits else ""

    if cm["tp"] or cm["fn"] or cm["fp"]:
        L.append("## Class hierarchy details")
        L.append("")
        L.append("Each entailment is tagged with how the source ontology "
                 "produced it: `[asserted]` = directly declared in the "
                 "OWL file (via `rdfs:subClassOf` or "
                 "`owl:equivalentClass`); `[inferred]` = "
                 "derived by HermiT through reasoning.")
        L.append("")

        if cm["tp"]:
            L.append(f"### TP — matched ({len(cm['tp'])})")
            L.append("")
            L.append("Each row: gold entailment `[gold-source]` — pred "
                     "entailment that translates to it `[pred-source]`.")
            L.append("")
            for s, x in sorted(cm["tp"]):
                gold_tag = _gold_src_tag((s, x), gold_asserted_class)
                pred_str = _pred_origin_str(
                    (s, x), class_pred_origin, pred_asserted_class)
                L.append(f"- `{_fmt_gold(s)}` ⊑ `{_fmt_gold(x)}` "
                         f"{gold_tag}{pred_str}")
            L.append("")

        if cm["fn"]:
            L.append(f"### FN — gold entailment missed by pred "
                     f"({len(cm['fn'])})")
            L.append("")
            L.append("Each row: gold entailment that pred could not "
                     "produce.")
            L.append("")
            for s, x in sorted(cm["fn"]):
                gold_tag = _gold_src_tag((s, x), gold_asserted_class)
                L.append(f"- `{_fmt_gold(s)}` ⊑ `{_fmt_gold(x)}` {gold_tag}")
            L.append("")

        if cm["fp"]:
            L.append(f"### FP — pred-only, gold doesn't entail "
                     f"({len(cm['fp'])})")
            L.append("")
            L.append("Each row: pred entailment (translated to gold "
                     "vocabulary) that gold does not entail. The "
                     "`gold says about <sub>` line shows what gold "
                     "actually wrote about the subject — useful for "
                     "spotting cases where pred used a simpler form "
                     "(e.g. atomic SubClassOf) than gold (e.g. "
                     "`A ⊑ ∃p.B`), which is structurally invalid.")
            L.append("")
            gold_by_sub = (cq_closure or {}).get(
                "gold_axioms_by_subject", {})
            for s, x in sorted(cm["fp"]):
                pred_str = _pred_origin_str(
                    (s, x), class_pred_origin, pred_asserted_class)
                if not pred_str:
                    pred_str = "  — (pred origin unknown)"
                L.append(f"- `{_fmt_gold(s)}` ⊑ `{_fmt_gold(x)}`{pred_str}")

                gold_axs = gold_by_sub.get(s, [])
                if gold_axs:

                    relevant = [ax for ax in gold_axs
                                if ax.get("axiom_type") != "Declaration"]
                    if relevant:
                        L.append(f"  &nbsp;&nbsp;gold says about "
                                 f"`{_fmt_gold(s)}`:")
                        for ax in relevant[:5]:  # cap at 5 per FP
                            L.append(f"    - `{ax.get('id')}`: "
                                     f"`{ax.get('dl', '')}`")
            L.append("")

    if pm["tp"] or pm["fn"] or pm["fp"]:
        L.append("## Property hierarchy details")
        L.append("")
        L.append("Each entailment is tagged with how the source ontology "
                 "produced it: `[asserted]` = directly declared in the "
                 "OWL file (via `rdfs:subPropertyOf` or "
                 "`owl:equivalentProperty`); `[inferred]` = "
                 "derived by HermiT through reasoning.")
        L.append("")

        if pm["tp"]:
            L.append(f"### TP — matched ({len(pm['tp'])})")
            L.append("")
            for s, x in sorted(pm["tp"]):
                gold_tag = _gold_src_tag((s, x), gold_asserted_prop)
                pred_str = _pred_origin_str(
                    (s, x), prop_pred_origin, pred_asserted_prop)
                L.append(f"- `{_fmt_gold(s)}` ⊑ `{_fmt_gold(x)}` "
                         f"{gold_tag}{pred_str}")
            L.append("")

        if pm["fn"]:
            L.append(f"### FN — gold entailment missed by pred "
                     f"({len(pm['fn'])})")
            L.append("")
            for s, x in sorted(pm["fn"]):
                gold_tag = _gold_src_tag((s, x), gold_asserted_prop)
                L.append(f"- `{_fmt_gold(s)}` ⊑ `{_fmt_gold(x)}` {gold_tag}")
            L.append("")

        if pm["fp"]:
            L.append(f"### FP — pred-only, gold doesn't entail "
                     f"({len(pm['fp'])})")
            L.append("")
            gold_by_sub = (cq_closure or {}).get(
                "gold_axioms_by_subject", {})
            for s, x in sorted(pm["fp"]):
                pred_str = _pred_origin_str(
                    (s, x), prop_pred_origin, pred_asserted_prop)
                if not pred_str:
                    pred_str = "  — (pred origin unknown)"
                L.append(f"- `{_fmt_gold(s)}` ⊑ `{_fmt_gold(x)}`{pred_str}")
                gold_axs = gold_by_sub.get(s, [])
                if gold_axs:
                    relevant = [ax for ax in gold_axs
                                if ax.get("axiom_type") != "Declaration"]
                    if relevant:
                        L.append(f"  &nbsp;&nbsp;gold says about "
                                 f"`{_fmt_gold(s)}`:")
                        for ax in relevant[:5]:
                            L.append(f"    - `{ax.get('id')}`: "
                                     f"`{ax.get('dl', '')}`")
            L.append("")

    if result["untranslated_class"] or result["untranslated_prop"]:
        L.append("## Untranslated pred pairs")
        L.append("")
        L.append("These pred-side entailments could not be translated to "
                 "gold vocabulary via the alignment tables. Each pair is "
                 "annotated with which side(s) failed lookup:")
        L.append("")
        L.append("- `[SUB]` sub-class is missing in alignment table")
        L.append("- `[SUP]` super-class is missing in alignment table")
        L.append("- `[BOTH]` neither name was found in alignment table")
        L.append("")

        inv_class = result.get("_inv_class_to_label", {})
        inv_prop = result.get("_inv_prop_to_label", {})
        pred_label_map = result.get("_pred_label_map", {})

        def _can_translate(name, inv_map):
            label = pred_label_map.get(name, name)
            split_form = _split_camel(name)
            variants = [name]
            for v in (label, split_form):
                if v and v not in variants:
                    variants.append(v)
            for v in list(variants):
                if v.lower() != v:
                    variants.append(v.lower())
            return any(v in inv_map for v in variants)

        def _classify(s, x, inv_map):
            sub_ok = _can_translate(s, inv_map)
            sup_ok = _can_translate(x, inv_map)
            if sub_ok and not sup_ok:
                return "[SUP]"
            if sup_ok and not sub_ok:
                return "[SUB]"
            return "[BOTH]"

        if result["untranslated_class"]:
            L.append("### Class entailments untranslated")
            L.append("")
            for s, x in sorted(result["untranslated_class"]):
                tag = _classify(s, x, inv_class)
                L.append(f"- `{tag}` `{s}` ⊑ `{x}`")
            L.append("")
        if result["untranslated_prop"]:
            L.append("### Property entailments untranslated")
            L.append("")
            for s, x in sorted(result["untranslated_prop"]):
                tag = _classify(s, x, inv_prop)
                L.append(f"- `{tag}` `{s}` ⊑ `{x}`")
            L.append("")

    if cq_closure is not None:
        L.append("## CQ Coverage (closure-based)")
        L.append("")
        L.append("A CQ is evaluated against pred's translated closure under "
             "three views:")
        L.append("1. **Fully covered:** all relevant gold-closure entailments "
             "are reproduced, or the CQ is fully covered in the strict "
             "axiom-level evaluation.")
        L.append("2. **At-least-one covered:** at least one relevant closure "
             "entailment is reproduced, or the CQ has at least one strict "
             "axiom-level match.")
        L.append("3. **Average rate:** the average per-CQ coverage rate. "
             "Each CQ uses its closure rate, or the higher strict "
             "axiom-level rate when available. An at-least-one strict "
             "match does not automatically count as 100%.")
        L.append("")

        n_strict_only = 0
        n_closure_new = 0
        n_both = 0
        for cq_id, info in cq_closure["per_cq"].items():
            src = info.get("source", "none")

            if src == "rescued-only":
                n_closure_new += 1
            elif src == "strict-only":
                n_strict_only += 1
            elif src == "strict + rescued":
                n_both += 1
            elif src == "closure-new":
                n_closure_new += 1
            elif src == "strict":
                n_strict_only += 1
            elif src == "both":
                n_both += 1

        n_total = cq_closure["n_total"]
        any_rescue_in_play = any(info.get("axiom_rescue")
                                 for info in cq_closure["per_cq"].values())
        if any_rescue_in_play:
            any_meaning = ("CQs where at least one gold axiom got TP "
                           "or was rescued by closure")
            avg_meaning = ("mean of each CQ's `(strict TPs + rescued) "
                           "/ total axioms`")
            fully_meaning = ("CQs where every gold axiom got TP or was "
                             "rescued by closure")
        else:
            any_meaning = "CQs where at least one gold axiom got TP"
            avg_meaning = "mean of each CQ's coverage %"
            fully_meaning = "CQs where every gold axiom got TP"

        L.append("### Overall CQ coverage rate")
        L.append("")
        L.append("| View | Value | Meaning |")
        L.append("|---|---:|---|")
        L.append(f"| Covered CQs (partial counts) | "
                 f"**{cq_closure['n_any_covered']}/{cq_closure['n_total']} = "
                 f"{cq_closure['any_coverage']*100:.1f}%** | "
                 f"{any_meaning} |")
        L.append(f"| Average per-CQ coverage | "
                 f"**{cq_closure['average_rate']*100:.1f}%** | "
                 f"{avg_meaning} |")
        L.append(f"| Fully (100%) covered CQs | "
                 f"**{cq_closure['n_fully_covered']}/{cq_closure['n_total']} = "
                 f"{cq_closure['fully_coverage']*100:.1f}%** | "
                 f"{fully_meaning} |")
        L.append("")




        gold_class_clos = result["gold_closure"]["class_hierarchy"]
        gold_prop_clos = result["gold_closure"]["property_hierarchy"]
        pred_class_trans = result.get("pred_class_translated", set())
        pred_prop_trans = result.get("pred_prop_translated", set())

        all_closure = (
            [("class", s, p) for (s, p) in sorted(gold_class_clos)]
            + [("property", s, p) for (s, p) in sorted(gold_prop_clos)]
        )
        per_cq = cq_closure.get("per_cq", {})
        ent_to_cqs: Dict[Tuple[str, str, str], list] = {}
        for cq_id, pcq in per_cq.items():
            pair_map: Dict[Tuple[str, str, str], list] = {}
            for rec in pcq.get("pair_axiom_records", []) or []:
                key = (rec["kind"], rec["sub"], rec["sup"])
                pair_map[key] = list(rec.get("axioms") or [])

            for e in pcq.get("matched_entailments", []):
                key = (e["kind"], e["sub"], e["sup"])
                ax_ids = pair_map.get(key, [])
                ent_to_cqs.setdefault(key, []).append((cq_id, ax_ids))
            for e in pcq.get("missing_entailments", []):
                key = (e["kind"], e["sub"], e["sup"])
                ax_ids = pair_map.get(key, [])
                ent_to_cqs.setdefault(key, []).append((cq_id, ax_ids))

        L.append("### Per-entailment Coverage Overview")
        L.append("")
        L.append("Every entailment HermiT derived from gold is listed "
                 "below. For each: did pred reproduce it, which CQs "
                 "consider it relevant, and which gold axiom is the "
                 "source.")
        L.append("")
        L.append("Only entailments coming from simple hierarchy axioms "
                 "(`A ⊑ B` or `p ⊑ q`) are tagged to a CQ here. "
                 "Entailments coming from complex axioms (with "
                 "cardinality, existential restrictions, etc.) appear "
                 "in the table without a CQ tag.")
        L.append("")
        n_total_e = len(all_closure)
        n_reproduced = sum(
            1 for (kind, s, p) in all_closure
            if (kind == "class" and (s, p) in pred_class_trans)
            or (kind == "property" and (s, p) in pred_prop_trans)
        )
        n_tagged = sum(1 for key in all_closure if key in ent_to_cqs)
        L.append(f"**{n_reproduced} / {n_total_e} closure entailments "
                 f"reproduced by pred.** "
                 f"{n_tagged} of {n_total_e} are tagged to at least one CQ.")
        L.append("")

        L.append("| Kind | Entailment by gold | Reproduced by pred | CQs | Source axiom(s) |")
        L.append("|---|---|:-:|---|---|")

        for (kind, sub, sup) in all_closure:
            if kind == "class":
                covered = "Y" if (sub, sup) in pred_class_trans else "N"
            else:
                covered = "Y" if (sub, sup) in pred_prop_trans else "N"

            tagged = ent_to_cqs.get((kind, sub, sup), [])
            tagged.sort(key=lambda x: x[0])

            ent_str = f"`{_fmt_gold(sub)} ⊑ {_fmt_gold(sup)}`"
            kind_label = "Class" if kind == "class" else "Property"

            if not tagged:
                cqs_cell = ""
                reason_cell = ("(transitive or complex axiom; "
                               "CQ tag not directly traceable)")
            else:
                cqs_cell = ", ".join(cq_id for cq_id, _ in tagged)
                parts = []
                for cq_id, ax_ids in tagged:
                    parts.append(f"{cq_id}: " + ", ".join(ax_ids))
                reason_cell = "; ".join(parts)

            L.append(f"| {kind_label} | {ent_str} | {covered} | "
                     f"{cqs_cell} | {reason_cell} |")
        L.append("")

        any_rescue_data = any(info.get("axiom_rescue")
                              for info in cq_closure["per_cq"].values())
        L.append("### Per-CQ coverage")
        L.append("")
        L.append("CQ coverage is computed at the axiom level:")
        L.append("")
        L.append("```")
        L.append("Coverage = (strict TPs + closure rescued) / total axioms")
        L.append("```")
        L.append("")
        L.append("The `Source` column indicates whether coverage comes from strict matching, closure recovery, or both:")
        L.append("")
        L.append("- `strict + rescued`: strict matching covers at least one axiom, and closure recovery adds at least one previously missed axiom")
        L.append("- `strict-only`: coverage comes only from strict matching; closure recovery did not add anything new")
        L.append("- `rescued-only`: coverage is obtained only through closure recovery")
        L.append("- empty: neither strict TPs nor closure rescue — "
                 "this CQ is uncovered")
        L.append("")
        L.append("Closure matches that correspond to already matched strict axioms are treated as confirmation and do not change the score.")
        L.append("")
        L.append("The `Closure-recovered axioms` column lists strict-missing axioms recovered by hierarchy closure. Recovery modes:")
        L.append("")
        L.append("- `pred wrote it`: pred has the exact axiom")
        L.append("- `pred reasoned via chain`: pred derived it through "
                 "a sub-class chain (path shown)")
        L.append("- `pred reasoned (other)`: pred derived it via more "
                 "complex reasoning (no simple chain found)")
        L.append("")
        L.append("The `Missing closure facts` column reports gold hierarchy entailments not reproduced by the predicted closure.")
        L.append("")
        L.append("| CQ id | Strict TP | Closure-recovered| Total | Coverage | "
                 "Source | Closure-recovered axioms | Missing closure facts |")
        L.append("|---|---:|---:|---:|---:|---|---|---|")
        src_label_map = {
            "strict-only": "strict-only",
            "strict + rescued": "strict + rescued",
            "rescued-only": "rescued-only",
            "strict": "strict",
            "closure-new": "closure-new",
            "both": "strict + closure",
            "none": "",
        }
        mode_glyph = {
            "direct_asserted": "pred wrote it",
            "simple_hierarchy_inferred": "pred reasoned via chain",
            "complex_inferred": "pred reasoned (other)",
            "uncovered": "pred missed it",
            "not_eligible": "not a simple hierarchy axiom",
        }
        for cq_id, info in cq_closure["per_cq"].items():
            tp = info.get("n_strict_tp")
            rescued = info.get("n_closure_rescued", 0)
            total = info.get("n_axioms_total")
            rate_disp = "—" if not info.get("n_axioms_total") else f"{info['rate']*100:.1f}%"
            src = src_label_map.get(info.get("source", "none"), "")

            rescued_lines = []
            for r in info.get("axiom_rescue", []):
                if r.get("rescued"):
                    sub = _fmt_gold(r.get("sub", ""))
                    sup = _fmt_gold(r.get("sup", ""))
                    line = (f"`{r['axiom_id']}`: `{sub} ⊑ {sup}`, "
                            f"{mode_glyph.get(r['mode'], r['mode'])}")
                    if r.get("path"):
                        ps = " then ".join(
                            f"`{_fmt_gold(e['sub'])}⊑{_fmt_gold(e['sup'])}`"
                            for e in r["path"])
                        line += f"<br>&nbsp;&nbsp;via: {ps}"
                    rescued_lines.append(line)
            rescued_cell = ("<br>".join(rescued_lines)
                            if rescued_lines else "")

            # Missing closure facts cell
            missing = info.get("missing_entailments", [])
            if missing:
                missing_strs = []
                for e in missing:
                    tag = "C" if e["kind"] == "class" else "P"
                    missing_strs.append(
                        f"[{tag}] `{_fmt_gold(e['sub'])} ⊑ "
                        f"{_fmt_gold(e['sup'])}`")
                missing_cell = "<br>".join(missing_strs)
            else:
                missing_cell = ""

            tp_disp = str(tp) if tp is not None else ""
            total_disp = str(total) if total is not None else ""
            rescued_disp = str(rescued) if total is not None else ""
            L.append(f"| {cq_id} | {tp_disp} | {rescued_disp} | "
                     f"{total_disp} | {rate_disp} | {src} | "
                     f"{rescued_cell} | {missing_cell} |")
        L.append("")

        if n_closure_new > 0:
            L.append(f"{n_closure_new} CQ(s) gained coverage via "
                     "closure reasoning (beyond strict axiom matching).")
            L.append("")

    return "\n".join(L)


def append_md_report(report_text: str, output_path: str) -> None:
    hermit_marker = "# HermiT Closure Evaluation Report"

    if not os.path.exists(output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f"\n[report] Note: '{output_path}' did not exist. Created a "
              f"new file containing ONLY the HermiT report. To get a "
              f"combined report, first run concept_label_matching.py / "
              f"eval_property.py / eval_triple.py with --save_report_md "
              f"pointing to the same file.")
        return

    with open(output_path, "r", encoding="utf-8") as f:
        existing = f.read()

    if hermit_marker in existing:
        idx = existing.find(hermit_marker)
        prefix = existing[:idx].rstrip()
        if prefix.endswith("---"):
            prefix = prefix[:-3].rstrip()
        new_text = prefix + "\n\n---\n\n" + report_text
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_text)
        print(f"\n[report] HermiT section already existed in "
              f"'{output_path}', replaced it with the new run.")
        return

    if not existing.endswith("\n"):
        existing += "\n"
    new_text = existing + "\n---\n\n" + report_text
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"\n[report] HermiT report appended to '{output_path}'.")


def get_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # Required: OWL files for HermiT
    p.add_argument("--gold_owl", required=True,
                   help="Gold OWL file (HermiT input)")
    p.add_argument("--pred_owl", required=True,
                   help="Pred OWL file (HermiT input)")
    p.add_argument("--class_csv", required=True,
                   help="Class alignment CSV (Gold_term,Pre_term,...)")
    p.add_argument("--property_csv", required=True,
                   help="Property alignment CSV (same format)")

    # Optional: gold/pred axioms for closure-based CQ coverage
    p.add_argument("--gold", default=None,
                   help="Gold axioms JSON (with cq_numbers). Required for "
                        "closure-based CQ coverage.")
    p.add_argument("--pred", default=None,
                   help="Pred axioms JSON (currently unused but accepted "
                        "for symmetry with eval_axioms.py).")
    p.add_argument("--cq_csv", default=None,
                   help="(optional) CQ table CSV; used if gold JSON has "
                        "no cq_definitions block.")
    p.add_argument("--strict_cq_csv", default=None,
                   help="(optional) Strict-coverage CQ results CSV from "
                        "eval_axioms.py. If provided, closure-based CQ "
                        "coverage will tag each CQ as strict / closure-new / "
                        "both. Expected columns: cq_id, covered.")

    # Outputs
    p.add_argument("--output_json", default=None,
                   help="Output JSON path: {config, results: [...]}")
    p.add_argument("--output_csv", default=None,
                   help="Output CSV path: one row per entailment pair")
    p.add_argument("--output_md", default=None,
                   help="Output Markdown path: HermiT report. Appended to "
                        "an existing MD file (e.g. label_matching_report.md) "
                        "if it exists.")
    p.add_argument("--output_txt", default=None,
                   help="(optional) Plain-text version of the MD report.")

    return p


def main():
    args = get_parser().parse_args()

    print(f"Loading class alignment from '{args.class_csv}'...",
          file=sys.stderr)
    class_align = load_alignment_csv(args.class_csv)
    print(f"  {len(class_align)} class pairs", file=sys.stderr)

    print(f"Loading property alignment from '{args.property_csv}'...",
          file=sys.stderr)
    prop_align = load_alignment_csv(args.property_csv)
    print(f"  {len(prop_align)} property pairs", file=sys.stderr)

    result = compute_hermit_evaluation(
        gold_owl_path=args.gold_owl,
        pred_owl_path=args.pred_owl,
        class_align=class_align,
        prop_align=prop_align,
    )

    cq_closure = None
    if args.gold:
        try:
            gold_axioms = load_axioms(args.gold)
            cq_defs = load_cq_definitions(args.gold)
            if not cq_defs and args.cq_csv:
                try:
                    cq_defs = []
                    with open(args.cq_csv, "r", encoding="utf-8",
                              newline="") as f:
                        for row in csv.DictReader(f):
                            cq_defs.append({
                                "id": row.get("ID") or row.get("id", ""),
                                "question": (row.get("Question")
                                             or row.get("question", "")),
                            })
                except Exception as e:
                    print(f"[warn] Could not load CQ CSV: {e}",
                          file=sys.stderr)

            if any(ax.get("cq_numbers") for ax in gold_axioms):
                strict_set = load_strict_covered_cqs(args.strict_cq_csv) \
                    if args.strict_cq_csv else None
                cq_closure = compute_cq_coverage_closure(
                    result, gold_axioms, cq_defs,
                    strict_covered_cqs=strict_set)
                print(f"\nClosure-based CQ coverage:", file=sys.stderr)
                print(f"  Fully covered:        "
                      f"{cq_closure['n_fully_covered']} / "
                      f"{cq_closure['n_total']} CQs "
                      f"({cq_closure['fully_coverage']*100:.1f}%)",
                      file=sys.stderr)
                print(f"  At-least-one covered: "
                      f"{cq_closure['n_any_covered']} / "
                      f"{cq_closure['n_total']} CQs "
                      f"({cq_closure['any_coverage']*100:.1f}%)",
                      file=sys.stderr)
                print(f"  Average rate:         "
                      f"{cq_closure['average_rate']*100:.1f}%",
                      file=sys.stderr)
        except Exception as e:
            print(f"[warn] CQ coverage skipped: {e}", file=sys.stderr)

    # ---- Save outputs ----
    if args.output_json:
        out = build_json_output(result, args, cq_closure=cq_closure)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"\nJSON output saved to: {args.output_json}")

    if args.output_csv:
        save_csv_output(result, args.output_csv)

    if args.output_md:
        report_text = build_md_report(result, cq_closure=cq_closure)
        append_md_report(report_text, args.output_md)

    if args.output_txt:

        report_text = build_md_report(result, cq_closure=cq_closure)

        plain = report_text.replace("**", "").replace("`", "")
        with open(args.output_txt, "w", encoding="utf-8") as f:
            f.write(plain)
        print(f"\nText report saved to: {args.output_txt}")

    cm = result["class_metrics"]
    pm = result["property_metrics"]
    print("\n===== HermiT EVALUATION SUMMARY =====")
    print(f"Class hierarchy:    TP={cm['n_tp']}  FP={cm['n_fp']}  "
          f"FN={cm['n_fn']}  P={cm['precision']*100:.1f}%  "
          f"R={cm['recall']*100:.1f}%  F1={cm['f1']*100:.1f}%")
    print(f"Property hierarchy: TP={pm['n_tp']}  FP={pm['n_fp']}  "
          f"FN={pm['n_fn']}  P={pm['precision']*100:.1f}%  "
          f"R={pm['recall']*100:.1f}%  F1={pm['f1']*100:.1f}%")


if __name__ == "__main__":
    main()

