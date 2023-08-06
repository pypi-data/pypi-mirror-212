Must have `Sphinx` installed in python environment.

```
pip install Sphinx
```

To update auto-generated documentation, run:

```
sphinx-autodoc -o ./source ../architect_py
```

To update manually written documentation, update the `.rst` files in 
this directory using whatever text editor you like. `index.rst` is the
root/homepage for the generated documentation.

To update the generated HTML documentation site after any updates
to autodocs or manually written pages, run:

```
make clean && make html
```

Documentation output resides in `_build/html`.


NB: this documentation scaffolding was generated with `sphinx-quickstart`,
but there's no need to run this again ever unless your intention is to
blow away everything (including manual documentation edits) and start
over.
