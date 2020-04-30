#!/bin/python
import yaml

output_end = True

stream = open("instructions.yml", 'r')
data = yaml.safe_load(stream)
f = open("out.html", "w")
l = list(data.values())
f.write("<!DOCTYPE html>\n<html>\n    <head>\n        <link rel=\"stylesheet\" href=\"main.css\">\n        <style>\n            body, html {\n                width: 100%;\n                min-height: 100%;\n                margin: 0px;\n                background-color: #F0F3F7;\n                color: #3A3D3D;\n                font-family: \"Lucida Console\", Monaco, monospace;\n                line-height: 1.5;\n            }\n            #maindiv {\n                width: 60%;\n                //margin: 0px auto 0px;\n                padding: 10px 5%;\n                min-height: calc(100vh - 70px);\n            }\n            h1 {\n                font-size: 36px;\n                margin: 10px 0px 20px 0px;\n            }\n            h1, h2, h3, h4, h5, th {\n                font-weight: normal;\n                font-family: Tahoma, Geneva, sans-serif;\n            }\n            hr {\n                height: 1px;\n                background-color: #BCC7CC;\n            }\n            table {\n                width: 100%;\n                cellspacing: 0;\n            }\n            td:not(:first-child) {\n                border-left: 1px solid #BCC7CC;\n            }\n            tr:nth-child(odd) {\n                background-color: #E4E8ED;\n            }\n            th {\n                background-color: #CED1D6;\n                padding: 10px;\n            }\n            th, td, table {\n                border-collapse: collapse;\n                font-size: 16px;\n            }\n            h2 {\n                text-align: center;\n                padding: 0px 10px;\n                font-size: 22px;\n            }\n            .s1 {\n                color: #800000;\n            }\n            .s2 {\n                color: #008000;\n            }\n            .s1, .s2, .s3 {\n                font-weight: bold;\n            }\n            .value {\n                text-align: center;\n            }\n            .description {\n                padding: 15px;\n            }\n            summary {\n                font-size: 22px;\n                outline: none;\n            }\n            summary:hover {\n                cursor: pointer;\n            }\n            .textblock {\n                width: 60%;\n                background-color: #FFFFFF;\n                border: 1px solid #BCC7CC;\n                padding: 15px;\n                margin-left: auto;\n                margin-right: auto;\n            }\n            hr {\n                border: 0;\n                height: 2px;\n                background-color: #CED1D6;\n            }\n        </style>\n    </head>\n    <body>\n        <?php include(\"navbar.php\"); ?>\n        <div id=\"maindiv\">\n            <h1 id=\"welcome\">SALL Docs</h1>")
num = 0
for i, val in enumerate(list(data.keys())):
    f.write("\n            <details>\n                <summary>" + val + "</summary>\n                <table class=\"salltable\">\n                    <tr>\n                        <th width=\"12%\">Opcode</th>\n                        <th width=\"5%\">Value</th>\n                        <th>Description</th>\n                    </tr>")
    for j, val2 in enumerate(l[i]):
        description = val2.get("description").replace("\n", "<br>")
        if(val2.get("example")):
            description += "<br>Example:"
            for k, val3 in enumerate(val2.get("example")):
                description += "<br>    " + val3
        f.write("\n                    <tr>\n                        <td><h2>" + list(val2.keys())[0] + "</h2></td>\n                        <td class=\"value\">" + ('0x%02X' % num) + "</td>\n                        <td class=\"description\"><pre>" + description + "</pre></td>\n                    </tr>")
        num += 1
    f.write("\n                </table>\n            </details>")
if(output_end):
    f.write("\n            <hr>\n            <details>\n                <summary>code</summary>\n                <pre class=\"textblock\">")
    maxnum = num - 1
    num = 0
    for i, val in enumerate(list(data.keys())):
        for j, val2 in enumerate(l[i]):
            _id = val2.get("id")
            if _id == None:
                f.write("#define I_" + list(val2.keys())[0].upper() + "\t " + ('0x%02X' % num) + "\n")
            else:
                f.write("#define I_" + _id.upper() + "\t " + ('0x%02X' % num) + "\n")
            num += 1
        #f.write("\n")
    f.write("</pre>\n");
    
    f.write("                <pre class=\"textblock\">");
    f.write("void (*instructions[256])() = {\n")
    num = 0
    for i, val in enumerate(list(data.keys())):
        for j, val2 in enumerate(l[i]):
            _id = val2.get("id")
            if _id == None:
                #f.write("    " + list(val2.keys())[0] + ("," if not num == maxnum else "") + (" " * (6 - len(list(val2.keys())[0]) + (1 if num == maxnum else 0))) + "// " + ('0x%02X' % num) + "\n")
                f.write("    " + list(val2.keys())[0] + "," + (" " * (6 - len(list(val2.keys())[0]))) + "// " + ('0x%02X' % num) + "\n")
            else:
                #f.write("    " + _id + ("," if not num == maxnum else "") + (" " * (6 - len(_id) + (1 if num == maxnum else 0))) + "// " + ('0x%02X' % num) + "\n")
                f.write("    " + _id + "," + (" " * (6 - len(_id))) + "// " + ('0x%02X' % num) + "\n")
            num += 1
    f.write("}")
    f.write("</pre>\n");
f.write("            </details>\n        </div>\n    </body>\n</html>")
f.close()
