import numpy as np
import pandas as pd
from pathlib import Path
from xml.dom.minidom import parse
from shutil import copyfile
import os
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from colorama import Fore
from colorama import Style
from pathlib import Path
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel



console = Console()
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})
def xml2txt():
    def convert_annot(size, box):
        x1 = int(box[0])
        y1 = int(box[1])
        x2 = int(box[2])
        y2 = int(box[3])

        dw = np.float32(1. / int(size[0]))
        dh = np.float32(1. / int(size[1]))

        w = x2 - x1
        h = y2 - y1
        x = x1 + (w / 2)
        y = y1 + (h / 2)

        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return [x, y, w, h]

    def save_txt_file(img_jpg_file_name, size, img_box):
        Path(main_dir + "/labels").mkdir(parents=True, exist_ok=True)
        save_file_name = main_dir + '/labels/' + \
            img_jpg_file_name + '.txt'
        with open(save_file_name, 'a+') as file_path:
            for box in img_box:
                
                cls_num = classes.index(box[0])
                new_box = convert_annot(size, box[1:])

                file_path.write(
                    f"{cls_num} {new_box[0]} {new_box[1]} {new_box[2]} {new_box[3]}\n")

            file_path.flush()
            file_path.close()

    def get_xml_data(file_path, img_xml_file):
        img_path = file_path + '/' + img_xml_file
        dom = parse(img_path)
        root = dom.documentElement
        img_name = root.getElementsByTagName("filename")[0].childNodes[0].data
        img_size = root.getElementsByTagName("size")[0]
        objects = root.getElementsByTagName("object")
        img_w = img_size.getElementsByTagName("width")[0].childNodes[0].data
        img_h = img_size.getElementsByTagName("height")[0].childNodes[0].data
        img_c = img_size.getElementsByTagName("depth")[0].childNodes[0].data
        img_box = []
        for box in objects:
            cls_name = box.getElementsByTagName("name")[0].childNodes[0].data
            x1 = int(box.getElementsByTagName("xmin")[0].childNodes[0].data)
            y1 = int(box.getElementsByTagName("ymin")[0].childNodes[0].data)
            x2 = int(box.getElementsByTagName("xmax")[0].childNodes[0].data)
            y2 = int(box.getElementsByTagName("ymax")[0].childNodes[0].data)
            img_jpg_file_name = img_xml_file + '.jpg'
            img_box.append([cls_name, x1, y1, x2, y2])
        img_xml_file = img_xml_file.split('.')[0]
        
        for box in img_box:
            if box[0] in classes_quantity:
                classes_quantity[box[0]] += 1
            else:
                classes_quantity[box[0]] = 1
        if box[0] in classes:
            save_txt_file(img_xml_file, [img_w, img_h], img_box)
    xml2txt_questions = [
        {
            'type': 'input',
            'name': 'pathxml',
            'message': 'Enter the path where you have the xml files:',
            'validate': lambda answer: 'You must enter a path.'
            if len(answer) == 0 else True
        },
        {
            'type': 'input',
            'name': 'classess',
            'message': 'Enter the classes you want to convert to txt separate by , :',
            'validate': lambda answer: 'You must enter at least one class.'
            if len(answer) == 0 else True
        }
    ]
    answers = prompt(xml2txt_questions, style=style)
    main_dir = answers['pathxml']
    classes = answers['classess'].split(',')
    xml_file = os.listdir(main_dir)
    classes_quantity = {}
    
    with console.status("Monkeying around...", spinner="monkey"):
        for path in xml_file:
            if path.endswith('.xml'):
                get_xml_data(main_dir, path)

    def get_formatted_classes_quantity(classe_quantity):
        name = classe_quantity
        quantity = classes_quantity[classe_quantity]
        return f"[b]{name}[/b]\n[yellow]{quantity}"
    print(" ")
    console.print("Classes Found", style="bold red", justify="center")
    print(" ")
    
    classes_found = [Panel(get_formatted_classes_quantity(classes), expand=True) for classes in classes_quantity]
    console.print(Columns(classes_found))
    print(" ")
    console.print("Everything was completed successfully...", style="bold green")
    
