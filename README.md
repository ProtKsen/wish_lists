This application allows users to create a collection of things they would like to receive as a gift. Users can add each other as friends and view friends' wishlists.

home page|login|profile
:-:|:-:|:-:
![Alt-текст](https://github.com/ProtKsen/wish_lists/blob/main/screenshots/background.png?raw=true) | ![Alt-текст](https://github.com/ProtKsen/wish_lists/blob/main/screenshots/auth.png?raw=true) | ![Alt-текст](https://github.com/ProtKsen/wish_lists/blob/main/screenshots/example.png?raw=true) 

## Technical stack
Django, Bootstrap

## Usage

### Installation

```bash
git clone https://github.com/ProtKsen/wish_lists.git
```

### One-time action (if not poetry)

```bash
pip install poetry
poetry config virtualenvs.in-project true
```

### Install dependecies

```bash
poetry init
poetry install
```

### Configure environment

Use `.env.default` to create `.env`

### Start app
```bash
make runserver
```
