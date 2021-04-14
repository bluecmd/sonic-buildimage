import collections

props = collections.defaultdict(dict)

with open('a', 'r') as f:
    for l in f:
        l = l.strip()
        n, v = l.split('=', 1)
        pre, idn = n.rsplit('_', 1)
        idn, _ = idn.rsplit('.', 1)
        idn = int(idn)
        props[idn][pre] = v


print('# Arista requires the index order to be the same as the SFP port order')
print('# it seems, so the following xe* order will be a bit annoying to follow.')

for idn in sorted(props.keys()):
    pro = props[idn]
    breakout = False
    if idn <= 24:
        breakout = True
    bidn = 32 + (idn-1) * 3
    print()
    if breakout:
        print('# Port {xe%d, xe%d, xe%d, xe%d} [40G, 4x10G]' % (idn-1, bidn, bidn+1, bidn+2))
    else:
        print('# Port {xe%d} [40G only]' % (idn-1))
    for pk in sorted(pro.keys()):
        print('%s_%d.0=%s' % (pk, idn, pro[pk]))
        if not breakout:
            continue
        if pk == 'portmap':
            p = int(pro[pk].split(':', 1)[0])
            for i in range(3):
                print('portmap_%d.0=%d:10:i' % (bidn+i+1, p+i+1))
        elif pk == 'port_phy_addr':
            x = int(pro[pk], base=16)
            for i in range(3):
                print('port_phy_addr%d.0=%s' % (bidn+i+1, hex(x+i+1)))
        elif pk.startswith('port_') or pk.startswith('phy_'):
            for i in range(3):
                print('%s_%d.0=%s' % (pk, bidn+i+1, pro[pk]))


