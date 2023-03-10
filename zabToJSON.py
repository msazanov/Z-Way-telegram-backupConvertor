#!/usr/bin/env python3

import base64
import json
import os
import sys

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = json.loads(f.read())['data']
    decoded_data = base64.b64decode(data).decode('utf-8')
    formatted_data = json.dumps(json.loads(decoded_data), indent=4, sort_keys=True)

    # Save the formatted data to a file with the same name but .json extension
    temp_output_filename = os.path.splitext(filename)[0] + ".json"
    with open(temp_output_filename, 'w') as output_file:
        output_file.write(formatted_data)

    # Delete the original file
    os.remove(filename)

    # Rename the temporary file to the original filename
    os.rename(temp_output_filename, os.path.splitext(filename)[0] + ".json")
