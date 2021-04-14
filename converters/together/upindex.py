import json

with open('../device/arista/x86_64-arista_7050_qx32/platform.json') as f:
    pf = json.load(f)

for ifx, v in pf['interfaces'].items():
    index = v['index']
    if ',' in index:
        a, _ = index.split(',', 1)
        bi = (int(a)-1)*4 + 1
        index = [bi, bi+1, bi+2, bi+3]
    else:
        bi = 96+(int(index)-25)+1
        index = [bi]
    v['index'] = ','.join(str(x) for x in index)

print(json.dumps(pf, sort_keys=True, indent=4))
