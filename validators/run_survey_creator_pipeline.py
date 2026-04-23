#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from contextlib import contextmanager

from auto_repair_survey_schema import auto_repair_schema
from render_survey_html import render_html_from_schema, DEFAULT_TEMPLATE
from validate_survey_schema import validate_survey_schema
from validate_survey_html_runtime import validate_html_runtime
from validate_survey_html_e2e import validate_html_e2e
from validate_survey_html_interaction_e2e import validate_html_interaction_e2e
from validate_survey_html_accessibility import validate_html_accessibility
from auto_repair_survey_html import auto_repair_html
from generate_sample_payload import generate_payload
from validate_survey_payload import validate_survey_payload
from validate_payload_against_schema import validate_payload_against_schema


def load_json(path_str):
    return json.loads(Path(path_str).read_text(encoding="utf-8"))


def summarize(report):
    return {
        "valid": report.get("valid", False),
        "error_count": len(report.get("errors", [])),
        "warning_count": len(report.get("warnings", [])),
    }


def warning_counts_by_severity(warnings):
    counts = {"high": 0, "medium": 0, "low": 0}
    for item in warnings or []:
        severity = item.get("severity", "medium")
        counts[severity] = counts.get(severity, 0) + 1
    return counts


def collect_manual_review_items(report, section_name):
    items = []
    if not report:
        return items
    for warning in report.get("warnings", []):
        item = {
            "section": section_name,
            "path": warning.get("path"),
            "message": warning.get("message"),
            "severity": warning.get("severity", "warning"),
        }
        if warning.get("code"):
            item["code"] = warning["code"]
        if warning.get("suggestion"):
            item["suggestion"] = warning["suggestion"]
        items.append(item)
    return items


def syntax_to_report(syntax):
    valid = syntax.get("valid", False)
    errors = []
    if not valid:
        errors.append({
            "path": "html.syntax",
            "message": syntax.get("error") or "Embedded HTML script syntax check failed.",
        })
    return {
        "valid": valid,
        "errors": errors,
        "warnings": [],
        "supported": syntax.get("supported", False),
    }


