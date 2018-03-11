'''Check files for broken links.'''

import os
import re
import sys
import yaml
import requests

# This isn't a perfect URL matcher, but should catch the large majority of
# URLs within this project.
URL_REGEX = r'\bhttps?://[^\ \'\'\)\]\>\`\s]+'


def linkie(config):
    check_config(config)
    update_config(config)
    file_count = 0
    url_count = 0
    status_counts = {}
    broken_urls = set()

    for directory_root, directories, files in os.walk('.'):
        # Remove directories in exclude list
        processed_directories = []
        for directory in directories:
            directory_path = os.path.join(directory_root, directory)
            if directory_path not in config['exclude_directories']:
                processed_directories.append(directory)
        directories[:] = processed_directories

        for filename in files:
            if filename.endswith(config['file_types']):
                file_path = os.path.join(directory_root, filename)
                file_count += 1
                print('\nChecking file {} for URLs... '.format(file_path), end='')
                file_object = open(file_path, 'r')
                file_contents = file_object.read()
                file_object.close()
                urls = re.findall(URL_REGEX, file_contents)
                print('{} URL{} found'.format(len(urls), 's' if len(urls) != 1 else ''))
                for url in urls:
                    url_count += 1
                    print('  {}) Checking URL {} '.format(url_count, url), end='')
                    try:
                        status_code = requests.head(url).status_code
                        # If response doesn't allow HEAD request, try GET request
                        if status_code >= 400:
                            status_code = requests.get(url).status_code
                    # If connection error
                    except:
                        status_code = 999
                    print('= {} status'.format(status_code))
                    status_counts[status_code] = status_counts.get(status_code, 0) + 1
                    if status_code >= 400:
                        broken_urls.add(url)

    print('\n=============================================')
    print('SUMMARY')
    print('=============================================')
    print('{} file{} checked'.format(file_count, 's' if file_count != 1 else ''))
    print('{} URL{} found'.format(url_count, 's' if url_count != 1 else ''))

    print('\nStatus code counts')
    print('---------------------------------------------')
    for status in sorted(status_counts.keys()):
        print('{}: {}'.format(status, status_counts[status]))
    if 999 in status_counts:
        print('Status 999 refers to a connection error.')

    print('\nBroken links:')
    print('---------------------------------------------')
    if broken_urls:
        for url in broken_urls:
            print(url)
        return 1
    else:
        print('No broken links found!')
        return 0


def check_config(config):
    exclude_directories = config['exclude_directories']
    if type(exclude_directories) != list:
        raise TypeError('The exclude_directories value should be a list of directories.')
    file_types = config['file_types']
    if type(file_types) != list:
        raise TypeError('The file_types value should be a list of file extensions.')


def update_config(config):
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
        if 'exclude_directories' in custom_config:
            config['exclude_directories'] = custom_config['exclude_directories']
        if 'file_types' in custom_config:
            config['file_types'] = custom_config['file_types']
    else:
        print('Using default Linkie configuation')
    return linkie(config)


if __name__ == '__main__':
    main()
