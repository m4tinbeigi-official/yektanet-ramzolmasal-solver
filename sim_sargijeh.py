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

# Rot to (dx, dy)
# 0 -> right (1, 0)
# 90 -> down (0, 1)
# 180 -> left (-1, 0)
# 270 -> up (0, -1)
def rot_to_dir(r):
    if r == 0: return (1, 0)
    if r == 90: return (0, 1)
    if r == 180: return (-1, 0)
    if r == 270: return (0, -1)
    return (0, 0)

# Let's test tracking paths for all possible rotation offsets (0, +90, -90, 180)
for rot_offset in [0, 90, 270, 180]:
    # find starting points (e.g. (0,0) or nodes with bar)
    start_candidates = [(0, 0), (11, 22), (0, 22), (11, 0)] + [k for k, v in grid.items() if v.get('bar')]
    for start in start_candidates:
        if start not in grid or grid[start]['type'] != 'arrow': continue
        visited = set()
        curr = start
        path = []
        circles_hit = []
        step = 0
        while curr in grid and curr not in visited and step < 300:
            visited.add(curr)
            node = grid[curr]
            if node['type'] == 'circle':
                circles_hit.append((curr, step))
                break
            
            r = (node['rot'] + rot_offset) % 360
            dx, dy = rot_to_dir(r)
            next_pos = (curr[0] + dx, curr[1] + dy)
            path.append((curr, r, next_pos))
            curr = next_pos
            step += 1
            if curr in grid and grid[curr]['type'] == 'circle':
                circles_hit.append((curr, step))
                # maybe continue in same direction?
                curr = (curr[0] + dx, curr[1] + dy)

        if len(visited) > 10:
            print(f"Offset {rot_offset} from {start}: visited {len(visited)} nodes, circles hit: {len(circles_hit)}")
