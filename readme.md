Automates the boring stuff related to uploading new phrases with Memrise.

- English and Chinese pairs are stored in phrases.json
- Chinese TTS soundbytes are generated using the soundoftext API, downloaded, and saved
- new stuff is uploaded to memrise

The course format is copied from this course by DrewSSP:
https://www.memrise.com/course/758578/2500-chinese-sentences-with-audio/

This uses Selenium to automate firefox. I believe this to be more expedient than reversing Memrise's API, at the cost of being sphincter-clenchingly fragile.

# Usage

```
pip install -e requirements.txt
./sync.py
```

# Additional Requirements

- [geckodriver](https://github.com/mozilla/geckodriver/releases)