def compute_release_decision(full_report, fail_on_high_warning=False):
    blocked_reasons = []
    manual_review_required = []

    schema_report = full_report.get("schema")
    html_report = full_report.get("html")
    html_syntax_report = full_report.get("htmlSyntax")
    html_e2e_report = full_report.get("htmlE2E")
    html_interaction_e2e_report = full_report.get("htmlInteractionE2E")
    html_accessibility_report = full_report.get("htmlAccessibility")
    payload_report = full_report.get("payload")
    payload_against_schema_report = full_report.get("payloadAgainstSchema")
    schema_summary = full_report.get("summary", {}).get("schema", {})
    schema_warning_severity = schema_summary.get("warning_severity", {"high": 0, "medium": 0, "low": 0})

    if schema_report and not schema_report.get("valid", False):
        blocked_reasons.append({
            "type": "schema-invalid",
            "message": "Schema validation failed.",
            "details": schema_report.get("errors", []),
        })
    if html_report and not html_report.get("valid", False):
        blocked_reasons.append({
            "type": "html-runtime-invalid",
            "message": "HTML runtime validation failed.",
            "details": html_report.get("errors", []),
        })
    if html_syntax_report and not html_syntax_report.get("valid", False):
        blocked_reasons.append({
            "type": "html-js-syntax-invalid",
            "message": "Embedded JavaScript syntax check failed.",
            "details": html_syntax_report.get("errors", []),
        })
    if html_e2e_report and not html_e2e_report.get("valid", False):
        blocked_reasons.append({
            "type": "html-e2e-invalid",
            "message": "Browser smoke test failed; rendered page may be blank or broken.",
            "details": html_e2e_report.get("errors", []),
        })
    if html_interaction_e2e_report and not html_interaction_e2e_report.get("valid", False):
        blocked_reasons.append({
            "type": "html-interaction-e2e-invalid",
            "message": "Browser interaction test failed; rendered page may not be fillable or submittable.",
            "details": html_interaction_e2e_report.get("errors", []),
        })
    if html_accessibility_report and not html_accessibility_report.get("valid", False):
        blocked_reasons.append({
            "type": "html-accessibility-invalid",
            "message": "Accessibility validation failed; rendered page may have unlabeled controls or invalid form semantics.",
            "details": html_accessibility_report.get("errors", []),
        })
    if payload_report and not payload_report.get("valid", False):
        blocked_reasons.append({
            "type": "payload-invalid",
            "message": "Payload validation failed.",
            "details": payload_report.get("errors", []),
        })
    if payload_against_schema_report and not payload_against_schema_report.get("valid", False):
        blocked_reasons.append({
            "type": "payload-schema-mismatch",
            "message": "Payload does not match the concrete schema ids/types/value constraints.",
            "details": payload_against_schema_report.get("errors", []),
        })
    if fail_on_high_warning and schema_warning_severity.get("high", 0) > 0:
        blocked_reasons.append({
            "type": "high-schema-warning",
            "message": "High severity schema warnings remain after repair.",
            "details": [w for w in (schema_report or {}).get("warnings", []) if w.get("severity") == "high"],
        })

    if schema_warning_severity.get("medium", 0) > 0:
        manual_review_required.extend([
            {**item, "reviewReason": "medium-schema-warning"}
            for item in collect_manual_review_items(schema_report, "schema")
            if item.get("severity") == "medium"
        ])
    if schema_warning_severity.get("low", 0) > 0:
        manual_review_required.extend([
            {**item, "reviewReason": "low-schema-warning"}
            for item in collect_manual_review_items(schema_report, "schema")
            if item.get("severity") == "low"
        ])

    if html_report and html_report.get("warnings"):
        manual_review_required.extend([
            {**item, "reviewReason": "html-runtime-warning"}
            for item in collect_manual_review_items(html_report, "html")
        ])
    if html_e2e_report and html_e2e_report.get("warnings"):
        manual_review_required.extend([
            {**item, "reviewReason": "html-e2e-warning"}
            for item in collect_manual_review_items(html_e2e_report, "htmlE2E")
        ])
    if html_interaction_e2e_report and html_interaction_e2e_report.get("warnings"):
        manual_review_required.extend([
            {**item, "reviewReason": "html-interaction-e2e-warning"}
            for item in collect_manual_review_items(html_interaction_e2e_report, "htmlInteractionE2E")
        ])
    if html_accessibility_report and html_accessibility_report.get("warnings"):
        manual_review_required.extend([
            {**item, "reviewReason": "html-accessibility-warning"}
            for item in collect_manual_review_items(html_accessibility_report, "htmlAccessibility")
        ])

    if payload_report and payload_report.get("warnings"):
        manual_review_required.extend([
            {**item, "reviewReason": "payload-warning"}
            for item in collect_manual_review_items(payload_report, "payload")
        ])
    if payload_against_schema_report and payload_against_schema_report.get("warnings"):
        manual_review_required.extend([
            {**item, "reviewReason": "payload-schema-warning"}
            for item in collect_manual_review_items(payload_against_schema_report, "payloadAgainstSchema")
        ])

    ship_ready = len(blocked_reasons) == 0
    release_decision = {
        "shipReady": ship_ready,
        "manualReviewRequired": manual_review_required,
        "blockedReasons": blocked_reasons,
        "manualReviewCount": len(manual_review_required),
        "blockedReasonCount": len(blocked_reasons),
    }
    return release_decision


def print_section(name, report):
    status = "✅ PASS" if report.get("valid") else "❌ FAIL"
    print(f"\n[{name}] {status}")
    if report.get("errors"):
        print("Errors:")
        for i, item in enumerate(report["errors"], start=1):
            print(f"  {i}. [{item['path']}] {item['message']}")
    if report.get("warnings"):
        print("Warnings:")
        for i, item in enumerate(report["warnings"], start=1):
            severity = item.get("severity", "medium").upper()
            code = item.get("code")
            code_text = f" [{code}]" if code else ""
            print(f"  {i}. [{severity}]{code_text} [{item['path']}] {item['message']}")


@contextmanager
def tempfile_html_file(html):
    with NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_path = Path(tmp.name)
    try:
        yield tmp_path
    finally:
        tmp_path.unlink(missing_ok=True)


def resolve_output_paths(schema_path, output_dir, prefix=None):
    schema_file = Path(schema_path)
    stem = prefix or schema_file.stem
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return {
        "schema": str(out_dir / f"{stem}.repaired.schema.json"),
        "html": str(out_dir / f"{stem}.html"),
        "payload": str(out_dir / f"{stem}.payload.json"),
        "report": str(out_dir / f"{stem}.pipeline-report.json"),
    }


