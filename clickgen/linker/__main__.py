from contextlib import contextmanager
from difflib import SequenceMatcher as SM
import itertools
import json
import os
import tempfile

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'data.json')


@contextmanager
def cd(path):
    CWD = os.getcwd()

    os.chdir(path)
    try:
        yield
    except:
        print('Exception caught: %s' % sys.exc_info()[0])
    finally:
        os.chdir(CWD)


def match_to_directory(name: str, directory: list) -> str:
    compare_ratio = 0.5
    match = name

    for word in directory:
        ratio = SM(None, name.lower(), word.lower()).ratio()
        if ratio > compare_ratio:
            compare_ratio = ratio
            match = word

    return match


def load_data() -> [list]:
    with open(data_file) as f:
        data = json.loads(f.read())

    cursors = data['cursors']
    all = list(itertools.chain.from_iterable(cursors))

    return cursors, all


def symlink(target, link_name, overwrite=False):
    '''
    Create a symbolic link named link_name pointing to target.
    If link_name exists then FileExistsError is raised, unless overwrite=True.
    When trying to overwrite a directory, IsADirectoryError is raised.
    
    ref => https://stackoverflow.com/a/55742015
    '''

    if not overwrite:
        os.symlink(target, link_name)
        return

    link_dir = os.path.dirname(link_name)

    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)

        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass

    try:
        if os.path.isdir(link_name):
            raise IsADirectoryError(
                f"Cannot symlink over existing directory: '{link_name}'")
        os.replace(temp_link_name, link_name)
    except:
        if os.path.islink(temp_link_name):
            os.remove(temp_link_name)
        raise


def link_cursors(dir: str, win=False) -> None:
    dir = os.path.abspath(dir)
    isExists = os.path.exists(dir)

    # user have cursors fot symblink
    cursors = []

    try:
        if isExists == False:
            raise FileNotFoundError('x11 directory not found')

        for file in os.listdir(dir):
            cursors.append(file)

        if (len(cursors) <= 0):
            raise FileNotFoundError('directory is empty')

    except FileNotFoundError as err:
        print('Error: ', err)

    known_cursors, all_cursors = load_data()

    # rename cursor with proper name
    for index, cursor in enumerate(cursors):
        fix_cur = match_to_directory(cursor, all_cursors)

        if fix_cur not in all_cursors:
            print('Warning: %s is unknown cursor' % fix_cur)

        elif (fix_cur != cursor):
            old_path = os.path.join(dir, cursor)
            new_path = os.path.join(dir, fix_cur)
            os.rename(old_path, new_path)

            cursors[index] = fix_cur

            print('Fixed: %s ==> %s' % (cursor, fix_cur))

    # For relative links
    if (win == False):
        with cd(dir):
            for cursor in cursors:
                for relative in known_cursors:
                    if cursor in relative:
                        # remove source cursor
                        relative.remove(cursor)

                        # links to other if not empty
                        if len(relative) != 0:
                            for link in relative:
                                src = './' + cursor
                                dst = './' + link
                                symlink(src, dst, overwrite=True)
                            print('symblink: %s ==> ' % (cursor), *relative)
