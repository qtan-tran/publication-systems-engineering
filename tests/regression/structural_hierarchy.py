from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy()
ENV["PYTHONPATH"]=str(ROOT/"tools")+os.pathsep+ENV.get("PYTHONPATH","")
CLI=[sys.executable,"-m","pse_cli.cli"]

EXPECTED={
    "academic-monograph":("required",True),
    "edited-collection":("required",True),
    "basic-book":("required",True),
    "scholarly-edition":("recommended",True),
    "critical-edition":("recommended",True),
    "bilingual-edition":("recommended",True),
    "drama":("discouraged",False),
    "poetry":("discouraged",False),
    "literary-fiction":("discouraged",False),
}

def run(args, expect=0, timeout=180):
    p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\nstdout:\n{p.stdout[-4000:]}\nstderr:\n{p.stderr[-4000:]}")
    return p

def main():
    checks=[]
    module=json.loads((ROOT/"modules/structural-hierarchy/module.json").read_text())
    checks.append(("module_registered",module["id"]=="structural-hierarchy","manifest"))
    sty=(ROOT/"modules/structural-hierarchy/pse-module-structural-hierarchy.sty").read_text()
    checks.append(("four_level_contract",r"\newcommand{\PSESectionDepthLimit}{4}" in sty,"depth=4"))
    checks.append(("no_silent_flatten",r"\PackageError" in sty and r"\subparagraph" in sty,"TeX guard"))
    for pid,(status,default) in EXPECTED.items():
        data=json.loads((ROOT/"profiles"/pid/"profile.json").read_text())
        rule=data["module_policy"].get("structural-hierarchy",{})
        checks.append((f"{pid}_policy",rule.get("status")==status and rule.get("default_enabled") is default,str(rule)))
    with tempfile.TemporaryDirectory(prefix="pse-structure-") as td:
        parent=Path(td)
        run(CLI+["new",str(parent),"--non-interactive","--profile","academic-monograph","--title","Hierarchy Test","--author","Synthetic Author","--language","en","--publication-year","2027","--slug","book"])
        project=parent/"book"
        chapter=project/"content/chapter-01.tex"
        chapter.write_text(r"""\chapter{Unit}
\section{One}
\subsection{Two}
\subsubsection{Three}
\paragraph{Four} Allowed run-in level.
""")
        run(CLI+["build",str(project)],timeout=240)
        checks.append(("depth_four_builds",(project/"build/book.pdf").is_file(),"PDF produced"))
        chapter.write_text(r"""\chapter{Unit}
\section{One}
\subsection{Two}
\subsubsection{Three}
\paragraph{Four}
\subparagraph{Five} This must fail.
""")
        p=subprocess.run(CLI+["build",str(project)],cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=90)
        msg=p.stdout+p.stderr
        checks.append(("depth_five_rejected",p.returncode!=0 and "four-level section contract" in msg,"source validation"))
        checks.append(("no_automatic_rewrite",r"\subparagraph{Five}" in chapter.read_text(),"source unchanged"))
    failed=[c for c in checks if not c[1]]
    print("Structural hierarchy regression")
    for n,ok,d in checks:
        print(("PASS" if ok else "FAIL"),n+":",d)
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0

if __name__=="__main__":
    raise SystemExit(main())
