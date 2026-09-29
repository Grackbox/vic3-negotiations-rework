"""Static checks for the Negotiations Rework mod. Run from the repository root: python tools/check_mod.py

Checks (no game files needed):
  1. braces are balanced and indentation follows brace depth (tabs) in the mod's own script files;
  2. every nr_ symbol used in script is defined (scripted effect / trigger / value, modifier, amendment,
     journal entry, event, variable, saved scope, localization key or a parameter value);
  3. every nr_ definition is used somewhere;
  4. names built from parameters (e.g. nr_devout_officials_$FORM$) exist for every value passed in;
  5. localization: UTF-8 BOM, English/Russian key parity, no duplicate keys, keys referenced from script exist.
Exit code 1 if anything is found. Use --fix-indent to rewrite indentation in place.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ('english', 'russian')
problems = []


def report(section, items):
    items = sorted(set(items))
    if items:
        problems.append(section)
        print(f'== {section}')
        for i in items:
            print(f'  {i}')


def own_script_files():
    """Script files written for the mod (copied vanilla files keep vanilla formatting)."""
    files = glob.glob('common/**/nr_*.txt', recursive=True) + glob.glob('events/nr_*.txt')
    return sorted(f.replace('\\', '/') for f in files)


def all_script_files():
    files = glob.glob('common/**/*.txt', recursive=True) + glob.glob('events/**/*.txt', recursive=True)
    return sorted(f.replace('\\', '/') for f in files)


def strip_comment(line):
    out, quoted = '', False
    for c in line:
        if c == '"':
            quoted = not quoted
        if c == '#' and not quoted:
            break
        out += c
    return out


# ---------- 1. braces and indentation ----------
def reindent(text):
    depth, out = 0, []
    for line in text.split('\n'):
        bom = '﻿' if line.startswith('﻿') else ''
        s = line.lstrip('﻿').strip()
        if not s:
            out.append('')
            continue
        code = strip_comment(s)
        ind = depth - (1 if code.startswith('}') else 0)
        out.append(bom + '\t' * max(ind, 0) + s)
        depth += code.count('{') - code.count('}')
    return '\n'.join(out), depth


fix = '--fix-indent' in sys.argv
bad_braces, bad_indent = [], []
for f in own_script_files():
    raw = open(f, encoding='utf-8').read()
    new, depth = reindent(raw)
    if depth != 0:
        bad_braces.append(f'{f}: depth {depth} at end of file')
    elif new != raw:
        if fix:
            open(f, 'w', encoding='utf-8', newline='').write(new)
        else:
            bad_indent.append(f)
report('unbalanced braces', bad_braces)
report('indentation differs from brace depth (run with --fix-indent)', bad_indent)

# ---------- collect definitions ----------
texts = {f: re.sub(r'#.*', '', open(f, encoding='utf-8-sig').read()) for f in all_script_files()}
defined = {}
for f, t in texts.items():
    for k in re.findall(r'^([A-Za-z0-9_.]+)\s*=', t, re.M):
        defined.setdefault(k, f)

known = set(defined)
for t in texts.values():
    known |= set(re.findall(r'namespace\s*=\s*([a-z0-9_]+)', t))
    known |= set(re.findall(r'save_(?:temporary_)?scope_as\s*=\s*([a-z0-9_]+)', t))
    known |= set(re.findall(r'(?:set_variable|remove_variable|has_variable|change_variable|add_to_variable_list|is_target_in_variable_list|remove_list_variable)\s*=\s*\{?\s*(?:name\s*=\s*)?([a-z0-9_$]+)', t))
    known |= set(re.findall(r'var:([a-z0-9_]+)', t))
    known |= set(re.findall(r'\b[A-Z]+\s*=\s*([a-z0-9_]+)', t))  # parameter values: KEY = nr_devout_softbribe

loc = {lang: {} for lang in LANGS}
for lang in LANGS:
    for f in sorted(glob.glob(f'localization/{lang}/*.yml')):
        for line in open(f, encoding='utf-8-sig'):
            m = re.match(r'\s+([A-Za-z0-9_.]+):\d*\s', line)
            if m:
                loc[lang].setdefault(m.group(1), []).append(f.replace('\\', '/'))
known |= set(loc['english'])

# ---------- 2. used but not defined ----------
undefined = []
for f, t in texts.items():
    body = re.sub(r'^([A-Za-z0-9_.]+)\s*=', '', t, flags=re.M)
    for tok in re.findall(r'(?<![\w.$])(nr_[a-z0-9_]+(?:\.[0-9]+)?)(?![\w$])', body):
        if tok in known or re.fullmatch(r'nr_[a-z_]+\.\d+', tok) and tok in defined:
            continue
        undefined.append(f'{tok}  ({f})')
report('used but not defined', undefined)

# ---------- 3. defined but never used ----------
alltext = '\n'.join(texts.values()) + '\n'.join(open(f, encoding='utf-8-sig').read() for f in glob.glob('localization/english/*.yml'))
param_prefixes = set(re.findall(r'\b([a-z0-9_]+?)_?\$[A-Z]+\$', alltext))
unused = []
for k, f in defined.items():
    if not k.startswith(('nr_', 'je_nr', 'amendment_nr', 'concept_nr')):
        continue
    if any(d in f for d in ('events/', 'on_actions', 'journal_entries', 'amendments', 'game_concepts')):
        continue  # used by the engine or through the database, not by name in script
    if len(re.findall(r'\b' + re.escape(k) + r'\b', alltext)) > 1:
        continue
    if any(p and k.startswith(p) for p in param_prefixes):
        continue  # reached through a $PARAM$ name
    if re.search(r'\$[A-Z]+\$_' + re.escape(k.split('_')[-1]) + r'\b', alltext):
        continue
    unused.append(f'{k}  ({f})')
report('defined but never used', unused)

# ---------- 4. names built from parameters ----------
param_defs = {}  # scripted effect/trigger name -> body
for f, t in texts.items():
    if 'scripted_effects' in f or 'scripted_triggers' in f:
        for m in re.finditer(r'^([a-z0-9_]+)\s*=\s*\{(.*?)^\}', t, re.M | re.S):
            if '$' in m.group(2):
                param_defs[m.group(1)] = m.group(2)
missing_built = []
for name, body in param_defs.items():
    templates = set(re.findall(r'[a-z0-9_]*\$[A-Z]+\$[a-z0-9_]*', body))
    templates = {tpl for tpl in templates if re.search(r'[a-z]', tpl)}  # skip bare $PARAM$ values
    # variables created by the helper itself are not definitions to look up
    templates -= set(re.findall(r'(?:has_variable|remove_variable|set_variable)\s*=\s*(?:\{\s*name\s*=\s*)?([a-z0-9_]*\$[A-Z]+\$[a-z0-9_]*)', body))
    if not templates:
        continue
    for f, t in texts.items():
        for call in re.finditer(r'\b' + re.escape(name) + r'\s*=\s*\{([^{}]*)\}', t):
            args = dict(re.findall(r'\b([A-Z]+)\s*=\s*([A-Za-z0-9_.$]+)', call.group(1)))
            if any('$' in v for v in args.values()):
                continue  # passed through from another parameterized call
            for tpl in templates:
                built = re.sub(r'\$([A-Z]+)\$', lambda m: args.get(m.group(1), m.group(0)), tpl)
                if '$' in built:
                    continue
                if built not in defined and built not in known:
                    missing_built.append(f'{built}  (from {name} in {f})')
report('names built from parameters that do not exist', missing_built)

# ---------- 5. localization ----------
no_bom = [f.replace('\\', '/') for lang in LANGS for f in glob.glob(f'localization/{lang}/*.yml')
          if not open(f, 'rb').read(3) == b'\xef\xbb\xbf']
report('localization files without UTF-8 BOM', no_bom)
report('keys only in English', set(loc['english']) - set(loc['russian']))
report('keys only in Russian', set(loc['russian']) - set(loc['english']))
dups = [f'{k} ({", ".join(v)})' for lang in LANGS for k, v in loc[lang].items() if len(v) > 1]
report('duplicate localization keys', dups)

need, variables = set(), set()
for f, t in texts.items():
    variables |= set(re.findall(r'(?:set_variable|remove_variable|add_to_variable_list)\s*=\s*\{?\s*(?:name\s*=\s*)?([a-z0-9_]+)', t))
    for pat in (r'custom_tooltip\s*=\s*([a-z0-9_.]+)', r'\btext\s*=\s*([a-z0-9_.]+)',
                r'\b(?:name|title|desc|flavor)\s*=\s*"?([a-z0-9_.]+)"?', r'type\s*=\s*(je_nr[a-z0-9_]+)'):
        need |= {k for k in re.findall(pat, t) if k.startswith(('nr_', 'je_nr', 'amendment_nr'))}
    if any(d in f for d in ('static_modifiers', 'amendments', 'journal_entries', 'game_concepts')):
        need |= {k for k in re.findall(r'^([a-z0-9_]+)\s*=\s*\{', t, re.M) if k.startswith(('nr_', 'je_nr', 'amendment_nr', 'concept_nr'))}
missing_loc = [k for k in need if k not in loc['english'] and k not in variables and '$' not in k and not k.endswith('_')]
report('referenced from script but missing in localization', missing_loc)

if problems:
    print(f'\n{len(problems)} check(s) failed.')
    sys.exit(1)
print('All checks passed.')
