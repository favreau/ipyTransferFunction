# Transfer Function
Transfer function editor widget for Jupyter Notebook

## Installation

```sh
virtualenv env
. ./env/bin/activate
pip install -r requirements.txt
```

## Usage (in Jupyter notebook)

### Create widget

```python
from ipyTransferFunction import TransferFunctionEditor

def display_palette_info(transfer_function):
    print(transfer_function.data_range)

tf = TransferFunctionEditor(
    name='rainbow', size=32, alpha=0.5, 
    continuous_update=False, on_change=display_palette_info)
```

### Change palette

```python
tf.set_palette('seismic')
```

### Set value range
```python
tf.set_range((0,255))
```

## Screenshot

![transfer_function_editor](/doc/transfer_function_editor.png)
