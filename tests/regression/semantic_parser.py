from pathlib import Path
import tempfile, json
from pse_cli.semantic_parser import parse_text

checks=[]
def ck(name,ok,detail=''):
    checks.append((name,bool(ok),detail))

text=r'''% ignored: \PSELocator{NOPE}
\PSELocator{A1}
\PSEApparatusEntry{A1}{lemma}{A note with {nested {braces}} and \emph{markup}.}
\PSEStageDirection{
  Enter {quietly} with \emph{nested} markup.
}
\PSEParallelSegment{source}{s1}{A multiline
segment with {nested} content and \textit{markup}.}
\PSEParallelTranslationNote{a1}{A {nested} note.}
\begin{PSESpeech}{alpha}
Speech.
\end{PSESpeech}
'''
nodes,errs=parse_text(text,'content/test.tex')
ck('balanced_nested_no_errors',not errs,str(errs))
by=[n.name for n in nodes]
ck('comments_ignored','NOPE' not in repr(nodes),repr(nodes))
ck('semantic_commands_found',all(x in by for x in ['PSELocator','PSEApparatusEntry','PSEStageDirection','PSEParallelSegment','PSEParallelTranslationNote','PSESpeech']),by)
ap=next(n for n in nodes if n.name=='PSEApparatusEntry')
ck('nested_argument_preserved','nested {braces}' in ap.args[2],ap.args[2])
seg=next(n for n in nodes if n.name=='PSEParallelSegment')
ck('multiline_argument_preserved','multiline\nsegment' in seg.args[2],repr(seg.args[2]))
loc=next(n for n in nodes if n.name=='PSEStageDirection').loc
ck('source_location',loc.file=='content/test.tex' and loc.line==4 and loc.column==1,repr(loc))
mal='first\n\\PSEParallelSegment{source}{s1}{unclosed\n'
n2,e2=parse_text(mal,'content/bad.tex')
ck('malformed_reported',len(e2)==1,str(e2))
ck('malformed_location',e2 and e2[0].loc.line==2,repr(e2[0].loc if e2 else None))
print(json.dumps({'audit_kind':'semantic_parser','checks':[{'name':n,'pass':p,'detail':d} for n,p,d in checks],'passed':sum(p for _,p,_ in checks),'total':len(checks)},indent=2))
raise SystemExit(0 if all(p for _,p,_ in checks) else 1)
