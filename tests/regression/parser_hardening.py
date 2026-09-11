from __future__ import annotations

import json
import random
import string
import tempfile
from pathlib import Path
from pse_cli.semantic_parser import ParseLimits, parse_files, parse_text
from pse_cli.qa import Finding
from pse_cli.cli import _format_finding_line

checks=[]
def ck(name,ok,detail=''):
    checks.append((name,bool(ok),detail))

# Escaped-percent correctness: \% is literal; \\% begins a comment in TeX-like scanning.
text='\\PSEStageDirection{100\\% visible}\n\\PSELocator{A1}\n'
nodes,errs=parse_text(text,'content/percent.tex')
ck('escaped_percent_literal',not errs and nodes[0].args[0]=='100\\% visible',repr((nodes,errs)))

text2='\\\\% \\PSELocator{NOPE}\n\\PSELocator{A1}\n'
nodes2,errs2=parse_text(text2,'content/even-percent.tex')
ck('even_backslash_percent_comments',not errs2 and [n.args for n in nodes2 if n.name=='PSELocator']==[('A1',)],repr(nodes2))

unicode_text='αβγ\n\\PSEParallelSegment{source}{s1}{Καλημέρα — tiếng Việt — 日本語}\n'
unodes,uerrs=parse_text(unicode_text,'content/unicode.tex')
ck('unicode_preserved',not uerrs and 'Καλημέρα' in unodes[0].args[2],repr((unodes,uerrs)))
ck('unicode_location',unodes and unodes[0].loc.line==2 and unodes[0].loc.column==1,repr(unodes[0].loc if unodes else None))

# Depth limit must fail quickly and with a location.
deep='\\PSEStageDirection{' + ('{'*20) + 'x' + ('}'*20) + '}'
_,derr=parse_text(deep,'content/deep.tex',limits=ParseLimits(max_group_depth=8))
ck('depth_limit',derr and derr[0].code=='brace_depth_exceeded',repr([(e.code,e.loc) for e in derr]))

# Argument-size limit.
large='\\PSEStageDirection{' + ('x'*200) + '}'
_,lerr=parse_text(large,'content/large.tex',limits=ParseLimits(max_argument_chars=64))
ck('argument_size_limit',lerr and lerr[0].code=='argument_too_large',repr([(e.code,e.loc) for e in lerr]))

# Node-count limit.
many='\n'.join('\\PSELocator{A%d}'%i for i in range(20))
nn,nerr=parse_text(many,'content/many.tex',limits=ParseLimits(max_nodes_per_file=5))
ck('node_limit',len(nn)==5 and nerr and nerr[-1].code=='node_limit_exceeded',repr((len(nn),[(e.code,e.loc.line) for e in nerr])))


loc={"file":"content/play.tex","line":42,"column":7,"offset":1001}
finding=Finding("undefined_drama_speaker","error","Speech references an undeclared speaker.",location=loc).as_dict()
ck('finding_location_contract',finding.get('location')==loc,repr(finding))
ck('human_diagnostic_format',_format_finding_line(finding).startswith('content/play.tex:42:7: error: undefined_drama_speaker:'),_format_finding_line(finding))


with tempfile.TemporaryDirectory(prefix='pse-r-parser-') as td:
    root=Path(td)
    huge=root/'huge.tex'; huge.write_text('x'*128,encoding='utf-8')
    _,ferr=parse_files([huge],root,limits=ParseLimits(max_file_bytes=64))
    ck('file_size_limit',ferr and ferr[0].code=='file_too_large',repr([(e.code,e.loc) for e in ferr]))
    bad=root/'bad-utf8.tex'; bad.write_bytes(b'\xff\xfe\x00')
    _,u8err=parse_files([bad],root)
    ck('invalid_utf8_rejected',u8err and u8err[0].code=='invalid_utf8',repr([(e.code,e.loc) for e in u8err]))

# Deterministic lightweight fuzz: parser must terminate without unexpected exceptions.
rng=random.Random(1701)
alphabet=string.ascii_letters+string.digits+'{}\\% \nαé—'
fuzz_ok=True; fuzz_detail=''
for case in range(400):
    s=''.join(rng.choice(alphabet) for _ in range(rng.randrange(0,500)))
    if case%5==0:
        s+='\\PSEStageDirection{nested {text} '+str(case)+'}'
    try:
        parse_text(s,f'content/fuzz-{case}.tex',limits=ParseLimits(max_group_depth=32,max_argument_chars=2048,max_nodes_per_file=500,max_errors_per_file=50))
    except Exception as exc:
        fuzz_ok=False; fuzz_detail=f'case {case}: {type(exc).__name__}: {exc}'; break
ck('deterministic_fuzz_400_cases',fuzz_ok,fuzz_detail)

payload={'audit_kind':'parser_hardening','checks':[{'name':n,'pass':p,'detail':d} for n,p,d in checks],'passed':sum(p for _,p,_ in checks),'total':len(checks)}
print(json.dumps(payload,ensure_ascii=False,indent=2))
raise SystemExit(0 if all(p for _,p,_ in checks) else 1)
