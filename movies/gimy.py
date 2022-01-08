import re
import requests
import rich
from langconv import *
from ffmpy3 import FFmpeg
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from rich.console import Console
from rich.progress import track
from rich.prompt import IntPrompt, Prompt
from rich.traceback import install


console = Console()
install(show_locals=True, suppress=[re, requests, rich, AES])

def search_for_code(key_word):
    res = requests.get(f"https://gimy.app/search/-------------.html?wd={key_word}")
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    results = soup.select('#content .details-info-min.col-md-12.col-sm-12.col-xs-12.clearfix.news-box-txt.p-0')
    result = {}
    for res in results:
        name = res.find('a').text
        info = res.select('li.col-md-12.col-sm-12.col-xs-12')
        result[name] = {}
        result[name]["id"] = res.find('a').attrs['href'].split('/')[-1][:-5]
        result[name]["status"] = info[0].text.replace("\n", ' ')
        result[name]["type"] = info[1].text.replace("\n", ' ')
        result[name]["actors"] = info[2].text.replace("\n", ' ')
        result[name]["introduction"] = info[3].text.replace("\n", ' ')
    return result

def get_source_addr(movie_code):
    '''Get the source address of the movie shown on gimy.app
    ---------------------------------------------------------

    movie_code: string, a code can be find on gimy.app url
    return: string, the source address of the movie
    '''
    base_url = "https://gimy.app/eps/{}.html"
    res = requests.get(base_url.format(movie_code))
    res.raise_for_status()
    source_address = re.findall(r'var player_data={.*"url":\s?"(.*?)",.*}', res.text)
    if source_address:
        source_address = source_address[0]
        source_address = source_address.replace("\\", '')
        console.print(f"[green]successfully find movie source address: [blue]{source_address}[/blue][/green]")
    else:
        console.print(f"[red]could not find movie source address")
    return source_address

def download_movie(source_address, save_path):
    '''Download the movie
    ----------------------

    source_address: string, the source address of the movie, which 
        can be obtained from `get_source_addr` function
    save_path: string, the path to save the downloaded movie
    '''
    def _get_real_source(source_address):
        res = requests.get(source_address)
        res.raise_for_status()
        host = source_address.split("/")[2]
        protocol = source_address.split("//")[0]
        host_address = protocol + '//' + host
        res_list = res.text.split('\n')
        if len(res_list) <= 5:
            movie_index = res_list[-2]
            real_source = host_address + movie_index
        else:
            real_source = source_address
        return real_source
    
    def _get_source_list_and_decrypt_key(real_source):
        part_list = requests.get(real_source)
        source_list = list(filter(lambda x: x.startswith('https://'), part_list.text.split('\n')))
        key = list(filter(lambda x: x.startswith("#EXT-X-KEY:"), part_list.text.split('\n')))[0]
        key_method = re.findall(r'METHOD=(.*?),', key)[0]
        if key_method != "AES-128":
            console.print(f"[red]Encrypt Method does not match AES-128, consider changing the source code")
            raise ValueError()
        key_url = re.findall(r'URI="(.*?)"', key)[0]
        key = requests.get(key_url).text        
        return source_list, key

    real_source = _get_real_source(source_address)
    source_list, key = _get_source_list_and_decrypt_key(real_source)
    result = []
    for part in track(source_list[:5], description="Getting movie ... "):
        res = requests.get(part)
        result.append(res.content)
    
    # because the result list was encrypted by AES, so we need to decrypt it
    decryptor = AES.new(key, AES.MODE_CBC, key)
    for i, res in enumerate(result):
        with open(f"{save_path}/{i}.ts", 'wb') as f:
            f.write(decryptor.decrypt(res))

def download_movie_ffmpeg(source_address, save_path):
    download_ffmpeg = FFmpeg(
        inputs={source_address: None},
        outputs={save_path: '-c copy'}
        )
    console.print(f"Running command: [red]{download_ffmpeg.cmd}")
    download_ffmpeg.run()

movie = Prompt.ask("What is the name of the movie?\n>>> ")
keyword = Converter("zh-hant").convert(movie)
console.print(f"[blue]Searching for {keyword} ... ")
search_results = search_for_code(key_word=keyword)
console.print(search_results)
code_choice = IntPrompt.ask(f"Choose? (in a order number)\n>>> ")
episode = IntPrompt.ask(f"Which episode?\n>>> ")
code = search_results[list(search_results.keys())[code_choice]]["id"] + f"-3-{episode}"
source_address = get_source_addr(code)
if source_address:
    # use the self-made function
    # download_movie(source_address, f'movies/cache')
    # or use the ffmpeg automatically
    download_movie_ffmpeg(source_address, f'movies/cache/movie.mp4')
