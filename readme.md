## RPGM Kanji Dumping Script

This extremely simple program extracts dialogue events (Code 401) from RPG Maker MV and VX Ace games, given a path to the Data directory. Furigana-only words are skipped, and the rest are provided in decreasing order of frequency.

If the files are not json files and are encrypted (e.g. rvdata2), you will have to decrypt them first using some external tool.

This was made mostly for learning the vocabulary of games so that we may play them without the hassle of text hookers.

Requires Python 3.

### Dependencies:
* [nagisa](https://github.com/taishi-i/nagisa)

#### Example Usage:
	python rpgm_kanji_dump.py Data/ --verbose --out out.txt --skip --vxace