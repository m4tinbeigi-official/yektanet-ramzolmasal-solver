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
    row_circles = [x for x in range(12) if grid.get((x, y), {}).get('type') == 'circle']
    row_bars = [x for x in range(12) if grid.get((x, y), {}).get('bar')]
    row_arrows = [(x, grid.get((x, y), {}).get('rot')) for x in range(12) if grid.get((x, y), {}).get('type') == 'arrow']
    print(f"Row {y:2d}: circles={row_circles}, bars={row_bars}")
