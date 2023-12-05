#!/usr/bin/env python3

# This script is a pre-commit hook for the Overleaf submodule. It gets copied to
# the hooks folder when the sync.sh script is run for the first time. Together
# with the file preserve-cite-keys.csl it enables the user to switch from
# formatting references using RStudio to uploading the cite keys and using
# Overleaf to format references, which may be preferable when submitting
# a manuscript for publication.

import os
import re

# Make figure paths relative.
working_directory = os.getcwd()

with open('main.tex', 'r') as input_file:
    input_text = input_file.read()

relative_paths = input_text.replace(working_directory, '.')

# Format references if preserve-cite-keys.csl is being used.
def format_reference(match_object):
    return (
        match_object
            .group(0)
            .replace('@STARTCITE@', '\cite{')
            .replace('\\_', '_')
            .replace('@ENDCITE@', '}')
    )

formatted_references = re.sub('@STARTCITE@.*@ENDCITE@', format_reference, relative_paths)

# Format bibliography if preserve-cite-keys.csl is being used.
if '@BIBLIOGRAPHYLOCATION@' in formatted_references:
    formatted_references = re.sub(r'\\hypertarget{refs}{}\n\\begin{CSLReferences}.*\\end{CSLReferences}',
                                    r'\\printbibliography', formatted_references, flags=re.DOTALL)

# Write the formatted file to disk.
with open('main.tex', 'w') as output_file:
    output_file.write(formatted_references)
