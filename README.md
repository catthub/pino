# Requirement
+ [`Arduino IDE`](https://www.arduino.cc/en/main/software)

# Quick start
## Poetry
Confirm `Arduino IDE` is installed on your system. If not, install it from the [official page](https://www.arduino.cc/en/main/software).

If `poetry` is installed on your system, run
```
poetry install --no-dev
```
and then you can run any examples in `examples`.

Or not, follow the [official instructions](https://python-poetry.org/docs/) to install poetry.

## Non-poetry
You can use `pino` on an environment without `poetry`.
Install `pyserial` with `pip`,
```
pip install pyserial
```
and then you can run any examples in `examples`.