def run_pipeline(schema, template_text, auto_repair=False, fail_on_high_warning=False):
    full_report = {
        "valid": True,
        "schema": None,
        "html": None,
        "htmlSyntax": None,
        "htmlE2E": None,
        "htmlInteractionE2E": None,
        "htmlAccessibility": None,
        "htmlRepair": None,
        "payload": None,
        "payloadAgainstSchema": None,
        "repair": None,
        "summary": {},
    }

    working_schema = schema

    if auto_repair:
        repair_report = auto_repair_schema(schema)
        full_report["repair"] = {k: v for k, v in repair_report.items() if k != "schema"}
        working_schema = repair_report["schema"]

    schema_report = validate_survey_schema(working_schema)
    full_report["schema"] = schema_report
    full_report["summary"]["schema"] = summarize(schema_report)
    full_report["summary"]["schema"]["warning_severity"] = warning_counts_by_severity(schema_report.get("warnings", []))
    full_report["valid"] = full_report["valid"] and schema_report.get("valid", False)

    if fail_on_high_warning and full_report["summary"]["schema"]["warning_severity"].get("high", 0) > 0:
        full_report["valid"] = False
        full_report["blockedBy"] = "high-schema-warning"
        full_report["releaseDecision"] = compute_release_decision(full_report, fail_on_high_warning=fail_on_high_warning)
        return full_report, working_schema, None, None

    if not schema_report.get("valid", False):
        full_report["releaseDecision"] = compute_release_decision(full_report, fail_on_high_warning=fail_on_high_warning)
        return full_report, working_schema, None, None

    html = render_html_from_schema(working_schema, template_text)
    html_repair_report = auto_repair_html(html)
    full_report["htmlRepair"] = {k: v for k, v in html_repair_report.items() if k != "html"}
    html = html_repair_report["html"]

    final_html_validation = html_repair_report["finalValidation"]
    html_syntax_report = syntax_to_report(final_html_validation.get("syntax", {}))
    full_report["htmlSyntax"] = html_syntax_report
    full_report["summary"]["htmlSyntax"] = summarize(html_syntax_report)
    full_report["valid"] = full_report["valid"] and html_syntax_report.get("valid", False)

    html_report = final_html_validation.get("runtime") or validate_html_runtime(html)
    full_report["html"] = html_report
    full_report["summary"]["html"] = summarize(html_report)
    full_report["valid"] = full_report["valid"] and html_report.get("valid", False)

    html_e2e_report = final_html_validation.get("e2e")
    html_interaction_e2e_report = final_html_validation.get("interactionE2E")
    html_accessibility_report = final_html_validation.get("accessibility")
    if html_e2e_report is None or html_interaction_e2e_report is None or html_accessibility_report is None:
        with tempfile_html_file(html) as temp_html_path:
            if html_e2e_report is None:
                html_e2e_report = validate_html_e2e(temp_html_path)
            if html_interaction_e2e_report is None:
                html_interaction_e2e_report = validate_html_interaction_e2e(temp_html_path)
            if html_accessibility_report is None:
                html_accessibility_report = validate_html_accessibility(temp_html_path)
    full_report["htmlE2E"] = html_e2e_report
    full_report["summary"]["htmlE2E"] = summarize(html_e2e_report)
    full_report["valid"] = full_report["valid"] and html_e2e_report.get("valid", False)
    full_report["htmlInteractionE2E"] = html_interaction_e2e_report
    full_report["summary"]["htmlInteractionE2E"] = summarize(html_interaction_e2e_report)
    full_report["valid"] = full_report["valid"] and html_interaction_e2e_report.get("valid", False)

    full_report["htmlAccessibility"] = html_accessibility_report
    full_report["summary"]["htmlAccessibility"] = summarize(html_accessibility_report)
    full_report["valid"] = full_report["valid"] and html_accessibility_report.get("valid", False)

    payload = generate_payload(working_schema)
    payload_report = validate_survey_payload(payload)
    payload_report["generated"] = True
    full_report["payload"] = payload_report
    full_report["summary"]["payload"] = summarize(payload_report)
    full_report["valid"] = full_report["valid"] and payload_report.get("valid", False)

    payload_schema_report = validate_payload_against_schema(working_schema, payload)
    payload_schema_report["generated"] = True
    full_report["payloadAgainstSchema"] = payload_schema_report
    full_report["summary"]["payloadAgainstSchema"] = summarize(payload_schema_report)
    full_report["valid"] = full_report["valid"] and payload_schema_report.get("valid", False)
    full_report["releaseDecision"] = compute_release_decision(full_report, fail_on_high_warning=fail_on_high_warning)

    return full_report, working_schema, html, payload


