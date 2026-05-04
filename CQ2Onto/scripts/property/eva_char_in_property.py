import warnings
from typing import Optional
from rdflib import OWL

CHAR_URIS = {
    "Functional":        OWL.FunctionalProperty,
    "InverseFunctional": OWL.InverseFunctionalProperty,
    "Transitive":        OWL.TransitiveProperty,
    "Symmetric":         OWL.SymmetricProperty,
    "Asymmetric":        OWL.AsymmetricProperty,
    "Reflexive":         OWL.ReflexiveProperty,
    "Irreflexive":       OWL.IrreflexiveProperty,
}

MUTEX_PAIRS: list[tuple[str, str]] = [
    ("Symmetric", "Asymmetric"),
    ("Reflexive", "Irreflexive"),
]


def _build_mutex_map() -> dict[str, Optional[str]]:
    mm: dict[str, Optional[str]] = {}
    for a, b in MUTEX_PAIRS:
        mm[a] = b
        mm[b] = a
    for char in CHAR_URIS:
        mm.setdefault(char, None)
    return mm


def eval_characteristics(gold_props, pred_props, gold_to_pred_union) -> dict:
    mutex_map = _build_mutex_map()

    gold_lu = {p.label: p for p in gold_props}
    pred_lu = {p.label: p for p in pred_props}

    counts = {
        char: {"tp": 0, "fp": 0, "fn": 0, "details": []}
        for char in CHAR_URIS
    }

    n_evaluated = 0
    n_skipped   = 0

    gold_op_labels = {
        p.label for p in gold_props if p.prop_type == "ObjectProperty"
    }
    aligned_gold_labels: set[str] = set()

    for gold_lbl, pred_set in gold_to_pred_union.items():
        gold_rec = gold_lu.get(gold_lbl)
        if gold_rec is None:
            warnings.warn(
                f"[eval_characteristics] gold label {gold_lbl!r} from "
                f"alignment table not found in gold_props; skipping."
            )
            continue
        if gold_rec.prop_type != "ObjectProperty":
            continue
        if not pred_set:
            continue

        for pred_lbl in pred_set:
            pred_rec = pred_lu.get(pred_lbl)
            if pred_rec is None:
                warnings.warn(
                    f"[eval_characteristics] pred label {pred_lbl!r} "
                    f"(matched to gold {gold_lbl!r}) not found in "
                    f"pred_props; skipping this pair."
                )
                continue

            gold_chars = set(gold_rec.characteristics)
            pred_chars = set(pred_rec.characteristics)

            if not gold_chars and not pred_chars:
                n_skipped += 1
                aligned_gold_labels.add(gold_lbl)
                continue

            n_evaluated += 1
            aligned_gold_labels.add(gold_lbl)

            for char in CHAR_URIS:
                gold_has = char in gold_chars
                pred_has = char in pred_chars
                if not gold_has and not pred_has:
                    continue

                if gold_has and pred_has:
                    verdict = "tp"
                    counts[char]["tp"] += 1
                elif gold_has and not pred_has:
                    verdict = "fn"
                    counts[char]["fn"] += 1
                else:
                    verdict = "fp"
                    counts[char]["fp"] += 1

                counts[char]["details"].append({
                    "gold_prop":  gold_lbl,
                    "pred_prop":  pred_lbl,
                    "gold_chars": sorted(gold_chars),
                    "pred_chars": sorted(pred_chars),
                    "char":       char,
                    "verdict":    verdict,
                    "mutex_pair": mutex_map.get(char),
                })

    unaligned_gold_with_chars = []
    for p in gold_props:
        if p.prop_type != "ObjectProperty":
            continue
        if p.label in aligned_gold_labels:
            continue
        chars = sorted(set(p.characteristics))
        if chars:
            unaligned_gold_with_chars.append({
                "label":           p.label,
                "characteristics": chars,
            })

    def _metrics(tp: int, fp: int, fn: int):
        precision = tp / (tp + fp) if (tp + fp) > 0 else None
        recall    = tp / (tp + fn) if (tp + fn) > 0 else None
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision is not None and recall is not None
            and (precision + recall) > 0
            else None
        )
        return precision, recall, f1

    def _fmt(v):
        return f"{v:.3f}" if v is not None else "  N/A"

    print(f"\n  [characteristics, pair-level]  "
          f"evaluated_pairs={n_evaluated}  "
          f"skipped_pairs(both_empty)={n_skipped}  "
          f"unaligned_gold_with_chars={len(unaligned_gold_with_chars)}")
    print(f"\n  {'Characteristic':<22s}  "
          f"{'TP':>4}  {'FP':>4}  {'FN':>4}  "
          f"{'P':>6}  {'R':>6}  {'F1':>6}  "
          f"Mutex")
    print("  " + "─" * 70)

    result_per_char = {}
    agg_tp = agg_fp = agg_fn = 0

    for char in CHAR_URIS:
        tp = counts[char]["tp"]
        fp = counts[char]["fp"]
        fn = counts[char]["fn"]
        precision, recall, f1 = _metrics(tp, fp, fn)

        result_per_char[char] = {
            "tp":            tp,
            "fp":            fp,
            "fn":            fn,
            "precision":     round(precision, 4) if precision is not None else None,
            "recall":        round(recall,    4) if recall    is not None else None,
            "f1":            round(f1,        4) if f1        is not None else None,
            "mutex_partner": mutex_map.get(char),
            "details":       counts[char]["details"],
        }

        agg_tp += tp
        agg_fp += fp
        agg_fn += fn

        mutex_note = f"↔ {mutex_map[char]}" if mutex_map.get(char) else ""
        print(f"  {char:<22s}  "
              f"{tp:>4}  {fp:>4}  {fn:>4}  "
              f"{_fmt(precision):>6}  {_fmt(recall):>6}  {_fmt(f1):>6}  "
              f"{mutex_note}")

    agg_prec, agg_rec, agg_f1 = _metrics(agg_tp, agg_fp, agg_fn)
    print("  " + "─" * 70)
    print(f"  {'OVERALL (pair)':<22s}  "
          f"{agg_tp:>4}  {agg_fp:>4}  {agg_fn:>4}  "
          f"{_fmt(agg_prec):>6}  {_fmt(agg_rec):>6}  {_fmt(agg_f1):>6}")

    extra_fn_per_char: dict[str, int] = {char: 0 for char in CHAR_URIS}
    for entry in unaligned_gold_with_chars:
        for char in entry["characteristics"]:
            if char in extra_fn_per_char:
                extra_fn_per_char[char] += 1

    print(f"\n  [characteristics, ontology-level]  "
          f"gold_ObjectProperty_total={len(gold_op_labels)}  "
          f"aligned={len(aligned_gold_labels)}  "
          f"unaligned={len(gold_op_labels) - len(aligned_gold_labels)}")
    print(f"\n  {'Characteristic':<22s}  "
          f"{'TP':>4}  {'FP':>4}  {'FN':>4}  "
          f"{'P':>6}  {'R':>6}  {'F1':>6}")
    print("  " + "─" * 70)

    result_per_char_onto = {}
    agg_tp_o = agg_fp_o = agg_fn_o = 0

    for char in CHAR_URIS:
        tp = counts[char]["tp"]
        fp = counts[char]["fp"]
        fn = counts[char]["fn"] + extra_fn_per_char[char]
        precision, recall, f1 = _metrics(tp, fp, fn)

        result_per_char_onto[char] = {
            "tp":              tp,
            "fp":              fp,
            "fn":              fn,
            "fn_from_pairs":   counts[char]["fn"],
            "fn_from_unaligned": extra_fn_per_char[char],
            "precision":       round(precision, 4) if precision is not None else None,
            "recall":          round(recall,    4) if recall    is not None else None,
            "f1":              round(f1,        4) if f1        is not None else None,
            "mutex_partner":   mutex_map.get(char),
        }

        agg_tp_o += tp
        agg_fp_o += fp
        agg_fn_o += fn

        print(f"  {char:<22s}  "
              f"{tp:>4}  {fp:>4}  {fn:>4}  "
              f"{_fmt(precision):>6}  {_fmt(recall):>6}  {_fmt(f1):>6}")

    agg_prec_o, agg_rec_o, agg_f1_o = _metrics(agg_tp_o, agg_fp_o, agg_fn_o)
    print("  " + "─" * 70)
    print(f"  {'OVERALL (ontology)':<22s}  "
          f"{agg_tp_o:>4}  {agg_fp_o:>4}  {agg_fn_o:>4}  "
          f"{_fmt(agg_prec_o):>6}  {_fmt(agg_rec_o):>6}  {_fmt(agg_f1_o):>6}")

    return {
        "n_pairs_evaluated":  n_evaluated,
        "n_pairs_skipped":    n_skipped,
        "per_characteristic": result_per_char,
        "overall": {
            "tp":        agg_tp,
            "fp":        agg_fp,
            "fn":        agg_fn,
            "precision": round(agg_prec, 4) if agg_prec is not None else None,
            "recall":    round(agg_rec,  4) if agg_rec  is not None else None,
            "f1":        round(agg_f1,   4) if agg_f1   is not None else None,
        },
        "unaligned_gold_with_chars":   unaligned_gold_with_chars,
        "per_characteristic_ontology": result_per_char_onto,
        "overall_ontology": {
            "tp":        agg_tp_o,
            "fp":        agg_fp_o,
            "fn":        agg_fn_o,
            "precision": round(agg_prec_o, 4) if agg_prec_o is not None else None,
            "recall":    round(agg_rec_o,  4) if agg_rec_o  is not None else None,
            "f1":        round(agg_f1_o,   4) if agg_f1_o   is not None else None,
        },
    }