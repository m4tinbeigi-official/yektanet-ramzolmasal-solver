import xml.etree.ElementTree as ET
import re

tree = ET.parse('/Users/ricksabchez/workspace/sargijeh.svg')
root = tree.getroot()

grid = {}
for elem in root.iter():
    transform = elem.attrib.get('transform', '')
    m = re.search(r'translate\(([\d\.]+),\s*([\d\.]+)\)(?:\s*rotate\(([-\d\.]+)\))?', transform)
    if m:
        x = float(m.group(1))
        y = float(m.group(2))
        rot = float(m.group(3)) if m.group(3) else 0.0
        lines = elem.findall('{http://www.w3.org/2000/svg}line')
        has_bar = any(l.attrib.get('x1') == '-34' and l.attrib.get('x2') == '-34' for l in lines)
        gx = int(round((x - 110.0) / 100.0))
        gy = int(round((y - 110.0) / 100.0))
        grid[(gx, gy)] = {'type': 'arrow', 'rot': int(rot) % 360, 'bar': has_bar}
    elif elem.tag.endswith('circle'):
        cx = float(elem.attrib.get('cx', 0))
        cy = float(elem.attrib.get('cy', 0))
        gx = int(round((cx - 110.0) / 100.0))
        gy = int(round((cy - 110.0) / 100.0))
        grid[(gx, gy)] = {'type': 'circle'}

for y in range(23):
    row_data = []
    for x in range(12):
        node = grid.get((x, y))
        if not node:
            row_data.append(" ")
        elif node['type'] == 'circle':
            row_data.append("C")
        else:
            rot = node['rot']
            # rot // 90 gives 0, 1, 2, 3 (2 bits: 00, 01, 10, 11)
            val = rot // 90
            row_data.append(str(val))
    print(f"Row {y:2d}: {' '.join(row_data)}")
