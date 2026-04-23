#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = ROOT / 'templates' / 'base-survey-template.html'
SCHEMA_MARKER = 'const surveySchema ='
FORM_MARKER = 'const form = document.getElementById'


def load_json(path_str):
    return json.loads(Path(path_str).read_text(encoding='utf-8'))


def render_html_from_schema(schema, template_text):
    start = template_text.find(SCHEMA_MARKER)
    if start == -1:
        raise ValueError('Template missing surveySchema marker.')
    end = template_text.find(FORM_MARKER, start)
    if end == -1:
        raise ValueError('Template missing form marker after surveySchema.')
    schema_js = 'const surveySchema = ' + json.dumps(schema, ensure_ascii=False, indent=2) + ';\n\n    '
    return template_text[:start] + schema_js + template_text[end:]


def main():
    parser = argparse.ArgumentParser(description='Render self-contained survey HTML from a frozen schema.')
    parser.add_argument('--schema', required=True, help='Path to schema JSON')
    parser.add_argument('--out', required=True, help='Output HTML path')
    parser.add_argument('--template', default=str(DEFAULT_TEMPLATE), help='Optional HTML template path')
    args = parser.parse_args()

    try:
        schema = load_json(args.schema)
        template_text = Path(args.template).read_text(encoding='utf-8')
        html = render_html_from_schema(schema, template_text)
        Path(args.out).write_text(html, encoding='utf-8')
        print(args.out)
    except FileNotFoundError as e:
        print(f'File not found: {e}', file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f'Invalid JSON: {e}', file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
