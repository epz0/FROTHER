import os
import pandas as pd
import json

def format_output(output):
    output = output.replace("\n", "")
    output = output.replace("    ", "")
    output = output.replace("  ", "")
    output = output.replace('","', '", "')

    output = output.replace("},{", "},}|{,{")

    output = output.replace('{"', '"').replace('"}', "")
    output = output.replace(",}", "}").replace("{,", "{")
    output = output.replace(".}", '."}')
    if r'}}' in output:
        output = output.replace('"}', '"')
    output = output.split('|')
    return output

def read_output(f_output):
    files = []

    for filename in os.listdir(f_output):
        filePath = os.path.join(f_output, filename)

        with open(filePath, 'r') as file:
            content = file.read()

        files.append(content)

    return files

def format_read_file(ls_js_read):
    ls_all = []

    for i in range(len(ls_js_read)):
        ls_all_json=[]
        tmp_json = ls_js_read[i].replace('\n',',').replace(' {','{')
        tmp_json = tmp_json.replace('},{','}|{')
        ls_all_json.append(tmp_json.split('|'))
        for id in ls_all_json[0]:
            ls_all.append(json.loads(id))

    df = pd.DataFrame(ls_all)
    df = df.sort_values(by='ID')

    return ls_all, df
