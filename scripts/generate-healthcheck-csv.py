#!/usr/bin/env python3

from os import path, walk
import yaml
import sys

colors={'required': '#FF0000', 'recommended': '#FEFE20', 'na': '#A6B9BF', 'advisory': '#80E5FF', 'no_change': "#00FF00", 'tbe': '#FFFFFF'}
text={'required': 'Changes Required', 'recommended': 'Changes Recommended', 'na': 'N/A', 'advisory': 'Advisory', 'no_change': "No Change", 'tbe': 'To Be Evaluated'}


f = []

findings = {}

print("This script is currently broken, please do not use.")
sys.exit(1)

if len(sys.argv) != 3:
    print("----USAGE----")
    print(sys.argv[0] + " <input directory> <output file>")

    print(sys.argv)
    sys.exit(1)


input_dir = sys.argv[1]
output_file = sys.argv[2]


for (dirpath, dirnames, filenames) in walk(input_dir):
    for item in filenames:
        if item.endswith('.item'):
            f.append(input_dir  + '/' + item)
    break

f.sort()

load_errors = 0

for item in f:
    y = yaml.safe_load(open(item))

    if y['recommendation'] not in text.keys():
        load_errors += 1
        print("Recommendation value invalid")
        print(y['recommendation'] + " in file " + item)

    if y['include_text'] is True:
        if path.exists(item + ".adoc"):
            y['text_path'] = item + ".adoc"
        else:
            load_errors += 1
            print("Text file not found")
            print("For file " + item)

    if y['category_key'] in findings.keys():
        findings[y['category_key']].append(y)

    else:
        findings[y['category_key']] = [y]

if load_errors > 0:
    print("There were " + str(load_errors) + " loading errors")
    exit(1)
# write summary

output = open(output_file, 'w')

output.write('Category,Item Evaluated,Result,Recommendation,Recommendation_Text\n')

for key in findings.keys():
    for item in findings[key]:
        output.write('"')
        output.write(item['category_short'])
        output.write('","')
        output.write(item['item_evaluated'])
        output.write('","')
        output.write(item['result'])
        output.write('","')
        output.write(text[item['recommendation']])
        output.write('","')
        if ('acceptance_criteria' in item.keys() and item['recommendation'] in item['acceptance_criteria']):
            output.write(item['acceptance_criteria'][item['recommendation']][0])
        else:
            output.write("N/A")
        output.write('"\n')

output.write('\n')

output.close()

#print(findings)
