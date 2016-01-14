#!/usr/bin/env python3

import json
from jinja2 import Template
from numpy import pi, sqrt

BLOCK_TEMPLATE = Template('''{{element}} GTH-NLCC2015-PBE-q{{zion}} GTH-NLCC2015-PBE
    {% for c in conf %}{{ '{:<2d}'.format(c) }}{%- endfor%}
        {{'{:<20s}'.format(rloc)}} {{'{:>1s}'.format(nloc)}} {% for c in cloc %} {{ '{:<20s}'.format(c) }}{%- endfor%}
    {%- if qcore is not none %}
    NLCC   1
        {{'{:<20s}'.format(rcore)}} 1 {{'{:<20.12f}'.format(ccore)}}
    {% endif -%}
    {{nsep}}
    {%- if sprojector is not none %}
        {{'{:<20s}'.format(sprojector[0])}} {{'{:<2d}'.format(sprojector[1])}} {%- for n in range(sprojector[1]) -%}
            {{ ' '*44*n }}{% for m in range(sprojector[1]-n) %} {{ '{:<20s}'.format(sprojector[2 + n*sprojector[1] - n*(n-1)//2 + m]) }}{% endfor %}
        {% endfor %}
    {%- endif -%}
    {%- if pprojector is not none -%}
        {{'{:<20s}'.format(pprojector[0])}} {{'{:<2d}'.format(pprojector[1])}} {%- for n in range(pprojector[1]) -%}
            {{ ' '*44*n }}{% for m in range(pprojector[1]-n) %} {{ '{:<20s}'.format(pprojector[2 + n*pprojector[1] - n*(n-1)//2 + m]) }}{% endfor %}
        {% endfor %}
    {%- endif -%}
    {%- if dprojector is not none -%}
        {{'{:<20s}'.format(dprojector[0])}} {{'{:<2d}'.format(dprojector[1])}} {%- for n in range(dprojector[1]) -%}
            {{ ' '*44*n }}{% for m in range(dprojector[1]-n) %} {{ '{:<20s}'.format(dprojector[2 + n*dprojector[1] - n*(n-1)//2 + m]) }}{% endfor %}
        {% endfor %}
    {%- endif -%}
''')

ATOMDB =      { #  s    p      d      
        "H-q1"  :  [ 1  , None , None ],
        "He-q2" :  [ 2  , None , None ],
        "Li-q1" :  [ 1  , None , None ],
        "Li-q3" :  [ 3  , None , None ],
        "Be-q2" :  [ 2  , None , None ],
        "Be-q4" :  [ 4  , None , None ],
        "B-q3"  :  [ 2  ,   1  , None ],
        "C-q4"  :  [ 2  ,   2  , None ],
        "N-q5"  :  [ 2  ,   3  , None ],
        "O-q6"  :  [ 2  ,   4  , None ],
        "F-q7"  :  [ 2  ,   5  , None ],
        "Ne-q8":   [ 2  ,   6  , None ],
        "Na-q9":   [ 3  ,   6  , None ],
        "Mg-q2":   [ 2  , None , None ],
        "Mg-q10":  [ 4  ,   6  , None ],
        "Al-q3":   [ 2  ,   1  , None ],
        "Si-q4":   [ 2  ,   2  , None ],
        "P-q5":    [ 2  ,   3  , None ],
        "S-q6":    [ 2  ,   4  , None ],
        "Cl-q7":   [ 2  ,   5  , None ],
        "Ar-q8":   [ 2  ,   6  , None ],
        "K-q9":    [ 3  ,   6  , None ],
        "Ca-q10":  [ 4  ,   6  , None ],
        "Sc-q11":  [ 4  ,   6  ,   1  ],
        "Ti-q12":  [ 4  ,   6  ,   2  ],
        "V-q13":   [ 4  ,   6  ,   3  ],
        "Cr-q14":  [ 3  ,   6  ,   5  ],
        "Mn-q15":  [ 4  ,   6  ,   5  ],
        "Fe-q16":  [ 4  ,   6  ,   6  ],
        "Co-q17":  [ 4  ,   6  ,   7  ],
        "Ni-q18":  [ 4  ,   6  ,   8  ],
        "Cu-q11":  [ 1  ,   0  ,  10  ],
        "Zn-q12":  [ 2  ,   0  ,  10  ],
        "Ga-q13":  [ 2  ,   1  ,  10  ],
        "Ge-q4":   [ 2  ,   2  , None ],
        "As-q5":   [ 2  ,   3  , None ],
        "Se-q6":   [ 2  ,   4  , None ],
        "Br-q7":   [ 2  ,   5  , None ],
        "Kr-q8":   [ 2  ,   6  , None ],
        "Rb-q9":   [ 3  ,   6  , None ],
        "Sr-q10":  [ 4  ,   6  , None ],
        "Y-q11":   [ 4  ,   6  ,   1  ],
        "Zr-q12":  [ 4  ,   6  ,   2  ],
        "Nb-q13":  [ 3  ,   6  ,   4  ],
        "Mo-q14":  [ 3  ,   6  ,   5  ],
        "Tc-q15":  [ 3  ,   6  ,   6  ],
        "Ru-q16":  [ 3  ,   6  ,   7  ],
        "Rh-q17":  [ 3  ,   6  ,   8  ],
        "Pd-q18":  [ 2  ,   6  ,  10  ],
        "Ag-q11":  [ 1  ,   0  ,  10  ],
        "Cd-q12":  [ 2  ,   0  ,  10  ],
        "In-q13":  [ 2  ,   1  ,  10  ],
        "Sn-q4":   [ 2  ,   2  , None ],
        "Sb-q5":   [ 2  ,   3  , None ],
        "Te-q6":   [ 2  ,   4  , None ],
        "I-q7":    [ 2  ,   5  , None ],
        "Xe-q8":   [ 2  ,   6  , None ],
        "Cs-q9":   [ 3  ,   6  , None ],
        "Ba-q10":  [ 4  ,   6  , None ],
        "Hf-q12":  [ 4  ,   6  ,   2  ],
        "Ta-q13":  [ 4  ,   6  ,   3  ],
        "W-q14":   [ 4  ,   6  ,   4  ],
        "Re-q15":  [ 4  ,   6  ,   5  ],
        "Os-q16":  [ 4  ,   6  ,   6  ],
        "Ir-q17":  [ 4  ,   6  ,   7  ],
        "Pt-q18":  [ 3  ,   6  ,   9  ],
        "Au-q11":  [ 1  ,   0  ,  10  ],
        "Hg-q12":  [ 2  ,   0  ,  10  ],
        "Tl-q13":  [ 2  ,   1  ,  10  ],
        "Pb-q4":   [ 2  ,   2  , None ],
        "Bi-q5":   [ 2  ,   3  , None ],
        "Po-q6":   [ 2  ,   4  , None ],
        "At-q7":   [ 2  ,   5  , None ],
        "Rn-q8":   [ 2  ,   6  , None ]}

