import xml.etree.ElementTree as ET
import re

tree = ET.parse('/Users/ricksabchez/workspace/sargijeh.svg')
root = tree.getroot()

# Let's inspect each node's exact shape and rotation
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

# Grid map
grid = {(n['x'], n['y']): n for n in nodes}

# Brainfuck interpreter
def run_bf(code):
    tape = [0] * 30000
    ptr = 0
    code_ptr = 0
    output = []
    
    # Precompute jump brackets
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

    steps = 0
    while code_ptr < len(code) and steps < 1000000:
        cmd = code[code_ptr]
        if cmd == '>':
            ptr += 1
        elif cmd == '<':
            ptr -= 1
        elif cmd == '+':
            tape[ptr] = (tape[ptr] + 1) % 256
        elif cmd == '-':
            tape[ptr] = (tape[ptr] - 1) % 256
        elif cmd == '.':
            output.append(chr(tape[ptr]))
        elif cmd == '[':
            if tape[ptr] == 0:
                code_ptr = brackets.get(code_ptr, len(code))
        elif cmd == ']':
            if tape[ptr] != 0:
                code_ptr = brackets.get(code_ptr, code_ptr)
        code_ptr += 1
        steps += 1
    return "".join(output)

print("Interpreter ready. Total nodes:", len(nodes))
