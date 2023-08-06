import base64
import xml.etree.cElementTree as et
import os
import zipfile
import argparse

resource_path = "resources/"

def str2image(image_name, image_format, image_string):
    with open(os.path.join(resource_path, f"{image_name}.{image_format}"), "wb") as fh:
        fh.write(base64.b64decode(image_string))

right_side = []
left_side = []

def when_element(elem):
    if elem[0].tag == "type":
        if elem[0].text == "variable":
            outputdata = elem[1]
            name = outputdata[0].text
            value = outputdata[1].text
            rows = outputdata[2].text
            columns = outputdata[3].text
            lineNumbers = []
            for el in elem[2]:
                lineNumbers.append(el.text)
            # print(name, value, rows, columns, lineNumbers)
            right_side.append(["variable", name, value, rows, columns, lineNumbers])
        elif elem[0].text == "matrix":
            outputdata = elem[1]
            name = outputdata[1].text
            varSize = outputdata[2].text
            rows = outputdata[3].text
            columns = outputdata[4].text
            varType = outputdata[5].text
            value = outputdata[6].text
            lineNumbers = []
            for el in elem[2]:
                lineNumbers.append(el.text)
            # print(name, varSize, varType, rows, columns, lineNumbers)
            # print(value)
            right_side.append(["matrix", name, varSize, varType, value, rows, columns, lineNumbers])
        elif elem[0].text == "text":
            outputdata = elem[1]
            text = outputdata[0].text
            lineNumbers = []
            for el in elem[2]:
                lineNumbers.append(el.text)
            # print(text, lineNumbers)
            right_side.append(["text", text, lineNumbers])
        elif elem[0].text == "figure":
            outputdata = elem[1]
            figureId = outputdata[0].text
            figureUri = outputdata[1].text
            width = outputdata[2][0].text
            height = outputdata[2][1].text
            regionNumbers = outputdata[3].text
            originalRegionNumber = outputdata[4].text
            lineNumbers = []
            for el in elem[2]:
                lineNumbers.append(el.text)

            index = figureUri.find(',')
            format_ind0 = figureUri.find('/')
            format_ind1 = figureUri.find(';')
            image_string = figureUri[index + 1:]
            image_format = figureUri[format_ind0 + 1: format_ind1]
            str2image(figureId, image_format, image_string)
            # print(figureId, width, height, image_format, lineNumbers)
            right_side.append(["figure", f"{figureId}.{image_format}", width, height, lineNumbers])
    elif elem[0].tag == "code":
        sectionBreak = elem[0][0].text
        endOfSection = elem[0][1].text
        regionNumber = elem[0][2].text
        startLine = elem[1].text
        endLine = elem[2].text
        outputIndexes = []
        for el in elem[3]:
            outputIndexes.append(el.text)
        # print(sectionBreak, endOfSection, regionNumber, startLine, endLine, outputIndexes)


def output(outputxml_path):
    tree=et.parse(outputxml_path)
    root=tree.getroot()

    for child in root:
        if child.tag == "outputArray":
            for grandchild in child:
                if grandchild.tag == "element":
                    when_element(grandchild)
        elif child.tag == "regionArray":
            for grandchild in child:
                if grandchild.tag == "element":
                    when_element(grandchild)

def document(documentxml_path):
    tree=et.parse(documentxml_path)
    root=tree.getroot()

    body = root[0]
    for child in body:
        dic = child[0][0].attrib
        if len(dic):
            style = dic[next(iter(dic))]
            if style == "code":
                code = child[1][0].text
                # print(code)
                left_side.append(["code", code])
            elif style == "heading":
                text = child[1][0].text
                # print(text)
                left_side.append(["heading", text])
        else:
            # print(50*"*")
            left_side.append(["breakline"])
    
def cook(outputmd_path, multicolumn=False):
    left_text = ""
    for elem in left_side:
        if elem[0] == "heading":
            left_text += f"\n**{elem[1]}**\n"
        if elem[0] == "code":
            left_text += f"\n```Matlab\n{elem[1]}\n```\n"
        if elem[0] == "breakline":
            left_text += "\n<hr>\n"

    right_text = ""
    for elem in right_side:
        if elem[0] == "variable":
            right_text += f"\n**{elem[1]}** *({elem[3]}x{elem[4]})*:\n" # name (rows x columns)
            right_text += f"\n```\n{elem[2]}\n```\n" # value
        if elem[0] == "matrix":
            right_text += f"**{elem[1]}** *({elem[5]}x{elem[6]}) {elem[3]}*:\n" # name size type
            right_text += f"\n```\n{elem[4]}\n```\n" # value
        if elem[0] == "figure":
            right_text += f"\n![{elem[1]}]({resource_path}{elem[1]})\n\n" # figure
        if elem[0] == "text":
            right_text += f"\n```\n{elem[1]}\n```\n" # text

    if multicolumn:
        markdown_text ='''

<table border="1">
<tr>
    <td><b style="font-size:30px">MATLAB LIVE SCRIPT</b></td>
    <td><b style="font-size:30px">LIVE RESULTS</b></td>
</tr>
<tr>
    <td>
        ''' + left_text + "</td><td>\n" + right_text + "</td></tr></table>"
    else:
        markdown_text = "<h1>MATLAB LIVE SCRIPT</h1>\n" + left_text + "<h1>RESULTS</h1>\n" + right_text
    
    with open(outputmd_path, "w") as f:
        f.write(markdown_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert your MATLAB MLX file to Markdown format')
    parser.add_argument('-i','--input', help='path to mlx file', required=True)
    parser.add_argument('-m','--multicolumn', help='passing False puts Results after Code, passing True puts Results next to Code ', required=False)
    args = vars(parser.parse_args())

    # mlx_path = "file.mlx"
    mlx_path = args['input']
    basename = os.path.basename(mlx_path)
    # extract_path = "mlx_data"
    extract_path = mlx_path[:-len(basename)] + "mlx_data"
    # output_path = "file.md"
    output_path = mlx_path[:-3] + "md"

    multicolumn = args['multicolumn']

    resource_path = os.path.join(mlx_path[:-len(basename)], resource_path)
    if not os.path.exists(resource_path):
        os.mkdir(resource_path)

    with zipfile.ZipFile(mlx_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    output(os.path.join(extract_path, "matlab", "output.xml"))
    document(os.path.join(extract_path, "matlab", "document.xml"))
    cook(output_path, multicolumn)
