import os
import requests
import random
from sampacks.non_use_funcs import (
    image_downloader,
    image_check
)

class mainfuncs:
    def __init__(self):
        pass

    def coder(self, text):
        """
        Encodes the given text by adding random letters before and after the reversed string.

        Args:
            text (str): The text to be encoded.

        Returns:
            str: The encoded text.
        """
        random_number = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))
        text = text.lower()
        text_reverse = text[::-1]
        encoded = random_number + text_reverse + random_number
        return encoded

    def decoder(self, text):
        """
        Decodes the given text by removing the random letters added by the `coder` function.

        Args:
            text (str): The text to be decoded.

        Returns:
            str: The decoded text.
        """
        encoded = text[3:-3]
        decoded = encoded[::-1].capitalize()
        return decoded

    def words_capitalizer(self, obj, print_output=False):
        """
        Capitalizes the words in a string or a list of strings.

        Args:
            obj (str or list): The string or list of strings to capitalize.
            print_output (bool): If True, prints the capitalized words. Defaults to False.

        Returns:
            str or list: The capitalized words.
        """
        if isinstance(obj, str):
            words = obj.split()
            capitalized_words = [word.capitalize() for word in words]
            capitalized_text = ' '.join(capitalized_words)
            if print_output:
                print(capitalized_text)
            else:
                return capitalized_text
        elif isinstance(obj, list):
            capitalized_words = [word.capitalize() for word in obj]
            if print_output:
                print(capitalized_words)
            else:
                return capitalized_words

    def words_upper(self, obj, print_output=False):
        """
        Converts the words in a string or a list of strings to uppercase.

        Args:
            obj (str or list): The string or list of strings to convert.
            print_output (bool): If True, prints the converted words. Defaults to False.

        Returns:
            str or list: The converted words.
        """
        if isinstance(obj, str):
            words = obj.split()
            uppercase_words = [word.upper() for word in words]
            uppercase_text = ' '.join(uppercase_words)
            if print_output:
                print(uppercase_text)
            else:
                return uppercase_text
        elif isinstance(obj, list):
            uppercase_words = [word.upper() for word in obj]
            if print_output:
                print(uppercase_words)
            else:
                return uppercase_words

    def words_lower(self, obj):
        """
        Converts the words in a string or a list of strings to lowercase.

        Args:
            obj (str or list): The string or list of strings to convert.

        Returns:
            str or list: The converted words.
        """
        if isinstance(obj, str):
            words = obj.split()
            lowercase_words = [word.lower() for word in words]
            lowercase_text = ' '.join(lowercase_words)
            return lowercase_text
        elif isinstance(obj, list):
            lowercase_words = [word.lower() for word in obj]
            return lowercase_words
        
    def downloader(self, url, **kwargs):
        """
        Downloads a file from a given url.
        Args:
            url: Url For The File You Wanna Download.
        Kwargs:
            name: Enter The Name Of The File
            chunk: Chunck_Size For Iter_Content
            location: Where To Save The File.
        Returns:
            Downloads: The Files.
        """
        img = image_check(url)
        if type(img) == list:
            image_extension = img[1]
            image_downloader(url, image_extension, **kwargs)
        else:
            if 'name' in kwargs:
                    name = kwargs['name']     
                    raws = url.split('/')[-1]
                    join = ''.join(raws)
                    if 'extension' in kwargs:
                        name = name + kwargs['extension']
                    else:
                        extension = '.' + join.split('.')[1] 
                        name = name + extension
            else:
                name = url.split('/')[-1]

            if 'chunk' in kwargs:
                chunk_raw = kwargs['chunk']
                if type(chunk_raw) == int:
                    chunk = chunk_raw     
            else:
                chunk = 500

            if 'location' in kwargs:
                location_raw = kwargs['location']
                if os.path.exists(location_raw):
                    location = location_raw
            else:
                location = ''

            file = requests.get(url, stream=True)
            try:
                os.chdir(location)
            except OSError:
                pass
            with open(name, 'wb') as files:
                for i in file.iter_content(chunk_size=chunk):
                    files.write(i)



