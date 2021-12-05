import requests
import json
from typing import Any, Dict
from urllib.parse import urljoin

def audio_query(engine_url: str, text: str, speaker: int) -> Dict[str, Any]:
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

def synthesis(engine_url: str, query: Dict[str, Any], speaker: int) -> bytes:
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

def synthesis_morphing(engine_url: str, query: Dict[str, Any], base_speaker: int, target_speaker: int, morph_rate: float) -> bytes:
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'audio/wav',
    }

    params = {
        'base_speaker': base_speaker,
        'target_speaker': target_speaker,
        'morph_rate': morph_rate,
    }

    r = requests.post(urljoin(engine_url, 'synthesis_morphing'), headers=headers, params=params, data=json.dumps(query).encode('utf-8'))

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
    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_synthesis = subparsers.add_parser('synthesis')
    parser_synthesis.add_argument('-t', '--text', type=str, required=True)
    parser_synthesis.add_argument('-s', '--speaker', type=int, required=True)
    parser_synthesis.add_argument('--engine-url', type=str, default=os.environ.get('VOICEVOX_ENGINE_URL', 'http://127.0.0.1:50021'))

    parser_morphing = subparsers.add_parser('morphing')
    parser_morphing.add_argument('-t', '--text', type=str, required=True)
    parser_morphing.add_argument('-s', '--base-speaker', type=int, required=True)
    parser_morphing.add_argument('-ts', '--target-speaker', type=int, required=True)
    parser_morphing.add_argument('-mr', '--morph-rate', type=float, required=True)
    parser_morphing.add_argument('--engine-url', type=str, default=os.environ.get('VOICEVOX_ENGINE_URL', 'http://127.0.0.1:50021'))

    args = parser.parse_args()

    if args.subparser_name == 'synthesis':
        text = args.text
        speaker = args.speaker
        engine_url = args.engine_url
        filename = dt.now().strftime('%Y%m%d_%H%M%S')

        query = audio_query(engine_url, text, speaker)

        binary = synthesis(engine_url, query, speaker)

        with open(f'{filename}.wav', 'wb') as fp:
            fp.write(binary)

    elif args.subparser_name == 'morphing':
        text = args.text
        base_speaker = args.base_speaker
        target_speaker = args.target_speaker
        morph_rate = args.morph_rate
        engine_url = args.engine_url
        filename = dt.now().strftime('%Y%m%d_%H%M%S')

        query = audio_query(engine_url, text, base_speaker)

        binary = synthesis_morphing(engine_url, query, base_speaker, target_speaker, morph_rate)

        with open(f'{filename}.wav', 'wb') as fp:
            fp.write(binary)

    else:
        parser.print_help()
