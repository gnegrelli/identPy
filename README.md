# identPy

_IdentPy_ is a framework for estimation of parameters of mathematical models used for describing dynamic nonlinear systems.

### Estimation methods

The following estimation methods are implemented on identPy and can be used to estimate the model parameters.

* Mean-Variance Mapping Optimization (MVMO)
* Trajectory Sensitivity

### Implemented systems

The following systems have mathematical models implemented  and can be estimated using on identPy.

* Spring-Mass
* Simple Pendulum
* Linearized Z-IM Load Model
* DFIG Model (2 mathematical models)

## Requirements

IdentPy requires Python 3.6 or higher as weel as blinker, numpy, scipy and matplotlib packages.

## Installation

Installation of identPy can be done by following the instructions below.

### Using pip

Users can install identPy by downloading the project from its GitHub page and running the following command on terminal.

```bash
$ pip install <path/to/identPy>
```

### Contributing

In order to contribute to this package, the user must install the package in develop mode. When contributing to identPy, it is generally recommended to install packages in a virtual environment to avoid modifying system state:

```bash
$ python -m venv venv
$ source venv/bin/activate
(venv)$ pip install -e <path/to/identPy>
```

## Running estimations

Inside the `scripts` folder, users can look at examples on how to perform parameter estimation using identPy.

On `run_estimation.py`, MVMO and TSM are used to estimate the parameters of an improved DFIG model with measurements imported from a file. The output behaviour are plotted throughout the estimation process and, at the its end, the error evolution is also presented.

The `population_size_analysis.py` script was developed to evaluate the effects of population size on the estimation performance. For every size given in a list, 35 estimations are performed and their results, as well as the time duration, are saved into a file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
