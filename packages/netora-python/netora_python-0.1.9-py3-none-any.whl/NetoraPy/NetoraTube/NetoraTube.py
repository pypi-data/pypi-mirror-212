from yt_dlp import YoutubeDL
import json
import copy
import os
import sys
import datetime

VIDEO = 'video'
AUDIO = 'audio'

F_M4A = 'm4a'
F_MP3 = 'mp3'
F_MP4 = 'mp4'
F_WEBM = 'webm'
F_MKV = 'mkv'

def filename_convert(filename:str):
    for i in ['\\', '/', '"', ':', '<', '>', '|', '*', '?']:
        filename = filename.replace(i, '')
    return filename

class Media():
    def __init__(self, type:str, format_id:str, format:str, filesize:int, protocol:str, width:int=None, height:int=None, resolution:str=None) -> None:
        self.format_id = format_id
        self.width = width
        self.height = height
        self.resolution = resolution
        self.format = format
        self.filesize = filesize
        self.protocol = protocol
        self.type = type

    def to_dict(self):
        return {
            'format_id': self.format_id,
            'width': self.width,
            'height': self.height,
            'resolution': self.resolution,
            'format': self.format,
            'filesize': self.filesize,
            'protocol': self.protocol,
            'type': self.type
        }
    
class Video(Media):
    def __init__(self, format_id:str, format:str, filesize:int, protocol: str, width:int, height:int, resolution:str) -> None:
        super().__init__(VIDEO, format_id, format, filesize, protocol, width, height, resolution)

class Audio(Media):
    def __init__(self, format_id:str, format:str, filesize:int, protocol:str) -> None:
        super().__init__(AUDIO, format_id, format, filesize, protocol)

