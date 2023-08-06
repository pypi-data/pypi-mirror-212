# PyArrShow

## About

Python is presently the leading language for MRI data processing and reconstruction, such as in fastMRI challenge, etc. Due to MRI data usually containing multiple dimensional aspects, such as width-height-slice-coil-dynamic-modalities(such as different b-values in DWI, and different TE images in multi-echo GRE/SE sequence), visualization of processed or reconstructed results requires checking MRI data along specific dimensions,  and this need can not be simply satisfied by standard matplotlib. Additionally, in the data preparation stage, visually checking multi-dimensional inputs and outputs is quite important and necessary.

PyArrShow attempts to provide a Python tool with a similar functionality as the Matlab arrShow project. 

## Installation

Use the package manager pip to install PyArrShow.

```
pip install PyArrShow
```

#### Installing Directly from Source

If you want to install directly from the GitHub source, clone the repository, navigate to the PyArrShow root directory and run

```
pip install -e .
```

## Examples

Here is a code example for PyArrShow

```
import pyas 
import numpy as np
nparray_5d = np.random.rand(256,344,10,5,8)
pyas.PyArrShow().show(nparray_5d)
nparray_5d_c= np.random.rand(256,344,10,5,8) + 1j*np.random.rand(256,344,10,5,8)
pyas.PyArrShow().show(nparray_5d_c)
```

## License

PyArrShow is MIT licensed, as found in the LICENSE file.