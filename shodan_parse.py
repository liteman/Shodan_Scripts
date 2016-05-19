import json

INFILE = '/Users/user/Desktop/shodan_export.txt'

with open(INFILE, 'r') as jfile:
    jmem = json.load(jfile)

modules = []
for item in jmem:
    if item.get('_shodan').get('module') in modules:
        continue
    else:
        modules.append(item.get('_shodan').get('module'))

fields = {}
for mod in modules:
        if mod in fields.keys():
            print fields.keys()
            continue
        else:
            for item in jmem:
                if item.get('_shodan').get('module') == mod:
                    fields[mod] = item.keys()

with open("field_names.txt", "wb") as w:
    for key in fields.keys():
        w.write(key + ": " + ','.join(fields.get(key)) + "\n")




