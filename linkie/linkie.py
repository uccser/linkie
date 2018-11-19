'''Check files for broken links.'''

import os
import re
import sys
import yaml
import logging
import requests
from multiprocessing.dummy import Pool as ThreadPool

# This isn't a perfect URL matcher, but should catch the large majority of URLs.
# This now matches URLs presented in the format defined in the CSU Writing Guide
# as of 13/11/2018 (https://cs-unplugged.readthedocs.io/en/latest/author/writing_guide.html)
# as well as formats used in the code for the guide itself.
# As such, URLs will be matched if and only if they have any one of the following prefixes: [=", (, <, ' '(a space)]
URL_REGEX = r'(?:\=\"|\(|\<| )(?:https?|ftp)://[^\s`\'\"\]\)>}]+'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
}
THREADS = 12


class Linkie:

    def __init__(self, config=None, config_file_path=None):
        self.file_count = 0
        self.status_counts = {}
        self.urls = dict()
        self.unchecked_urls = []
        self.directory = '.'
        self.pool = ThreadPool(THREADS)
        if not config and config_file_path:
            logging.info('Using Linkie configuration file {}'.format(config_file_path))
            config = self.read_config(config_file_path)
        elif config:
            logging.info('Using custom Linkie settings via Python constructor')
        elif not config and not config_file_path:
            logging.info('Using default Linkie configuation')
        config = self.check_config(config)
        self.config = self.process_config(config)

    def read_config(self, config_file_path):
        config_file = open(config_file_path, 'r')
        config = yaml.load(config_file)
        config_file.close()
        return config

    def check_config(self, config):
        default_config = {
            'exclude-directories': [
                '.git/',
                'docs/build/',
            ],
            'file-types': [
                'html',
                'md',
                'rst',
                'txt',
            ],
            'skip-urls': [],
        }
        if config:
            if config.get('exclude-directories'):
                if type(config['exclude-directories']) != list:
                    raise TypeError('The exclude-directories value should be a list of directories.')
            if config.get('file-types'):
                if type(config['file-types']) != list:
                    raise TypeError('The file-types value should be a list of file extensions.')
            if config.get('skip-urls'):
                if type(config['skip-urls']) != list:
                    raise TypeError('The skip-urls value should be a list of URLs to skip.')
            for key in config.keys():
                if key in config:
                    default_config[key] = config[key]
        return default_config

    def process_config(self, config):
        exclude_directories = config['exclude-directories']
        for i in range(len(exclude_directories)):
            directory = exclude_directories[i]
            directory = os.path.join('./', directory)
            if directory.endswith('/'):
                directory = directory[:-1]
            exclude_directories[i] = directory
        config['exclude-directories'] = exclude_directories

        file_types = config['file-types']
        for i in range(len(file_types)):
            if not file_types[i].startswith('.'):
                file_types[i] = '.' + file_types[i]
        config['file-types'] = tuple(file_types)
        return config

    def count_broken_links(self):
        count = 0
        for url, url_data in self.urls.items():
            if url_data['broken']:
                count += 1
        return count

    def run(self):
        self.traverse_directory()
        self.traverse_connection_errors()
        self.print_summary()
        if self.count_broken_links():
            return 1
        else:
            return 0

    def traverse_directory(self):
        for directory_root, directories, files in os.walk(self.directory):
            # Remove directories in exclude list
            processed_directories = []
            for directory in directories:
                directory_path = os.path.join(directory_root, directory)
                if directory_path not in self.config['exclude-directories']:
                    processed_directories.append(directory)
            directories[:] = processed_directories

            for filename in files:
                if filename.endswith(self.config['file-types']):
                    self.search_file(os.path.join(directory_root, filename))
        self.pool.map(self.check_link, self.unchecked_urls)
    
    def traverse_connection_errors(self):
        connect_errors = []
        for url, url_data in self.urls.items():
            if str(url_data['status']) == 'ConnectionError':
                connect_errors.append(url)
        for url in connect_errors:
            self.urls.__delitem__(url)
        if len(connect_errors):
            logging.info('Rechecking {} link{} that returned ConnectionError... '.format(len(connect_errors), 's' if len(connect_errors) != 1 else ''))
            self.pool.map(self.check_link, connect_errors)


    def search_file(self, file_path):
        self.file_count += 1
        file_message = 'Checking file {} for URLs... '.format(file_path)
        file_object = open(file_path, 'r')
        file_contents = file_object.read()
        file_object.close()
        urls = re.findall(URL_REGEX, file_contents)
        logging.info('{}{} URL{} found'.format(file_message, len(urls), 's' if len(urls) != 1 else ''))
        self.unchecked_urls += urls

    def check_link(self, url):
        # Remove trailing characters
        url = url.rstrip('> !"#$%&\'*+,-./@:;=^_`|~').lstrip(' <(=\"')
        # Remove extra trailing bracket if link containing brackets
        # within Markdown link syntax.
        # [Wikipedia link](http://foo.com/blah_blah_(wikipedia))
        if url.count('('):
            url += url.count('(') * ')'
        message = '  - Checking URL {} '.format(url)
        if url in self.config['skip-urls']:
            message += '= skipping URL (as defined in config file)'
        elif url not in self.urls:
            try:
                status_code = requests.head(url, headers=HEADERS).status_code
                # If response doesn't allow HEAD request, try GET request
                if status_code >= 400:
                    status_code = requests.get(url, headers=HEADERS).status_code
            # If connection error
            except Exception as e:
                status_code = str(type(e).__name__)

            if type(status_code) == str:
                message += '= {}'.format(status_code)
            else:
                message += '= {} status'.format(status_code)

            if type(status_code) == str or status_code >= 400:
                self.save_url(url, status_code, True)
            else:
                self.save_url(url, status_code, False)
        else:
            message += '= {} (already checked)'.format(self.urls[url]['status'])
        logging.info(message)

    def save_url(self, url, status_code, broken):
        self.urls[url] = {
            'broken': broken,
            'status': status_code,
        }
    
    def collect_status_counts(self):
        for _, url_data in self.urls.items():
            status_code = str(url_data['status'])
            self.status_counts[status_code] = self.status_counts.get(status_code, 0) + 1

    def print_summary(self):
        number_broken_links = self.count_broken_links()
        self.collect_status_counts()

        logging.info('=============================================')
        logging.info('SUMMARY')
        logging.info('=============================================')
        logging.info('{} file{} checked'.format(self.file_count, 's' if self.file_count != 1 else ''))
        logging.info('{} unique URL{} found'.format(len(self.urls), 's' if len(self.urls) != 1 else ''))
        logging.info('{} broken link{} found'.format(number_broken_links, 's' if number_broken_links != 1 else ''))

        logging.info('---------------------------------------------')
        logging.info('Status code counts')
        logging.info('---------------------------------------------')
        for status in sorted(self.status_counts.keys()):
            logging.info('{}: {}'.format(status, self.status_counts[status]))
        if 999 in self.status_counts:
            logging.info('Status 999 refers to a connection error.')

        logging.info('---------------------------------------------')
        logging.info('Broken links')
        logging.info('---------------------------------------------')
        if number_broken_links:
            for url, url_data in self.urls.items():
                if url_data['broken']:
                    logging.info('{}: {}'.format(url_data['status'], url))
        else:
            logging.info('No broken links found!')


def main():
    config_filepath = None
    if len(sys.argv) > 1:
        config_filepath = sys.argv[1]
    linkie = Linkie(config_file_path=config_filepath)
    return linkie.run()


if __name__ == '__main__':
    main()

