import sys
from modules.pipeline_module import *


def parse_line(num):
    """After the html index is generated, we can access his datas"""
        line = corrector(open("failed.html", "r").readlines()[num-1])
            line = corrector(line)
                print(line)
                    res = parser.parse(line)
                        if res is not None:
                                res = unfold_substructures(res)
                                        return createTriplet(res)
                                            else:
                                                    return None


                                                    print(parse_line(8))
                                                    print(parse_line(8))
