import json, hashlib, pathlib
rel=pathlib.Path('releases/1.0.0')
manifest=json.loads((rel/'manifest.json').read_text('utf-8'))
files={e['path']:e for e in manifest['files']}
sha=lambda p: hashlib.sha256((rel/p).read_bytes()).hexdigest()
for p in ['CHANGES.md','release_manifest.json']:
    if p in files:
        files[p]['sha256']=sha(p)
s=json.dumps(manifest, indent=2)+chr(10)
(rel/'manifest.json').write_text(s, encoding='utf-8')
print('updated checksums for target files')
