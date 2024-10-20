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