#!/usr/bin/env python3

import sys
from os import path, walk
import yaml

def write_detail(output, item):
    metadata=item['metadata']
    results=item['results']
    if results['additional_comments_text'] != "" or results['recommendation'] not in skip_statuses:
        output.write('## ' + metadata['item_evaluated'] + '\n')

        output.write('[cols="^"]\n')
        output.write('|===\n')
        output.write('| \n')
        output.write('{set:cellbgcolor:' + result_statuses[results['recommendation']]['color'] + '}\n')
        output.write(result_statuses[results['recommendation']]['text'] + '\n')
        output.write('|===\n')

        output.write('\n')

        output.write('\n\n*Observed Result*\n\n')
        output.write(results['result_text'])

        if 'acceptance_criteria' in metadata.keys() and results['recommendation'] in metadata['acceptance_criteria']:

            output.write('\n\n*Matching Status(es)*\n\n')
            for matching_status in metadata['acceptance_criteria'][results['recommendation']]:
                output.write(" - " + matching_status + "\n")

        if results['recommendation'] not in skip_statuses:
            if results['impact_risk_text'] != "":
                output.write('\n\n*Impact and Risk*\n\n')
                output.write(results['impact_risk_text'])

            if results['remediation_text'] != "":
                output.write('\n\n*Remediation Advise*\n\n')
                output.write(results['remediation_text'])

        if results['additional_comments_text'] != "":
            output.write('\n\n*Additional Comments*\n\n')
            output.write(results['additional_comments_text'])

        if len(metadata['references']) > 0 :
            output.write('\n\n*Reference Link(s)*\n\n')
            for ref in metadata['references']:
                output.write("* " + ref['url'] + "[" + ref['title'] + "]\n")
                output.write("** " + ref['url'] + "\n")

    output.write('\n')

def generate_key_table(output):
    "Generates a key table of item status with their meanings"
    output.write('\n')
    output.write('[cols="1,3", options=header]\n')
    output.write('|===\n')
    output.write('|Value\n')
    output.write('|Description\n')
    output.write('\n')
    output.write('\n')

    for key in result_statuses.keys():
        output.write('| \n')
        output.write('{set:cellbgcolor:' + result_statuses[key]['color'] + '}\n')
        output.write(result_statuses[key]['text'] + '\n')
        output.write('|\n')
        output.write('{set:cellbgcolor!}\n')
        output.write(result_statuses[key]['description'] + '\n')
        output.write('\n')

    close_table(output)

def close_table(output):
    "Write table closing ASCIIdoc"
    output.write('|===\n')

def generate_table_header(output):
    "Generate a standard table header for item table"

    # Write first row
    output.write('[cols="1,3,3,2,2,2"]\n')
    output.write('|===\n')
    output.write('.2+|\n{set:cellbgcolor:#D3D3D3}\n*Category*\n')
    output.write('.2+|*Item Evaluated*\n')
    output.write('2+|*Test Rules*\n')
    output.write('.2+|*Observed Result*\n')
    output.write('.2+|*Recommendation*\n')

    # Write second row.  Only two items, since most columns in
    # prior row spanned two columns.
    output.write('|*Criteria*\n')
    output.write('|*Matching Status*\n')

    output.write('\n')

def write_table_row(output, item):
    metadata=item['metadata']
    results=item['results']

    row_span = 0

    for ac_key in metadata['acceptance_criteria'].keys():
        row_span += len(metadata['acceptance_criteria'][ac_key])

    output.write('// ------------------------ITEM START\n')
    output.write('// ----ITEM SOURCE:  ' + item['filename'] + '\n')

    output.write('// Category\n')
    output.write('.' + str(row_span) + '+')
    output.write('|\n')
    output.write('{set:cellbgcolor!}\n')
    output.write(categories[metadata['category_key']]['short_text'])
    output.write('\n')

    output.write('// Item Evaluated\n')
    output.write('.' + str(row_span) + '+')
    output.write('|\n')
    output.write(metadata['item_evaluated'])
    output.write('\n')

    firstloop = True

    for ac_key in metadata['acceptance_criteria'].keys():
        ac_name = result_statuses[ac_key]['text']

        for ac_item in metadata['acceptance_criteria'][ac_key]:

            output.write('// AC Text \n')
            output.write('|\n{set:cellbgcolor!}\n')
            output.write(ac_item)
            output.write('\n')

            output.write('// AC \n')
            output.write('|\n')
            output.write(ac_name)
            output.write('\n')

            if firstloop == True:
                output.write('// Result\n')
                output.write('.' + str(row_span) + '+')
                output.write('| \n')
                output.write(results['result_text'])
                output.write('\n')
                output.write('// Recommendation\n')
                output.write('.' + str(row_span) + '+')
                output.write('| \n')
                output.write('{set:cellbgcolor:' + result_statuses[results['recommendation']]['color'] + '}\n')
                output.write(result_statuses[results['recommendation']]['text'] + '\n')
                output.write('\n')

                firstloop = False

    output.write('// ------------------------ITEM END\n')