class Options:
    def __init__(self, ytdlp:YoutubeDL, ytvideo_info:dict) -> None:
        self.info = ytvideo_info
        self.ytdlp = ytdlp
        self.selected_option = [None, None]
        self.output_format = None

        # Video Options
        self.options = [
            Video(
                i['format_id'],
                i['ext'],
                i['filesize'],
                i['protocol'],
                i['width'],
                i['height'],
                i['resolution']
            ) if i['video_ext'] != 'none' else
            Audio(
                i['format_id'],
                i['ext'],
                i['filesize'],
                i['protocol']
            )
            for i in self.ytdlp.sanitize_info(self.info)['formats'] 
            if i['format_note'] != 'storyboard' and (i['ext'] == 'webm' or i['ext'] == 'mp4' or i['ext'] == 'm4a')
        ]

        # Remove Duplicate
        self.opts = []
        for opt in self.options:
            if opt.filesize:
                is_duplicate = False
                for opt2 in self.opts:
                    if (opt.format, opt.height) == (opt2.format, opt2.height):
                        is_duplicate = True
                        if opt2.filesize and opt.filesize > opt2.filesize:
                            self.opts[self.opts.index(opt2)] = opt
                            break

                if not is_duplicate:
                    opt:Media
                    self.opts.append(opt)

        self.options = self.opts

        # Selectable Formats & Resolutions
        self.selectableOptions = {}
        for opt in self.options:
            if opt.format in self.selectableOptions:
                self.selectableOptions[opt.format].append({
                    'format_id': opt.format_id,
                    'width': opt.width,
                    'height': opt.height,
                    'type': opt.type,
                    'filesize': opt.filesize,
                    'format_id': opt.format_id,
                    'protocol': opt.protocol
                })
            else:
                self.selectableOptions.update({opt.format: []})
                self.selectableOptions[opt.format].append({
                    'format_id': opt.format_id,
                    'width': opt.width,
                    'height': opt.height,
                    'type': opt.type,
                    'filesize': opt.filesize,
                    'format_id': opt.format_id,
                    'protocol': opt.protocol
                })

    def get_options(self):
        return {
            fmt: [
                res['height']
                for res in self.selectableOptions[fmt]
                if res['height']
            ]
            for fmt in self.selectableOptions
        }
    
    def get_audios(self, format:str=None):
        return [
            opt
            for opt in self.options
            if opt.type == AUDIO and ((format and format == opt.format) or not format)
        ]
    
    def get_videos(self, format:str=None):
        return [
            opt
            for opt in self.options
            if opt.type == VIDEO and ((format and format == opt.format) or not format)
        ]
    
    def select(self, video_option:dict=None, audio_option:dict=None, optimization_options:bool=False, output_format:str='mp4'):
        '''
            video_option: dict -> The option requirements of the video by using dictionary
             - Example: {'format': 'mp4', 'height': 1080}

            audio_option: dict -> The option requirements of the audio by using dictionary
             - Example: {'format': 'm4a'}

            optimization_options: bool -> Choose the best download option automatically

            output_format: str -> The output format of the video/audio downloaded
             - Example: 'mp4'
        '''

        if optimization_options:
            video_option = {
                'format': 'webm',
                'height': [h.height for h in self.get_videos('webm')][-1]
            }

            audio_option = {
                'format': 'webm'
            }

        if video_option:
            for opt in self.options:
                if opt.type == VIDEO:
                    is_meet_all_requirements = True
                    for req in video_option:
                        if video_option[req] != opt.to_dict()[req]:
                            is_meet_all_requirements = False
                            break
                    
                    if is_meet_all_requirements:
                        self.selected_option[0] = opt
                        break
        
        if audio_option:
            for opt in self.options:
                is_meet_all_requirements = True
                if opt.type == AUDIO:
                    for req in audio_option:
                        if audio_option[req] != opt.to_dict()[req]:
                            is_meet_all_requirements = False
                            break
                    
                    if is_meet_all_requirements:
                        self.selected_option[1] = opt
                        break

        self.output_format = output_format

    def select_by_expression(self, expression:str):
        '''
            Expression: '-v <video-resolution>/<video-format> -a <audio-format> -of <output-format>'
        '''
        expression = expression.replace('  ', ' ')
        expression = expression.split()
        for i, exp in enumerate(expression):
            expression[i] = exp.strip()

        output_format = None
        v_resolution, v_format = None, None
        a_format = None

        for i, exp in enumerate(expression):
            if exp == '-v':
                v_resolution, v_format = expression[i+1].split('/', 1) if len(expression[i+1].split('/')) == 2 else [self.list_videos(expression[i+1])[-1].height, expression[i+1]]
            elif exp == '-a':
                a_format = expression[i+1]
            elif exp == '-of':
                output_format = expression[i+1]

            if all([v_resolution, v_format, a_format]):
                option = {'height': int(v_resolution), 'format': v_format}, {'format': a_format}, False, output_format
            
            elif all([v_resolution, v_format]):
                option = {'height': int(v_resolution), 'format': v_format}, None, False, output_format
            
            elif a_format:
                option = None, {'format': a_format}, False, output_format
            
            else:
                option = None, None, True, output_format

        self.select(*option)

    def list_options(self):
        '''
            Print out all options that the video allowed
        '''
        for format in self.get_options():
            print(f"<{format}>")
            for res in self.get_options()[format]:
                print(f" - {res}")

