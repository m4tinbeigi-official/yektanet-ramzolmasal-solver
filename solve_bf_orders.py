import xml.etree.ElementTree as ET
import itertools
import re

tree = ET.parse('/Users/ricksabchez/workspace/sargijeh.svg')
root = tree.getroot()

nodes = []
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
        nodes.append({'type': 'arrow', 'x': gx, 'y': gy, 'rot': int(rot) % 360, 'bar': has_bar})
    elif elem.tag.endswith('circle'):
        cx = float(elem.attrib.get('cx', 0))
        cy = float(elem.attrib.get('cy', 0))
        gx = int(round((cx - 110.0) / 100.0))
        gy = int(round((cy - 110.0) / 100.0))
        nodes.append({'type': 'circle', 'x': gx, 'y': gy, 'rot': 0, 'bar': False})

def run_bf(code):
    tape = [0] * 30000
    ptr = 0
    code_ptr = 0
    output = []
    
    stack = []
    brackets = {}
    for i, c in enumerate(code):
        if c == '[':
            stack.append(i)
        elif c == ']':
            if stack:
                start = stack.pop()
                brackets[start] = i
                brackets[i] = start
    if stack: # unbalanced
        return ""

    steps = 0
    while code_ptr < len(code) and steps < 2000000:
        cmd = code[code_ptr]
        if cmd == '>': ptr = (ptr + 1) % 30000
        elif cmd == '<': ptr = (ptr - 1) % 30000
        elif cmd == '+': tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-': tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.': output.append(chr(tape[ptr]))
        elif cmd == '[':
            if tape[ptr] == 0: code_ptr = brackets.get(code_ptr, len(code))
        elif cmd == ']':
            if tape[ptr] != 0: code_ptr = brackets.get(code_ptr, code_ptr)
        code_ptr += 1
        steps += 1
    return "".join(output)

# Try reading orders:
# 1. Column by column top-down (x=0..11, y=0..22)
# 2. Column by column bottom-up
# 3. Row by row rotated 90 CW (y=22..0, x=0..11)
# 4. Row by row rotated 90 CCW (y=0..22, x=11..0)

orders = {
    "col_ltr_td": sorted(nodes, key=lambda n: (n['x'], n['y'])),
    "col_rtl_td": sorted(nodes, key=lambda n: (-n['x'], n['y'])),
    "col_ltr_bu": sorted(nodes, key=lambda n: (n['x'], -n['y'])),
    "col_rtl_bu": sorted(nodes, key=lambda n: (-n['x'], -n['y'])),
    "row_rot_cw": sorted(nodes, key=lambda n: (22 - n['y'], n['x'])),
    "row_rot_ccw": sorted(nodes, key=lambda n: (n['y'], 11 - n['x'])),
}

arrow_symbols = ['>', '<', '+', '-']

for order_name, node_list in orders.items():
    for p in itertools.permutations(arrow_symbols):
        for bar_map in [
            {90: '[', 270: ']'},
            {270: '[', 90: ']'},
            {0: '[', 180: ']'},
            {180: '[', 0: ']'},
        ]:
            code = []
            for n in node_list:
                if n['type'] == 'circle':
                    code.append('.')
                elif n['bar']:
                    code.append(bar_map.get(n['rot'], p[n['rot']//90]))
                else:
                    code.append(p[n['rot']//90])
            bf_code = "".join(code)
            res = run_bf(bf_code)
            if res and ("YEK" in res or "flag" in res or any(c.isascii() and c.isalnum() for c in res) and len(res) > 5):
                print(f"[{order_name}] Output ({p}, {bar_map}): {res}")

print("Rotated column search completed.")
