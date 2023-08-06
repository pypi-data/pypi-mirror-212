from .BaseDeploy import _BaseDeploy

def __call__(model_path, backend='ort'):
    return _BaseDeploy(model_path, backend=backend)

import sys
sys.modules[__name__] = __call__