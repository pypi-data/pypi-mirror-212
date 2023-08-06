# 🚀 Notebook Copilot: From Thoughts to Well-Crafted Code at Record-Speed.

Welcome to Notebook Copilot, your next-generation tool for Jupyter Notebooks. Inspired by GitHub Copilot, Notebook
Copilot is designed to help engineers and data scientists in developing professional, high-quality notebooks. It's like
having your personal AI-powered assistant that helps you navigate through the Jupyter universe, seamlessly
generating code and markdown cells based on your inputs.

Imagine not having to start with a blank notebook every time. Sounds dreamy, right?

## Demo
<div><iframe src="https://www.loom.com/embed/d347052d3403412083cf4ea75b2e2cd4" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div>

## Key Features

- **`%copilot` magic function**: Continues the notebook for you, generating professional code and markdown cells, making
  blank notebooks a thing of the past.
- **`%generate` magic function**: Utilizes AI to generate the next cell from your comments. Just give it a hint, and
  it'll do the heavy lifting for you.
- **`%explain` magic function**: Produces a markdown cell that elaborates the functionality of the current cell. Don't
  just write code, understand it thoroughly!

## Installation

You can install Notebook Copilot directly from PyPI:

```bash
pip install notebook_copilot
```

## Usage
Load the Notebook Copilot extension in your Jupyter notebook:

```python
%load_ext notebook_copilot
```

Now you're ready to use the magic functions:

```python
# Enter Assistant Mode, will continue the notebook for you
%copilot
```

```python
# Generate the next cell code
%%generate plot the confusion matrix using for the model
```

```python
# Explain the current cell
%%explain
# some code…
```

## Roadmap

- [x] **Copilot Magic Function**: Continues the notebook for you, generating professional code and markdown cells, making
  blank notebooks a thing of the past.
- [x] **Generate Magic Function**: Turn Your Comments into Code
- [x] **Explain Magic Function**: Generate Markdown Cells that Explain Your Code
- [ ] Update underlying strategy to ToT
- [ ] AI-Powered Code completion inside cells
    

## Contributing
We appreciate all contributions. If you're planning to contribute back bug-fixes, please do so without any further discussion. If you plan to contribute new features, utility functions, or extensions to the core, please first open an issue and discuss the feature with us.

## License
Notebook Copilot is MIT licensed, as found in the LICENSE file.