class NetoraTube:
    def __init__(self, url:str, download_progress_handler=None) -> None:
        # Args
        self.url = url
        self.download_progress_handler = download_progress_handler

        # Get youtube video information
        self.ytd = YoutubeDL()
        self.info = self.ytd.extract_info(self.url, False)
        self.title = self.ytd.sanitize_info(self.info)['title']
        self.thumbnail = self.ytd.sanitize_info(self.info)['thumbnail']
        self.duration = datetime.timedelta(seconds=self.ytd.sanitize_info(self.info)['duration'])

        # Get youtube video download options
        self.options = Options(self.ytd, self.info)

    def download(self):
        video_format_id = self.options.selected_option[0].format_id if self.options.selected_option[0] else None
        audio_format_id = self.options.selected_option[1].format_id if self.options.selected_option[1] else None
        output_format = self.options.output_format

        if video_format_id and audio_format_id:
            option = {
                'format': f'{video_format_id}+{audio_format_id}',
                'requested_formats': [self.options.selected_option[0].format, self.options.selected_option[1].format],
                'outtmpl': filename_convert(f'{self.title}'),
                'progress_hooks': [self.__on_progress]
            }

            if option['requested_formats'][0] == option['requested_formats'][1]:
                output_filename = [filename_convert(f'{self.title}.{option["requested_formats"][0]}')]
            elif option['requested_formats'][0] == 'mp4' and option['requested_formats'][1] == 'webm':
                output_filename = [filename_convert(f'{self.title}.mkv'), filename_convert(f'{self.title}.webm')]
            elif option['requested_formats'][0] == 'webm' and option['requested_formats'][1] == 'm4a':
                output_filename = [filename_convert(f'{self.title}.mkv')]
            elif option['requested_formats'][0] == 'mp4' and option['requested_formats'][1] == 'm4a':
                output_filename = [filename_convert(f'{self.title}.mp4')]
            else:
                output_filename = [filename_convert(f'{self.title}.mp4')]
        
        elif video_format_id:
            option = {
                'format': f'{video_format_id}/{self.options.selected_option[0].format}',
                'outtmpl': filename_convert(f'{self.title}.{self.options.selected_option[0].format}'),
                'progress_hooks': [self.__on_progress]
            }

            output_filename = [filename_convert(f'{self.title}.{self.options.selected_option[0].format}')]
        
        elif audio_format_id:
            option = {
                'format': f'{audio_format_id}/{self.options.selected_option[1].format}',
                'outtmpl': filename_convert(f'{self.title}.{self.options.selected_option[1].format}'),
                'progress_hooks': [self.__on_progress]
            }

            output_filename = [filename_convert(f'{self.title}.{self.options.selected_option[1].format}')]
        
        else:
            return "[Error] Download Option Not Selected"
        
        print(
            f"[DOWNLOADER] Downloading Video '{self.title}'\n------------------------------\n",
            f"[DOWNLOADER] Attached Video Format-ID: {video_format_id}\n" if video_format_id else "[DOWNLOADER] No Video Attached\n",
            f" - Resolution: {self.options.selected_option[0].resolution}\n" if video_format_id else '',
            f" - Format: {self.options.selected_option[0].format}\n" if video_format_id else '',
            f"[DOWNLOADER] Attached Audio Format-ID: {audio_format_id}\n" if audio_format_id else "[DOWNLOADER] No Audio Attached\n",
            f" - Format: {self.options.selected_option[1].format}\n" if audio_format_id else '',
            sep=''
        )
        
        YoutubeDL(option).download(self.url)

        for f in output_filename:
            if os.path.exists(f):
                output_filename = f
                break
            else:
                continue
        
        if type(output_filename) == list:
            return "[Error] Output Format Error"

        if not(not output_format or output_format == output_filename[::-1].split('.')[0][::-1]):
            os.system(f'ffmpeg -i "{output_filename}" -c:v copy "{filename_convert(f"{self.title}.{output_format}")}"')
            os.remove(output_filename)

            print(
                f'\n[DOWNLOADER] Video/Audio \'{filename_convert(f"{self.title}.{output_format}")}\' downloaded successfully'
            )
        else:
            print(
                f'\n[DOWNLOADER] Video/Audio \'{output_filename}\' downloaded successfully'
            )

        return "[SUCCESS] Downloaded Success"

    def __on_progress(self, d:dict):
        if d['status'] == 'finished':
            progress = 100

        if d['status'] == 'downloading':
            progress = d['_percent_str']
            progress = float(progress[7:].replace('%\x1b[0m', ''))
        
        if self.download_progress_handler:
            self.download_progress_handler(progress)