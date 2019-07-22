import os
import sys
import ffmpeg
import logging
import argparse
import subprocess
from guessit import guessit


class DuplicateString(str):
    def __hash__(self):
        return hash(str(id(self)))


def find_streams(probe, preferred_lang):
    vstream = 0
    astream = 0
    alang = 'unknown'
    achannels = 0
    found_preferred = False

    for s in probe['streams']:
        if s.get('codec_type'):
            if s['codec_type'] == 'video':
                vstream = s['index']

            if s['codec_type'] == 'audio':
                tags = s.get('tags')

                if tags.get('language'):
                    achannels = int(s['channels'])
                    if tags.get('language') == preferred_lang:
                        found_preferred = True
                        astream = s['index']
                        alang = tags.get('language')
                    elif not found_preferred:
                        if tags.get('language') == 'eng' and s['channels'] > achannels:
                            achannels = s['channels']
                            astream = s['index']
                            alang = tags.get('language')

                if astream == 0:
                    astream = s['index']

    logger.debug('Selected video stream {0} and audio stream {1} (Lang: {2}, Channels: {3})'.format(vstream, astream, alang, achannels))

    return vstream, astream


def find_filename(path):
    guess = guessit(path)
    filename = ''

    if guess.get('title') is not None:
        filename += guess['title']

        if guess.get('year') is not None:
            filename += ' ({0})'.format(guess['year'])

    return filename

def find_files(path):
    whitelist = ('.mkv', '.avi', '.mp4')
    paths = []
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith(whitelist):
                paths.append(fname)

    return paths


def main(args):
    incoming = args.incoming
    outgoing = args.outgoing
    preferred_lang = 'nor'

    logger.info('Processing directory: {0}'.format(incoming))

    for f in find_files(incoming):
        file_base = os.path.basename(f)
        filename, ext = os.path.splitext(file_base)

        logger.info('Processing file: {0}'.format(file_base))

        new_filename = find_filename(f)
        if not new_filename:
            new_filename = filename

        outfile = '{0}/{1}.avi'.format('/output', new_filename)
        logger.info('File destination: {0}'.format(outfile))

        probe = ffmpeg.probe(f)
        vstream, astream = find_streams(probe, preferred_lang)

        try:
            (ffmpeg
                .input(f)
                .output(outfile,
                        **{DuplicateString('map'): '0:{0}'.format(vstream),
                           DuplicateString('map'): '0:{0}'.format(astream),
                           'c:v': 'libxvid',
                           'vf': 'scale=720:406',
                           'qscale:v': 7,
                           'pix_fmt': 'yuv420p',
                           'sws_flags': 'lanczos',
                           'c:a': 'ac3',
                           'b:a': '192k'
                          })
                .global_args('-v', 'quiet', '-stats')
                .overwrite_output()
                .run())
        except ffmpeg.Error as e:
            logger.error(e.stderr)
            sys.exit(1)

        logger.info('Done processing: {0}'.format(new_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('incoming', type=str, help='input directory')
    parser.add_argument('outgoing', type=str, help='output directory')
    parser.add_argument("-v", "--verbose", help="Set loglevel to debug", action="store_true")
    args = parser.parse_args()

    logger = logging.getLogger('rseConverter')
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    main(args)
