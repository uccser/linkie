'''Check files for broken links.'''

import os
import re
import sys
import yaml
import requests

# This isn't a perfect URL matcher, but should catch the large majority of URLs.
URL_REGEX = r'(https?|ftp)://[^\s/$.?#].[^\s`\'\"\]>}]*'

class Linkie:

    def __init__(self, config):
        self.file_count = 0
        self.url_count = 0
        self.status_counts = {}
        self.broken_urls = set()
        self.directory = '.'

        self.check_config(config)
        self.process_config(config)
        self.traverse_directory()
        self.print_summary()

    def traverse_directory(self):
        for directory_root, directories, files in os.walk(self.directory):
            # Remove directories in exclude list
            processed_directories = []
            for directory in directories:
                directory_path = os.path.join(directory_root, directory)
                if directory_path not in self.config['exclude_directories']:
                    processed_directories.append(directory)
            directories[:] = processed_directories

            for filename in files:
                if filename.endswith(self.config['file_types']):
                    check_file(os.path.join(directory_root, filename))


    def check_file(self, file_path):
        self.file_count += 1
        print('\nChecking file {} for URLs... '.format(file_path), end='')
        file_object = open(file_path, 'r')
        file_contents = file_object.read()
        file_object.close()
        urls = re.findall(URL_REGEX, file_contents)
        print('{} URL{} found'.format(len(urls), 's' if len(urls) != 1 else ''))
        for url in urls:
            # Remove extra trailing bracket if link containing brackets
            # Within Markdown link syntax.
            # [Wikipedia link](http://foo.com/blah_blah_(wikipedia))
            if url.endswith(')') and url.count('(') < url.count(')'):
                url = url[:-1]
            # Remove trailing characters
            url = url.rstrip('!"#$%&\'*+,-./@:;=^_`|~')
            self.url_count += 1
            print('  {}) Checking URL {} '.format(self.url_count, url), end='')
            try:
                status_code = requests.head(url).status_code
                # If response doesn't allow HEAD request, try GET request
                if status_code >= 400:
                    status_code = requests.get(url).status_code
            # If connection error
            except:
                status_code = 999
            print('= {} status'.format(status_code))
            self.status_counts[status_code] = self.status_counts.get(status_code, 0) + 1
            if status_code >= 400:
                self.broken_urls.add(url)

    def print_summary(self):
        print('\n=============================================')
        print('SUMMARY')
        print('=============================================')
        print('{} file{} checked'.format(self.file_count, 's' if self.file_count != 1 else ''))
        print('{} URL{} found'.format(self.url_count, 's' if self.url_count != 1 else ''))

        print('\nStatus code counts')
        print('---------------------------------------------')
        for status in sorted(self.status_counts.keys()):
            print('{}: {}'.format(status, self.status_counts[status]))
        if 999 in self.status_counts:
            print('Status 999 refers to a connection error.')

        print('\nBroken links:')
        print('---------------------------------------------')
        if self.broken_urls:
            for url in self.broken_urls:
                print(url)
            return 1
        else:
            print('No broken links found!')
            return 0


    def check_config(self, config):
        exclude_directories = config['exclude_directories']
        if type(exclude_directories) != list:
            raise TypeError('The exclude_directories value should be a list of directories.')
        file_types = config['file_types']
        if type(file_types) != list:
            raise TypeError('The file_types value should be a list of file extensions.')


    def process_config(self, config):
        exclude_directories = config['exclude_directories']
        for i in range(len(exclude_directories)):
            directory = exclude_directories[i]
            directory = os.path.join('./', directory)
            if directory.endswith('/'):
                directory = directory[:-1]
            exclude_directories[i] = directory
        config['exclude_directories'] = exclude_directories

        file_types = config['file_types']
        for i in range(len(file_types)):
            if not file_types[i].startswith('.'):
                file_types[i] = '.' + file_types[i]
        config['file_types'] = tuple(file_types)
        self.config = config


def main():
    config = {
        'exclude_directories': [
            '.git/',
            'docs/build/',
        ],
        'file_types': [
            'html',
            'md',
            'rst',
            'txt',
        ],
    }
    if len(sys.argv) > 1:
        config_filepath = sys.argv[1]
        print('Using Linkie configuration file {}'.format(config_filepath))
        config_file = open(config_filepath, 'r')
        custom_config = yaml.load(config_file)
        config_file.close()
        for key in config.keys():
            if key in custom_config:
                config[key] = custom_config[key]
    else:
        print('Using default Linkie configuation')
    return linkie(config)


if __name__ == '__main__':
    main()
