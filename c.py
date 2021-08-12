import argparse

import sys
print(sys.getdefaultencoding())

parser = argparse.ArgumentParser()
parser.add_argument('body', type=str)
args = parser.parse_args()

body = args.body
ref = 'あいうえお'

sys.stdout.buffer.write((body + '\n').encode('utf-8'))

print(f'Input(sys.argv[1]): {body}')
print(f'Reference: {ref}')
assert body == ref
