#!/usr/bin/env python3
"""Export canonical Agent Skills to common host discovery folders.

This copies source only. It does not install skills or prove host runtime support.
"""
from pathlib import Path
import argparse, shutil, sys
ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    "codex": ".agents/skills",
    "claude": ".claude/skills",
    "copilot": ".github/skills",
    "gemini": ".gemini/skills",
    "cursor": ".cursor/skills",
}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--target', choices=[*TARGETS, 'all'], default='all')
    ap.add_argument('--out', default=str(ROOT/'exports'))
    ap.add_argument('--overwrite', action='store_true')
    args=ap.parse_args()
    src=ROOT/'skills'; out=Path(args.out).resolve()
    if not src.is_dir():
        print('ERROR: canonical skills/ directory missing',file=sys.stderr); return 2
    targets=TARGETS if args.target=='all' else {args.target:TARGETS[args.target]}
    for name, rel in targets.items():
        dest=out/name/rel
        dest.mkdir(parents=True,exist_ok=True)
        for skill_dir in sorted(src.iterdir()):
            if not skill_dir.is_dir() or not (skill_dir/'SKILL.md').is_file():
                continue
            target=dest/skill_dir.name
            if target.exists():
                if not args.overwrite:
                    print(f'SKIP existing: {target} (use --overwrite)')
                    continue
                shutil.rmtree(target)
            shutil.copytree(skill_dir,target)
        print(f'EXPORTED {name}: {dest}')
    print('NOTE: export is a folder-layout adapter, not an install or runtime test.')
    return 0
if __name__=='__main__': raise SystemExit(main())
