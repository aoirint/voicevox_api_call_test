import requests
import json
from typing import Any, Dict

def audio_query(speaker: int, text: str) -> Dict[str, Any]:
    headers = {
        'Content-Type': 'application/json',
    }
    
    params = {
        'speaker': speaker,
        'text': text,
    }

    r = requests.post('http://127.0.0.1:50021/audio_query', headers=headers, params=params)

    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()

def synthesis(speaker: int, query: Dict[str, Any]) -> bytes:
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'audio/wav',
    }

    params = {
        'speaker': speaker,
    }

    r = requests.post('http://127.0.0.1:50021/synthesis?speaker=1', headers=headers, data=json.dumps(query).encode('utf-8'))

    if r.status_code != 200:
        raise Exception(r.text)
    
    return r.content


if __name__ == '__main__':
    from datetime import datetime as dt
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('speaker', type=int)
    parser.add_argument('text', type=str)
    args = parser.parse_args()

    speaker = args.speaker
    text = args.text
    filename = dt.now().strftime('%Y%m%d_%H%M%S')

    query = audio_query(speaker, text)

    binary = synthesis(speaker, query)

    with open(f'{filename}.wav', 'wb') as fp:
        fp.write(binary)

