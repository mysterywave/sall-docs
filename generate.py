#!/usr/bin/env python3

import yaml

TABLE_TEMPLATE = '''
            <details>
                <summary>{summary}</summary>
                <table class="salltable">
                    <tr>
                        <th width="12%">Opcode</th>
                        <th width="5%">Value</th>
                        <th>Description</th>  
                    </tr>{rows}
                </table>
            </details>'''

ROW_TEMPLATE = '''
                    <tr id="instruction-{id}">
                        <td><h2><a href="#instruction-{id}">{name}</a></h2></td>
                        <td class="value">{value}</td>
                        <td class="description">
                            <pre>{description}<br>Example: {examples}</pre>
                        </td>
                    </tr>'''

EXAMPLE_TEMPLATE = '''<br>    {example}'''

CODE_TEMPLATE = '''            <hr>
            <details>
                <summary>code</summary>
                <pre class="textblock">{defines}</pre>
                <pre class="textblock">{instructions}</pre>
            </details>'''

def formatter(data, text):
    for key, value in data.items():
        # None => ''
        text = text.replace('{%s}' % key, str(value) if value != None else '')
        
    return text

def generate_row(instruction):
    return formatter({
        # take formatting directly from yaml
        **instruction,
        
        # format multiple examples
        'examples' : ''.join([
            # repeat this for every example
            formatter({
                'example' : example
            }, EXAMPLE_TEMPLATE)
            
            for example in (
                # default to empty list if no examples
                instruction.get('examples') or list()
            )
        ])
    }, ROW_TEMPLATE)

def generate_tables(data):
    return ''.join([
        # generate every table at a time
        formatter({
            'rows' : ''.join([
                # generate row by row
                generate_row(instruction)
                for instruction in details
            ]),
            
            'summary' : summary
        }, TABLE_TEMPLATE)
        
        for summary, details in data.items()
    ])

def generate_code(data):
    define_code = ''
    instructions_code = 'void (*instructions[256])() = {\n'
    
    for summary, details in data.items():
        for instruction in details:
            define_code += formatter({
                **instruction,
                'id' : instruction['id'].upper()
            }, '#define I_{id}\t{value}\n')
            instructions_code += formatter(instruction, '    {id},\t// => {value} ({name})\n')
    
    instructions_code += '}'
    
    return formatter({
        'defines' : define_code,
        'instructions' : instructions_code
    }, CODE_TEMPLATE)

if __name__ == '__main__':
    CONFIG = 'instructions.yml'
    TEMPLATE = 'template.html'
    SHOW_CODE = False
    
    # read config
    
    with open(TEMPLATE, 'r') as f:
        template = f.read()
    
    with open(CONFIG, 'r') as f:
        data = yaml.safe_load(f.read())
    
    # add value attributes and patch id => name
    
    i = 0
    for summary, details in data.items():
        for instruction in details:
            instruction['value'] = '0x%02X' % i
            instruction['id'] = instruction.get('id', instruction['name'])
            i += 1
    
    # generate document
    
    output = formatter({
        'tables' : generate_tables(data),
        'code' : generate_code(data) if SHOW_CODE else '            <!-- run generate.py with the SHOW_CODE flag set to True to generate the code too -->'
    }, template)
    
    # save it
    
    print(output, end = '')
    
    with open('out.html', 'w') as f:
        f.write(output)
    
    
