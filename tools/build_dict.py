#!/usr/bin/env python3
"""입력 허용 사전(dict.js) 생성.

출처: hunspell-dict-ko (국립국어원 표준국어대사전/한국어기초사전/우리말샘 기반, CC BY-SA / GPL-3)
규칙: 명사 + 순수 한글 음절 + 기본 자모 완전 분해 시 정확히 5자모. 500개 정답 단어는 항상 포함.
사용: python3 tools/build_dict.py [dict-ko-data.yaml 경로]   (생략 시 GitHub에서 내려받음)
"""
import re, sys, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from jamo import decompose

ROOT = Path(__file__).resolve().parent.parent
URL = "https://raw.githubusercontent.com/spellcheck-ko/hunspell-dict-ko/master/dict-ko-data.yaml"
NOUN_POS = {"명사", "관·명"}
ALPHABET = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ"   # → a..x 로 압축 저장

def load_entries(src):
    text = Path(src).read_text(encoding="utf-8") if src else urllib.request.urlopen(URL, timeout=60).read().decode("utf-8")
    pos = None
    for line in text.splitlines():
        if line.startswith("- pos:"):
            pos = line.split(":", 1)[1].strip()
        elif line.startswith("  word:"):
            yield pos, line.split(":", 1)[1].strip()

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else None
    jamo_set = set()
    for pos, word in load_entries(src):
        d = decompose(word)
        if pos in NOUN_POS and d and len(d) == 5:
            jamo_set.add(d)
    n_dict = len(jamo_set)

    answers = []
    for l in (ROOT / "assets/한글_5자모_단어.txt").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*\d+\.\s*(\S+)\s*=\s*(.+)$", l)
        if m:
            answers.append((m.group(1), m.group(2).replace(" ", "")))
    missing = [(w, j) for w, j in answers if j not in jamo_set]
    jamo_set.update(j for _, j in answers)          # 정답은 반드시 입력 가능해야 함

    enc = {ch: chr(ord("a") + i) for i, ch in enumerate(ALPHABET)}
    packed = " ".join("".join(enc[c] for c in j) for j in sorted(jamo_set))
    (ROOT / "dict.js").write_text(
        "// 자동 생성 파일 (tools/build_dict.py). 출처: hunspell-dict-ko, CC BY-SA / GPL-3\n"
        f"const DICT_ALPHABET = {ALPHABET!r};\nconst DICT_PACKED = {packed!r};\n", encoding="utf-8")
    print(f"사전 명사(5자모): {n_dict}개 / 정답 중 사전에 없던 단어: {len(missing)}개 / 최종 허용: {len(jamo_set)}개")
    for w, j in missing:
        print("  사전에 없음:", w, j)

if __name__ == "__main__":
    main()
