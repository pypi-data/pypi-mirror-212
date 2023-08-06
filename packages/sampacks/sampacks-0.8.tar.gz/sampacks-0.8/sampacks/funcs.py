import os
import requests
import random
import time
from win10toast import ToastNotifier
from sampacks.non_use_funcs import (
    image_downloader,
)

# Declarations

toaster = ToastNotifier()

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
        
    def image_check(self, url):
        valid_extensions = ('png', 'jpg', 'jpeg', 'webp', 'svg')
        valid_domains = ('encrypted-tbn0.gstatic.com', 'unsplash', 'pexels', 'image')
        check = None

        for i in valid_extensions:
            if url.split('/')[1] != '' and url.split('/')[1].startswith(i):
                check = True
            elif url.split('/')[1] != '' and url.split('/')[2].startswith(i):
                check = True
            else:
                check = False

        if any(url.endswith(ext) for ext in valid_extensions) or any(domain in url for domain in valid_domains) or check == True:
            return True
        return False

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
            0.8
        """

        if mainfuncs.image_check(self, url) == True:
            image_downloader(url, **kwargs)
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


    def reminder(timing, message, title):
        """
        Reminds User A Specific Message On Certain Time.
        Args:
            timing: Intervals Between Reminder
            message: Message To Reminded
            title: Title Of The Reminder
        Returns:
            Reminder As Windows Notification.
        """
        toaster.show_toast(title, message, duration=timing, threaded=True)
        while toaster.notification_active:
            time.sleep(1)

