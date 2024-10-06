"""
Converts from Scribe-i18n localization JSON files to the Localizable.xcstrings file.


Usage:
    python3 Scribe-i18n/scripts/ios/convert_jsons_to_xcstrings.py
"""

import json
import os

directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Define the path to the "jsons" folder
jsons_folder = os.path.join(directory, "jsons")

# Ensure the "jsons" folder exists inside the directory
if not os.path.exists(jsons_folder):
    os.makedirs(jsons_folder)

json_dir_list = os.listdir(jsons_folder)
languages = sorted(
    [file.replace(".json", "") for file in json_dir_list if file.endswith(".json")]
)

# Load the base language file safely
with open(os.path.join(jsons_folder, "en-US.json"), "r") as json_file:
    file = json.load(json_file)

data = {"sourceLanguage": "en"}
strings = {}
for key in file:
    language = {}

    for lang in languages:
        with open(os.path.join(jsons_folder, f"{lang}.json"), "r") as lang_file:
            lang_json = json.load(lang_file)


        translation = lang_json[key] if key in lang_json else ""
        if lang == "en-US":
            lang = "en"
        if translation != "":
            language[lang] = {"stringUnit": {"state": "", "value": translation}}

    strings[key] = {"comment": "", "localizations": language}

data |= {"strings": strings, "version": "1.0"}

with open(os.path.join(directory, "Localizable.xcstrings"), "w") as outfile:
    json.dump(data, outfile, indent=2, ensure_ascii=False, separators=(",", " : "))

print(
    "Scribe-i18n localization JSON files successfully converted to the Localizable.xcstrings file."
)
