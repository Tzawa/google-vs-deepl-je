# google-vs-deepl-je

```sh
pipenv install
pipenv run python eval.py devtest.en-ja.google devtest.ja -l ja
pipenv run python eval.py devtest.en-ja.deepl devtest.ja -l ja
pipenv run python eval.py devtest.ja-en.google devtest.en -l en
pipenv run python eval.py devtest.ja-en.deepl devtest.en -l en
```
