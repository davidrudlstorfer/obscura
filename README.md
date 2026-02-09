# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/davidrudlstorfer/obscura/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                              |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------- | -------: | -------: | ------: | --------: |
| src/obscura/\_\_init\_\_.py                       |        0 |        0 |    100% |           |
| src/obscura/core/\_\_init\_\_.py                  |        0 |        0 |    100% |           |
| src/obscura/core/convert\_vtu\_to\_stl.py         |       15 |       15 |      0% |      3-26 |
| src/obscura/core/rendering/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| src/obscura/core/rendering/background.py          |        9 |        6 |     33% |     10-15 |
| src/obscura/core/rendering/camera.py              |       14 |       10 |     29% |     17-31 |
| src/obscura/core/rendering/lighting.py            |       23 |       18 |     22% |13-38, 43-49 |
| src/obscura/core/rendering/material.py            |       11 |        8 |     27% |     10-18 |
| src/obscura/core/rendering/object\_settings.py    |       17 |       11 |     35% |12-14, 19-26, 31-34 |
| src/obscura/core/rendering/render\_settings.py    |       24 |       20 |     17% |     11-37 |
| src/obscura/core/rendering/rendering\_pipeline.py |       23 |        0 |    100% |           |
| src/obscura/core/run.py                           |       12 |        0 |    100% |           |
| src/obscura/core/utilities.py                     |       33 |        2 |     94% |     92-93 |
| src/obscura/main.py                               |       21 |        1 |     95% |        24 |
| **TOTAL**                                         |  **202** |   **91** | **55%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/davidrudlstorfer/obscura/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/davidrudlstorfer/obscura/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/davidrudlstorfer/obscura/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/davidrudlstorfer/obscura/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdavidrudlstorfer%2Fobscura%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/davidrudlstorfer/obscura/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.