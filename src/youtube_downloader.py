from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import pytube
from pytube.cli import on_progress
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
def youtube_downloader():
    youtube_downloader_questions = [
        {
            'type': 'input',
            'name': 'url',
            'message': 'Enter the URL of the video you want to download:',
            'validate': lambda answer: 'You must enter a URL.'
            if len(answer) == 0 else True
        },
        {
            'type': 'input',
            'name': 'path',
            'message': 'Enter the path where you want to save the video:',
            'validate': lambda answer: 'You must enter a path.'
            if len(answer) == 0 else True,
            'default': './'
        }
    ]
    answers = prompt(youtube_downloader_questions, style=style)
    url = answers['url']
    path = answers['path']
    with console.status("Getting data from the video", spinner="monkey"):
        query = pytube.YouTube(url, on_progress_callback=on_progress)
    video_options = [{
        'type': 'list',
        'name': 'video',
        'message': 'Select the video quality you want to download:',
        'choices': [
             {
                'name': f"{stream.resolution}  {stream.fps}fps {stream.mime_type}",
                'value': stream.itag
            } for stream in query.streams if stream.resolution is not None and stream.mime_type == 'video/mp4'
        ]
    }]
    answers = prompt(video_options, style=style)
    video = answers['video']

    video_dp = query.streams.get_by_itag(video)
    video_dp.download(path)
