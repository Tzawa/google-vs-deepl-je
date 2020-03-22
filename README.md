# google-vs-deepl-je

```sh
pipenv install
pipenv run python eval.py devtest.en-ja.google devtest.ja -l ja
pipenv run python eval.py devtest.en-ja.deepl devtest.ja -l ja
pipenv run python eval.py devtest.ja-en.google devtest.en -l en
pipenv run python eval.py devtest.ja-en.deepl devtest.en -l en
```

Ja -> En (as of March 22, 2020)
|DATA|Google|DeepL|
| ------------- | ------------- | ------------- |
|ASPEC (devtest)|**24.030**|20.431|
|JParaCrawl|25.819|**26.833**|

En -> Ja (as of March 22, 2020)
|DATA|Google|DeepL|
| ------------- | ------------- | ------------- |
|ASPEC (devtest)|28.554|**36.244**|
|JParaCrawl|25.554|**27.048**|