def main():
    parser = argparse.ArgumentParser(description="Unified schema -> repair -> html -> payload pipeline for survey-creator-skill.")
    parser.add_argument("--schema", required=True, help="Path to source schema JSON")
    parser.add_argument("--output-dir", required=True, help="Directory for repaired schema, html, payload, and report")
    parser.add_argument("--prefix", help="Optional output file prefix; defaults to source schema filename stem")
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE), help="Optional HTML template path")
    parser.add_argument("--auto-repair", action="store_true", help="Attempt safe semantic auto-repairs before rendering")
    parser.add_argument("--fail-on-high-warning", action="store_true", help="Fail if schema still contains high severity warnings")
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    args = parser.parse_args()

    try:
        schema = load_json(args.schema)
        template_text = Path(args.template).read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"Failed to read input: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    outputs = resolve_output_paths(args.schema, args.output_dir, prefix=args.prefix)
    report, repaired_schema, html, payload = run_pipeline(
        schema,
        template_text,
        auto_repair=args.auto_repair,
        fail_on_high_warning=args.fail_on_high_warning,
    )

    Path(outputs["schema"]).write_text(json.dumps(repaired_schema, ensure_ascii=False, indent=2), encoding="utf-8")
    if html is not None:
        Path(outputs["html"]).write_text(html, encoding="utf-8")
    if payload is not None:
        Path(outputs["payload"]).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    final_report = {
        **report,
        "output": outputs,
    }
    Path(outputs["report"]).write_text(json.dumps(final_report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(final_report, ensure_ascii=False, indent=2))
    else:
        print("✅ SURVEY CREATOR PIPELINE PASS" if final_report["valid"] else "❌ SURVEY CREATOR PIPELINE FAIL")
        if final_report.get("releaseDecision") is not None:
            decision = final_report["releaseDecision"]
            print("\n[RELEASE DECISION]")
            print(f"Ship ready: {'YES' if decision.get('shipReady') else 'NO'}")
            print(f"Blocked reasons: {decision.get('blockedReasonCount', 0)}")
            print(f"Manual review items: {decision.get('manualReviewCount', 0)}")
        if final_report["repair"] is not None:
            print("\n[REPAIR]")
            print(f"Stopped reason: {final_report['repair'].get('stoppedReason')}")
            print(f"Applied fixes: {len(final_report['repair'].get('appliedFixes', []))}")
        if final_report["htmlRepair"] is not None:
            print("\n[HTML REPAIR]")
            print(f"Stopped reason: {final_report['htmlRepair'].get('stoppedReason')}")
            print(f"Applied fixes: {len(final_report['htmlRepair'].get('appliedFixes', []))}")
        if final_report["schema"] is not None:
            print_section("SCHEMA", final_report["schema"])
        if final_report["htmlSyntax"] is not None:
            print_section("HTML SYNTAX", final_report["htmlSyntax"])
        if final_report["html"] is not None:
            print_section("HTML", final_report["html"])
        if final_report["htmlE2E"] is not None:
            print_section("HTML E2E", final_report["htmlE2E"])
        if final_report["htmlInteractionE2E"] is not None:
            print_section("HTML INTERACTION E2E", final_report["htmlInteractionE2E"])
        if final_report.get("htmlAccessibility") is not None:
            print_section("HTML ACCESSIBILITY", final_report["htmlAccessibility"])
        if final_report["payload"] is not None:
            print_section("PAYLOAD", final_report["payload"])
        if final_report.get("payloadAgainstSchema") is not None:
            print_section("PAYLOAD AGAINST SCHEMA", final_report["payloadAgainstSchema"])
        print("\nOutput:")
        for key, value in outputs.items():
            print(f"- {key}: {value}")

    sys.exit(0 if final_report["valid"] else 1)


if __name__ == "__main__":
    main()
