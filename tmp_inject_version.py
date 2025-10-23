import json, pathlib
rel=pathlib.Path('releases/1.0.0/examples/contracts')
changed=[]
for p in sorted(rel.glob('*.annotated.json')):
    data=json.loads(p.read_text('utf-8'))
    if 'version' not in data:
        data['version']='1.0.0'
        s=json.dumps(data, ensure_ascii=False, indent=2)+chr(10)
        p.write_text(s, encoding='utf-8')
        changed.append(p.name)
print('updated', len(changed), 'files:', ', '.join(changed))
