import xml.etree.ElementTree as ET
import itertools

tree = ET.parse('/Users/ricksabchez/workspace/sargijeh.svg')
root = tree.getroot()

nodes = []
for elem in root.iter():
    transform = elem.attrib.get('transform', '')
    import re
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

# Sort nodes in reading order: top-to-bottom, left-to-right (or right-to-left)
nodes_ltr = sorted(nodes, key=lambda n: (n['y'], n['x']))
nodes_rtl = sorted(nodes, key=lambda n: (n['y'], -n['x']))

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

# Try candidate mappings:
# Normal arrows: {0, 90, 180, 270} mapped to {+, -, <, >}
# Bar arrows: mapped to {[ (if rot in X), ] (if rot in Y)}
# Circle: mapped to .

arrow_symbols = ['>', '<', '+', '-']

for order_name, node_list in [("LTR", nodes_ltr), ("RTL", nodes_rtl)]:
    for p in itertools.permutations(arrow_symbols):
        # p[0] for 0, p[1] for 90, p[2] for 180, p[3] for 270
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
            if res and ("YEK" in res or "flag" in res or len(res) > 5):
                print(f"[{order_name}] Found output ({p}, {bar_map}): {res}")

print("Search completed.")
