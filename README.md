# 무한 단어맞추기

한글 자모 5개를 맞추는 Wordle 스타일 게임. `index.html`을 열면 실행됩니다.

## 사전 (dict.js)
입력 가능한 단어 사전은 [hunspell-dict-ko](https://github.com/spellcheck-ko/hunspell-dict-ko)의
단어 데이터(국립국어원 표준국어대사전·한국어기초사전·우리말샘 기반, CC BY-SA 4.0 / CC BY-SA 2.0 KR)에서
명사 중 자모 5개로 분해되는 단어만 뽑아 만든 파생물이며, 같은 조건(CC BY-SA)으로 제공됩니다.

재생성: `python3 tools/build_dict.py [dict-ko-data.yaml]`
