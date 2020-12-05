## RPGM Kanji Dumping Script

This extremely simple program extracts dialogue events (Code 401) from RPG Maker MV and VX Ace games, given a path to the Data directory. Furigana-only words are skipped, and the rest are provided in decreasing order of frequency. It can also generate a txt-file that can directly be imported into Anki decks.

If the files are not json files and are encrypted (e.g. rvdata2), you will have to decrypt them first using some external tool.

This was made mostly for learning the vocabulary of games so that we may play them without the hassle of text hookers.

Requires Python 3.

### Dependencies:
* [nagisa](https://github.com/taishi-i/nagisa)

#### Example Usage:
	python rpgm_kanji_dump.py Data/ --verbose --out out.txt --skip --vxace --anki game_anki.txt --alimit 100
	
_Effect_: Strips out words from the Data/ directory while listing the files as they are processed. It stores the words, in descending order by frequency of occurrence, in out.txt, but skips the actual frequencies (which would otherwise be on the same line after a tab). It takes the first 100 of these and puts them in the game_anki.txt in the form of semi-colon separated fields.

**Anki format**[Two fields]: *word*;"*kana* \n *english_meaning*"
