import sys
import os

ap = os.path.abspath('./krutils')
print ('imported:' + ap)

sys.path.append(ap)

import logger as lgr
l = lgr.getlogger(__file__)
# print (l)
l.debug('[%%]', 123)
l.info('[%%]', 1111111111)


import utils

kl = utils.logger(__file__)
kl.info('[%%]', '우훼훼훼')

# kl = utils.logger(__file__)
# kl.info('[%%]', 'xxxxx')