def cconv(z, z_ion, r_core, c_core):
    return c_core * 4 * pi * (z - z_ion) / (sqrt (2 * pi) * r_core)**3

if __name__ == '__main__':

    with open('nlcc_params.json', 'r') as f:
        entries = json.load(f)

    for e in entries:
        if e['qcore'] is not None:
            zion = int(e['zion'])

            # calculate one of the NLCC coefficients, see comment in NLCC_POTENTIALS
            e['ccore'] = cconv(int(e['zatom']), zion,
                float(e['rcore']), float(e['qcore']))

        # lookup the electron configuration
        e['conf'] = [n for n in ATOMDB['{element}-q{zion}'.format(**e)][0:3] if n is not None]

        if e['sprojector'] is not None:
            e['sprojector'][1] = int(e['sprojector'][1])
            # split up coefficients into the standard coefficient set and the spin-orbital coupling (required by Abinit)
            #ncoeffs = (e['sprojector'][1]*(e['sprojector'][1] + 1)) // 2
            #e['sprojectors'] = [ e['sprojector'][2+i*ncoeffs:2+(i+1)*ncoeffs] for i in range(len(e['sprojector'][2:])//ncoeffs) ]

        if e['pprojector'] is not None:
            e['pprojector'][1] = int(e['pprojector'][1])
            # split up coefficients into the standard coefficient set and the spin-orbital coupling (required by Abinit)
            #ncoeffs = (e['pprojector'][1]*(e['pprojector'][1] + 1)) // 2
            #e['pprojectors'] = [ e['pprojector'][2+i*ncoeffs:2+(i+1)*ncoeffs] for i in range(len(e['pprojector'][2:])//ncoeffs) ]

        if e['dprojector'] is not None:
            e['dprojector'][1] = int(e['dprojector'][1])
            # split up coefficients into the standard coefficient set and the spin-orbital coupling (required by Abinit)
            #ncoeffs = (e['dprojector'][1]*(e['dprojector'][1] + 1)) // 2
            #e['dprojectors'] = [ e['dprojector'][2+i*ncoeffs:2+(i+1)*ncoeffs] for i in range(len(e['dprojector'][2:])//ncoeffs) ]

        # render the block and print
        print(BLOCK_TEMPLATE.render(**e))
