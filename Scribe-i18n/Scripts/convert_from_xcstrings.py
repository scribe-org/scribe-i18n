import os
import json

directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file = open(os.path.join(directory, "Localizable.xcstrings"), "r").read()
files = os.listdir(directory)
langlist = [file.replace('.json', '') for file in files if file.endswith('.json')]

for lang in langlist:
    dest = open(f'{directory}/{lang}.json', 'w')
    if lang == "en-US":
        lang = "en"

    data = '{\n'
    json_file = json.loads(file)
    strings = json_file["strings"]
    pos = 0
    for key in strings:
        pos += 1
        translation = ''
        if (lang in json_file["strings"][key]["localizations"]
                and json_file["strings"][key]["localizations"][lang]["stringUnit"]["value"] != ""
                and json_file["strings"][key]["localizations"][lang]["stringUnit"]["value"] != key):
            translation = (json_file["strings"][key]["localizations"][lang]["stringUnit"]["value"]
                           .replace('"', '\\"')
                           .replace('\n', '\\n'))
        data += f'  "{key}" : "{translation}"'
        if pos < len(json_file["strings"]):
            data += ',\n'
        else:
            data += '\n'
    data += '}\n'

    dest.write(data)
