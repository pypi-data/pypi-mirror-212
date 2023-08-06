# Sub_Funcs 
import os
import requests

def image_downloader(url, extension, **kwargs):
    """
        Downloads a file from a given url.
        Args:
            url: Url For The File You Wanna Download.
        Kwargs:
            name: Enter The Name Of The Image.
            chunk: Chunck_Size For Iter_Content.
            location: Where To Save The Image.
        Returns:
            The Downloaded Image
    """

    if 'name' in kwargs:
        name = kwargs['name'] + extension
    else:
        name = 'default.png' 
    
    if 'chunk' in kwargs:
        chunk = kwargs['chunk']
    else:
        chunk = 500

    if 'location' in kwargs:
        location = kwargs['location']
    else:
        location = ''

    try:
        os.chdir(location)
    except OSError:
        pass
    request = requests.get(url, stream=True)
    with open(name, 'wb') as file:
        for i in request.iter_content(chunk_size=chunk):
            file.write(i)


def image_check(url):
    if url.split('/')[2] == 'encrypted-tbn0.gstatic.com' or url.endswith('.png') or ''.join(url.split('/')[1]).startswith('png'): 
        extension = '.png'
        return [True, extension]
    elif url.endswith('.jpg') or ''.join(url.split('/')[1]).startswith('jpg'): 
        extension = '.jpg'
        return [True, extension]
    elif url.endswith('.jpeg') or ''.join(url.split('/')[1]).startswith('jpeg'): 
        extension = '.jpeg'
        return [True, extension]
    else:
        return False


