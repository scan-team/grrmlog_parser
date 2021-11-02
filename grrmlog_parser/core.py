import os
import glob
import copy
from .models import GRRMMap, EQ
from .parser_grrm_map import parser_grrm_map
from .tools_judge_grrm_log import tools_judge_grrm_log
from .tools_get_abs_fn_top import tools_get_abs_fn_top

## ----------------------------------
##  MAIN program for grrmlog_parser
## ----------------------------------
def parse(fn_rel_top):
    
    ## get absolute path for fn
    fn_abs_top=tools_get_abs_fn_top(fn_rel_top)
    
    ## judge grrm log or not
    tag_grrm_map_log=tools_judge_grrm_log(fn_abs_top)

    if tag_grrm_map_log:
        map = parser_grrm_map(fn_abs_top)
    else:
        map = GRRMMap()

    return map

