import argparse 
import base64
import json
import os
import zlib
import urllib.parse


def decode_base64_and_inflate(b64string):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data , -15)


def deflate_and_base64_encode(bytes):
    zlibbed_str = zlib.compress(bytes.encode('ascii'))
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string).decode('ascii')


def build_links_parser(parser):
    parser.add_argument('-i', '--survey', required=True)
    parser.add_argument('-s', '--section', required=False)
    parser.add_argument('-b', '--base-url', required=False, default='https://surveyor-next.apps.triple.engineering/survey.html')
    parser.set_defaults(func=generate_links)
    return


def main():
    parser = argparse.ArgumentParser()
    build_links_parser(parser)
    args = parser.parse_args()
    generate_links(args)


def generate_links(args):
    survey = json.load(open(args.survey))
    if args.section:
        roster = json.load(open(f'spectra-data/{args.section}/roster.json'))

        print('Generating links ...')
        max_len = 0
        links = []
        for team in roster.get('Teams').values():
            # Copy the form data
            data = json.loads(json.dumps(survey))

            # Add team members to Matrix X-Axis
            x = data.get('matrix').get('x')
            for member in team.get('members'):
                x.append({
                    "id": member.get('canvas_user_id'),
                    "label": member.get('name')
                })

            minified = json.dumps(data, sort_keys=True)
            deflated = deflate_and_base64_encode(minified)
            url_safe_string = urllib.parse.quote_plus(deflated)
            link = f'{args.base_url}?data={url_safe_string}'

            if len(link) > max_len:
                max_len = len(link)

            print(f"{team['name']} - {link}", end='\n\n')
            links.append(f'<li><a href="{link}">{team["name"]}</a></li>')
        
        links = '\n\n'.join(links)
        survey_id = args.survey.split(os.sep)[-1].split('.')[0]
        with open(f'spectra-data/{args.section}/outputs/{survey_id}_links.html', 'w') as f:
            f.write(f'<ul>{links}</ul>')
    
    else:
        print('Generating link ...\n')
        minified = json.dumps(survey, sort_keys=True)
        deflated = deflate_and_base64_encode(minified)
        url_safe_string = urllib.parse.quote_plus(deflated)
        link = f'{args.base_url}?data={url_safe_string}'
        max_len = len(link)
        print(link)
    print(f'\nMax URL length is {max_len}')


if __name__ == '__main__':
    main()