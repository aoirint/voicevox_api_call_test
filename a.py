import requests
import json

query = '''
{
  "accent_phrases": [
    {
      "moras": [
        {
          "text": "コ",
          "consonant": "k",
          "vowel": "o",
          "pitch": 5.671706676483154
        },
        {
          "text": "ン",
          "consonant": null,
          "vowel": "N",
          "pitch": 5.811046600341797
        },
        {
          "text": "ニ",
          "consonant": "n",
          "vowel": "i",
          "pitch": 5.925144672393799
        },
        {
          "text": "チ",
          "consonant": "ch",
          "vowel": "i",
          "pitch": 5.822493076324463
        },
        {
          "text": "ワ",
          "consonant": "w",
          "vowel": "a",
          "pitch": 5.713477611541748
        }
      ],
      "accent": 5,
      "pause_mora": null
    }
  ],
  "speedScale": 1,
  "pitchScale": 0,
  "intonationScale": 1
}
'''

headers = {
    'Content-Type': 'application/json',
    'Accept': 'audio/wav',
}

r = requests.post('http://127.0.0.1:50021/synthesis?speaker=1', headers=headers, data=query.encode('utf-8'))
print(r.status_code)

if r.status_code == 200:
    with open('w.wav', 'wb') as fp:
        fp.write(r.content)
else:
    raise Exception(r.text)

