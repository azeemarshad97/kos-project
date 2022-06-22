import sys
from modules.pipeline_module import *

# Index file selection (default Index_1543.docx)
if len(sys.argv) == 1:
    name = "Index_1543.docx"
else:
    name = str(sys.argv[1])

# 1) docx -> html
file_name_html = docx_to_html(name)

# 2) html -> triple
tab = html_to_triple(file_name_html)

# 3) triple -> owl
triple_to_owl(tab)
