#!/usr/bin/env python3
import base64
import os
import sys

filename = os.path.splitext(sys.argv[1])[0] + ".zab"

with open(sys.argv[1], "rb") as f_in, open(filename, "wb") as f_out:
    data = f_in.read()
    encoded = base64.b64encode(data).decode("utf-8")
    f_out.write(
        ('{"data":"%s","code":200,"message":"200 OK","error":null}\n' % encoded).encode(
            "utf-8"
        )
    )

os.remove(sys.argv[1])
