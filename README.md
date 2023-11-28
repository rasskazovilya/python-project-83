### Hexlet tests and linter status:
[![Actions Status](https://github.com/rasskazovilya/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/rasskazovilya/python-project-83/actions)
[![Github Actions Status](https://github.com/rasskazovilya/python-project-83/workflows/test-lint/badge.svg)](https://github.com/rasskazovilya/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/6c4b520f8356d5e92547/maintainability)](https://codeclimate.com/github/rasskazovilya/python-project-83/maintainability)

## Webpage Analyzer
Webpage Analyzer is an educational project from Hexlet Python Developer course. This is a simple Flask web application used to get seo data with help of Beautiful Soup from different websites.
[Link to app on Render](https://hexlet-page-analyzer-qv2p.onrender.com)

### Requirements
- python > 3.8
- pip > 22.1
- poetry >= 1.5.1
- flask >= 3.0.0
- beautifulsoup4 >= 4.12.2
- validators >= 0.22.0
- requests >= 2.31.0
- psycopg2-binary >= 2.9.9

### Installation
- Clone this repo  
```
git clone https://github.com/rasskazovilya/python-project-83
```
- Go to repo directory  
```
cd python-project-83
```
- Install application  
```
make build
```

### Usage
Run app locally:
```
make start
```
Run app locally in debug mode:
```
make debug
```
Run app locally on development server:
```
make dev
```