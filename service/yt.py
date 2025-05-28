from yt_dlp import YoutubeDL
import shutil
import os
import re

class Yt:
    def __init__(self):
        self.error = False
        self.users = {}
        pass
    def download(self, playlist, type, url, user):

        self.users[user] = {'status': 'Vídeo em processamento...'}

        def progress_hook(d):
            if d['status'] == 'downloading':
                info = d['info_dict']
                title = info.get('title')
                fmt = info.get('format', '')
                frag = f"(frag {d.get('fragment_index', '?')}/{d.get('fragment_count', '?')})" if d.get('fragment_index') else '(concluindo download)'
                self.users[user] = {'status': f'{title}[{fmt}] {frag}'}
            elif d['status'] == 'finished':
                info = d['info_dict']
                title = d['info_dict'].get('title')
                fmt = info.get('format', '')
                self.users[user] = {'status': f'{title}[{fmt}] foi processado com sucesso.'}

        outputPath = f'./files/{user}/%(playlist_title)s/%(title)s.%(ext)s' if playlist else f'./files/{user}/%(title)s.%(ext)s'

        ydl_opts_audio = {
            'yes_playlist': playlist,
            'outtmpl': outputPath,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0', 
            }],
            'progress_hooks': [progress_hook],
            'quiet': True,
            'progress_with_newline': True,
            'no_color': True
        }

        ydl_opts_video = {
            'yes_playlist': playlist,
            'outtmpl': outputPath,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'recode_video': 'mp4',
            'progress_hooks': [progress_hook],
            'quiet': True,
            'progress_with_newline': True,
            'no_color': True
        }

        if playlist == False:

            opts = ydl_opts_video if type == 1 else ydl_opts_audio

            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl._prepare_filename(info)
                self.users[user] = {'status': 'O download do arquivo será iniciado em instantes.', 'file': os.path.basename(filename if type == 1 else filename.replace('webm', 'mp3'))}    
                return True
        else:

            opts = ydl_opts_video if type == 1 else ydl_opts_audio

            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl._prepare_filename(info)
                originPath = filename.replace('NA/', '').replace('.NA', '/')
                self.sanitizeFolderFiles(originPath)
                newPath = shutil.make_archive(originPath, 'zip', originPath)
                shutil.rmtree(originPath)
                self.users[user] = {'status': 'O download do arquivo será iniciado em instantes.', 'file': os.path.basename(newPath)}
                return True

        self.error = True
        return False
                
    def checkDownload(self, user):
        if not self.error:
            if user in self.users:
                return self.users[user]
            else:
                return ''
        else:
            return 'error'
        
    def setErrorToTrue(self):
        self.error = True

    def sanitizeFolderFiles(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for name in files:
                safeName = re.sub(r'[^\w\s\-.]', '_', name, flags=re.UNICODE)
                if name != safeName:
                    os.rename(os.path.join(root, name), os.path.join(root, safeName))


