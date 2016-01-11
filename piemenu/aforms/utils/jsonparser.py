import re
import json

# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
    )


def parse(filename):
    """ Strips comments from given file returning a json object. """
    with open(str(filename)) as f:
        content = ''.join(f.readlines())

        # Looking for comments
        match = comment_re.search(content)
        while match:
            # single line comment
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

        return json.loads(content)


if __name__ == '__main__':
    parse_json('G:/dev/pyside/menusystem/menusystem/template.piemenu')
