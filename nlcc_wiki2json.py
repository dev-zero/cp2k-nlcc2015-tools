#!/usr/bin/env python3

import json
import lxml.html
import regex

URL   = 'http://bigdft.org/Wiki/index.php?title=New_Soft-Accurate_NLCC_pseudopotentials'
XPATH = '//*[@id=\'mw-content-text\']/pre'
BLOCK_RE = regex.compile(r'''
[\w\s]+\((?P<element>\w{1,2})\)[^\n]+\n
(   # optional line for spin-polarized systems
    [\t ]*spin-polarized
    [\t ]+(?P<method>\d+)
    [\t ]+(?P<ncov>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)
    ([\t ]+(?P<rcov>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?))+
    .* # catch everything else after the last number
    \n
)?
[\t ]*(?P<zatom>\d+)\s+(?P<zion>\d+)\s+(?P<date>\d{8})\s[^\n]+\n
[\t ]*(?P<pspcode>[^\s]+)\s+(?P<ixc>[^\s]+)\s+(?P<lmax>[^\s]+)\s+(?P<lloc>\S+)\s+(?P<mmax>[^\s]+)\s+(?P<rwell>[^\s]+)[^\n]+\n
[\t ]*(?P<rloc>\S+)\s+(?P<nloc>\S+)(\s+(?P<cloc>\S+))+\s*rloc[^\n]+\n
[\t ]*(?P<nsep>\d)[^\n]+\n
(
    ^([\t ]+(?P<sprojector>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)){3,}[\t ]+s-projector[\t ]*\n
    (
        (
            # look floating point number with some space in front
            ( [\t ]+ (?P<sprojector>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?) )
        )+ # and require at least one
        \s*\n # they may be followed by some space, but then there must be a newline, but nothing else
    )* # this entire section is optional (only one line of projector coefficients)
)? # there can be 0 or 1 s-projector
(
    ^([\t ]+(?P<pprojector>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)){3,}[\t ]+p-projector[\t ]*\n
    (
        (
            # look floating point number with some space in front
            ( [\t ]+ (?P<pprojector>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?) )
        )+ # and require at least one
        \s*\n # they may be followed by some space, but then there must be a newline, but nothing else
    )* # this entire section is optional (only one line of projector coefficients)
)? # there can be 0 or 1 p-projector
(
    ^([\t ]+(?P<dprojector>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)){3,}[\t ]+d-projector[\t ]*\n
    (
        (
            # look floating point number with some space in front
            ( [\t ]+ (?P<dprojector>[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?) )
        )+ # and require at least one
        \s*\n # they may be followed by some space, but then there must be a newline, but nothing else
    )* # this entire section is optional (only one line of projector coefficients)
)? # there can be 0 or 1 d-projector
(
    # match at most one NLCC parameter set
    ^[\t ]+(?P<rcore>\S+)\s+(?P<qcore>\S+)\s+rcore.*\n
)?
\s* # now consume any more whitespace (required for fullmatch)
        ''', regex.X | regex.M | regex.V1)
SECTIONNAME_RE=regex.compile(r'''
psppar\.(?P<element>\w+)\s+\((?P<config>q\d+)\)
''', regex.X)

def simplify_array(arr):
    '''
    Convert empty arrays to None's
    and single-valued arrays to single values
    '''
    if arr is None:
        return None

    if len(arr) == 0:
        return None
    elif len(arr) == 1:
        return arr[0]

    return arr

if __name__ == '__main__':

    # let lxml fetch the the url and apply the xpath expression
    elements = lxml.html.parse(URL).xpath(XPATH)

    entries = []

    for e in elements:
        block_m = BLOCK_RE.fullmatch(e.text)

        sectionname = e.getprevious().text_content().strip()
        sectionname_m = SECTIONNAME_RE.fullmatch(sectionname)

        if block_m is None or sectionname_m is None:
            print("Parsing failed for one section: {}".format(sectionname))
            continue

        entry = { k: simplify_array(v)
                for k, v in block_m.capturesdict().items() }

        if sectionname_m.group('element') != block_m.group('element'):
            print("WARNING: element symbol in pseudo description does not match section title for '{}', using section title element instead".format(sectionname))
            entry['element'] = sectionname_m.group('element')

        entries.append(entry)

    with open('nlcc_params.json', 'w') as f:
        json.dump(entries, f, indent=2, sort_keys=True)
