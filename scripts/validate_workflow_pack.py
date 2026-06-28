#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "workflow" / "contract.json"
SOURCE_ID_PATTERN = re.compile(r"\bS\d+\b")
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\btvly-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\b"),
]


def load_contract():
    if not CONTRACT_PATH.exists():
        raise RuntimeError(f"missing contract: {CONTRACT_PATH}")
    with CONTRACT_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path):
    return path.read_text(encoding="utf-8")


def add(errors, message):
    errors.append(message)


def validate_required_files(pack_dir, contract, errors):
    for file_name in contract["required_files"]:
        if not (pack_dir / file_name).is_file():
            add(errors, f"{file_name}: required file is missing")


def validate_source_table(pack_dir, contract, errors):
    source_path = pack_dir / "02_source_table.csv"
    source_ids = set()
    credible_count = 0

    if not source_path.exists():
        return source_ids, credible_count

    with source_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != contract["source_table_headers"]:
            add(
                errors,
                "02_source_table.csv: header mismatch; expected "
                + ",".join(contract["source_table_headers"]),
            )
            return source_ids, credible_count

        for row_number, row in enumerate(reader, start=2):
            source_id = (row.get("source_id") or "").strip()
            tier = (row.get("reliability_tier") or "").strip()

            if not source_id:
                add(errors, f"02_source_table.csv:{row_number}: source_id is empty")
                continue
            if source_id in source_ids:
                add(errors, f"02_source_table.csv:{row_number}: duplicate source_id {source_id}")
            source_ids.add(source_id)

            if tier in contract["credible_source_tiers"]:
                credible_count += 1

    minimum = contract["minimum_credible_sources"]
    if credible_count < minimum:
        add(
            errors,
            f"02_source_table.csv: Credible A/B sources: {credible_count}; minimum required: {minimum}",
        )

    return source_ids, credible_count


def parse_sections(text, heading_regex):
    matches = list(re.finditer(heading_regex, text, flags=re.IGNORECASE | re.MULTILINE))
    sections = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(0).strip(), text[start:end]))
    return sections


def field_value(section, field_name):
    pattern = re.compile(rf"^{re.escape(field_name)}:[ \t]*(.*)$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(section)
    if not match:
        return None
    return match.group(1).strip()


def validate_claims_matrix(pack_dir, contract, source_ids, errors):
    claims_path = pack_dir / "03_claims_matrix.md"
    requiring_evidence = {status.lower() for status in contract["claim_statuses_requiring_evidence"]}
    checked_claims = 0

    if not claims_path.exists():
        return checked_claims

    text = read_text(claims_path)
    for fallback_index, (heading, section) in enumerate(
        parse_sections(text, r"^##\s+Claim\s+\d+.*$"), start=1
    ):
        claim_label = heading.lstrip("#").strip() or f"Claim {fallback_index}"
        status = field_value(section, "Status")
        evidence = field_value(section, "Evidence")

        if status and status.lower() in requiring_evidence:
            checked_claims += 1
            if not evidence:
                add(errors, f"03_claims_matrix.md: {claim_label} has status \"{status}\" but empty Evidence.")
                continue
            found_ids = SOURCE_ID_PATTERN.findall(evidence)
            if not found_ids:
                add(errors, f"03_claims_matrix.md: {claim_label} has no parseable source IDs in Evidence.")
                continue
            for source_id in found_ids:
                if source_id not in source_ids:
                    add(errors, f"03_claims_matrix.md: {claim_label} references unknown source id {source_id}.")

    return checked_claims


def validate_outline(pack_dir, source_ids, errors):
    outline_path = pack_dir / "04_ppt_outline.md"
    checked_slides = 0

    if not outline_path.exists():
        return checked_slides

    text = read_text(outline_path)
    for fallback_index, (heading, section) in enumerate(
        parse_sections(text, r"^##\s+Slide\s+\d+.*$"), start=1
    ):
        slide_label = heading.lstrip("#").strip() or f"Slide {fallback_index}"
        evidence = field_value(section, "Evidence source_ids")
        if not evidence:
            add(errors, f"04_ppt_outline.md: {slide_label} has empty Evidence source_ids.")
            continue
        checked_slides += 1
        found_ids = SOURCE_ID_PATTERN.findall(evidence)
        if not found_ids:
            add(errors, f"04_ppt_outline.md: {slide_label} has no parseable source IDs.")
            continue
        for source_id in found_ids:
            if source_id not in source_ids:
                add(errors, f"04_ppt_outline.md: {slide_label} references unknown source id {source_id}.")

    return checked_slides


def validate_ppt_master_input(pack_dir, contract, errors):
    input_path = pack_dir / "06_ppt_master_input.md"
    if not input_path.exists():
        return

    text = read_text(input_path).lower()
    required_phrases = [phrase.lower() for phrase in contract["ppt_master_input_required_phrases"]]
    if not any(phrase in text for phrase in required_phrases):
        add(
            errors,
            "06_ppt_master_input.md: missing instruction not to introduce unreviewed factual claims",
        )


def validate_no_obvious_secrets(pack_dir, errors):
    for path in pack_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".csv", ".txt", ".env", ".example", ".json"}:
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                add(errors, f"{path.relative_to(pack_dir)}: possible secret-looking token detected")
                break


def validate_pack(pack_dir, contract):
    errors = []
    validate_required_files(pack_dir, contract, errors)
    source_ids, credible_count = validate_source_table(pack_dir, contract, errors)
    checked_claims = validate_claims_matrix(pack_dir, contract, source_ids, errors)
    checked_slides = validate_outline(pack_dir, source_ids, errors)
    validate_ppt_master_input(pack_dir, contract, errors)
    validate_no_obvious_secrets(pack_dir, errors)

    return {
        "errors": errors,
        "required_files": len(contract["required_files"]),
        "credible_count": credible_count,
        "checked_claims": checked_claims,
        "checked_slides": checked_slides,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate an evidence-to-ppt workflow pack.")
    parser.add_argument("pack_dir", help="Directory containing workflow output files.")
    args = parser.parse_args(argv)

    pack_dir = Path(args.pack_dir).resolve()
    if not pack_dir.is_dir():
        print(f"ERROR: pack directory does not exist: {pack_dir}")
        return 2

    try:
        contract = load_contract()
        result = validate_pack(pack_dir, contract)
    except (OSError, RuntimeError, json.JSONDecodeError, csv.Error) as exc:
        print(f"ERROR: {exc}")
        return 2

    errors = result["errors"]
    if errors:
        print("FAIL workflow pack validation")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS workflow pack validation")
    print(f"Checked required files: {result['required_files']}")
    print(f"Credible A/B sources: {result['credible_count']}")
    print(f"Claims requiring evidence: {result['checked_claims']}")
    print(f"Slides with source bindings: {result['checked_slides']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