def load_statuses(filename):
    if path.exists(filename):
        y = yaml.safe_load(open(filename))
    else:
        y = yaml.safe_load('''
statuses:
  changes_required:
    color: '#FF0000'
    text: 'Changes Required'
    description: 'Indicates Changes Required for system stability, subscription compliance, or other reason.'
  changes_recommended:
    color: '#FEFE20'
    text: 'Changes Recommended'
    description: 'Indicates Changes Recommended to align with recommended practices, but not urgently required'
  na:
    color: '#A6B9BF'
    text: 'N/A'
    description: 'No advise given on line item.  For line items which are data-only to provide context.'
  advisory:
    color: '#80E5FF'
    text: 'Advisory'
    description: 'No change required or recommended, but additional information provided.'
  no_change:
    color: '#00FF00'
    text: 'No Change'
    description: 'No change required.  In alignment with recommended practices.'
  tbe:
    color: '#FFFFFF'
    text: 'To Be Evaluated'
    description: 'Not yet evaluated.  Will appear only in draft copies.'
''')

    return y['statuses']

def load_skip_statuses(filename):
    if path.exists(filename):
        y = yaml.safe_load(open(filename))
        return y['skip_statuses']
    else:
        return ['na', 'tbe', 'no_change']

def load_categories(filename):
    if path.exists(filename):
        y = yaml.safe_load(open(filename))
        return y['categories']
    else:
        print("No categories file found at:  " + filename)
        sys.exit(1)


if len(sys.argv) != 3:
    print("----USAGE----")
    print(sys.argv[0] + " <input directory> <output file>")
    sys.exit(1)

################
# MAIN PROGRAM #
################

input_dir = sys.argv[1]
output_file = sys.argv[2]

item_files = []

findings = {}

result_statuses = load_statuses(input_dir + '/config.yaml')
skip_statuses = load_skip_statuses(input_dir + '/config.yaml')
categories = load_categories(input_dir + '/categories.yaml')

for (dirpath, dirnames, filenames) in walk(input_dir):
    for item in filenames:
        if item.endswith('.item'):
            item_files.append(input_dir + '/' + item)
    break

item_files.sort()

load_errors = 0

for item in item_files:
    y = yaml.safe_load(open(item))

    y['filename'] = item

    if y['results']['recommendation'] not in result_statuses.keys():
        load_errors += 1
        print("Recommendation value invalid")
        print(y['results']['recommendation'] + " in file " + item)

    if y['metadata']['category_key'] not in categories.keys():
        load_errors += 1
        print("Category value invalid")
        print(y['metadata']['category_key'] + " in file " + item)

    # if y['include_text'] is True:
    #     if path.exists(item + ".adoc"):
    #         y['text_path'] = item + ".adoc"
    #     else:
    #         load_errors += 1
    #         print("Text file not found")
    #         print("For file " + item)

    if y['metadata']['category_key'] in findings.keys():
        findings[y['metadata']['category_key']].append(y)

    else:
        findings[y['metadata']['category_key']] = [y]

if load_errors > 0:
    print("There were " + str(load_errors) + " loading errors")
    exit(1)
# write summary

output = open(output_file, 'w')

#######################
# WRITE SUMMARY TABLE #
#######################

output.write('= Key\n')

generate_key_table(output)

output.write('= Summary\n')

generate_table_header(output)

for key in findings.keys():
    for item in findings[key]:
        write_table_row(output, item)

close_table(output)


#########################
# WRITE DETAIL SECTIONS #
#########################
for key in findings.keys():
    output.write('<<<\n')
    output.write('# ' + categories[key]['text'] + '\n')

    # Write Table

    generate_table_header(output)

    for item in findings[key]:
        write_table_row(output, item)

    close_table(output)

    # Page break between table and descriptions looks nice
    output.write('<<<\n\n')

    # Write Descriptions
    for item in findings[key]:
        output.write('\n')

        write_detail(output, item)

        output.write('\n')

# WRITE FINAL INVISIBLE TABLE
# This resets the bgcolor for future tables
output.write('''
[grid=none,frame=none]
|===
|{set:cellbgcolor!}
|===
''')

output.close()
