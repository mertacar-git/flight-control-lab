# Flight Control Lab

Interactively tune a PID controller for a simplified vertical-motion model, apply a disturbance and export the simulation.

## Quick start

Python 3.12 recommended. Run commands inside this repository.

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Validation

```sh
python -m unittest discover -v
```

## Model and limitations

Model: dh/dt = v; dv/dt = u - 0.3v + disturbance. The acceleration command is bounded to ±10 m/s² and interpreted relative to gravity-compensated hover. Derivative feedback uses measured velocity; conditional integration limits windup. Integration is semi-implicit Euler at 0.02 seconds. Settling time uses a 2% target band over the finite simulation window. This is an educational one-dimensional model, not aircraft flight software.

## Repository structure

- `core.py`: numerical/data processing functions
- `app.py`: interactive Streamlit interface
- `test_core.py`: checks for model behavior and invalid input

## Development

Built with AI assistance. Model assumptions and validation are documented so the implementation can be reviewed and extended.
