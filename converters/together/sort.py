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


for idn in sorted(props.keys()):
    pro = props[idn]
    breakout = False
    if idn <= 24:
        breakout = True
        idn = (idn-1)*4 + 1
    else:
        idn = 24*4 + idn - 24
    bidn = idn
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


