# htm_wl_demo

### Installing htm.core (required dependency)

Due to the native C++ code dependencies, `htm-core` can be challenging to install directly via pip on some systems. Follow these recommended steps:

#### Option 1 (recommended for most users):

```bash
pip install --upgrade pip wheel setuptools
pip install htm-core
```

#### Option 2 (compile from source):

```bash
brew install cmake ninja boost python3
git clone https://github.com/htm-community/htm.core.git
cd htm.core
python htm_install.py install
```