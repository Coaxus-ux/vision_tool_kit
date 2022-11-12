from __future__ import print_function, unicode_literals
import regex
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError

import numpy as np
import pandas as pd
from pathlib import Path
from xml.dom.minidom import parse
from shutil import copyfile
import os
from src.youtube_downloader import youtube_downloader
from src.xml2txt import xml2txt
print(
    " \
    ░█░█░▀█▀░█▀▀░▀█▀░█▀█░█▀█░▀█▀░█▀█░█▀█░█░░░█░█░▀█▀░▀█▀ \n \
    ░▀▄▀░░█░░▀▀█░░█░░█░█░█░█░░█░░█░█░█░█░█░░░█▀▄░░█░░░█░ \n \
    ░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░▀░ \n \
    "
)
style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


fucntions_manager = {
    "Download youtube video": youtube_downloader,
    "xml2txt": xml2txt,
}
main_questions = [
    {
        'type': 'list',
        'message': 'Select want to do ',
        'name': 'todo',
        'choices': ['JPG2PNG', 'Download youtube video', 'xml2txt', 'move files', 'rename files']
    }
]
answers = prompt(main_questions, style=style)
fucntions_manager[answers['todo']]()
