import requests
import json
from typing import Any, Dict
from urllib.parse import urljoin

def audio_query(engine_url: str, speaker: int, text: str) -> Dict[str, Any]:
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'speaker': speaker,
        'text': text,
    }

    r = requests.post(urljoin(engine_url, 'audio_query'), headers=headers, params=params)

    if r.status_code != 200:
        raise Exception(r.text)

    return r.json()

def synthesis(engine_url: str, speaker: int, query: Dict[str, Any]) -> bytes:
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'audio/wav',
    }

    params = {
        'speaker': speaker,
    }

    r = requests.post(urljoin(engine_url, 'synthesis'), headers=headers, params=params, data=json.dumps(query).encode('utf-8'))

    if r.status_code != 200:
        raise Exception(r.text)

    return r.content


if __name__ == '__main__':
    from datetime import datetime as dt

    from dotenv import load_dotenv
    load_dotenv()

    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('speaker', type=int)
    parser.add_argument('text', type=str)
    parser.add_argument('--engine-url', type=str, default=os.environ.get('VOICEVOX_ENGINE_URL', 'http://127.0.0.1:50021'))
    args = parser.parse_args()

    speaker = args.speaker
    text = args.text
    engine_url = args.engine_url
    filename = dt.now().strftime('%Y%m%d_%H%M%S')

    query = audio_query(engine_url, speaker, text)

    binary = synthesis(engine_url, speaker, query)

    with open(f'{filename}.wav', 'wb') as fp:
        fp.write(binary)
