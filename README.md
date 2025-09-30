# Mock Data Generation Framework

This repository houses code for the `mock_data` package, a framework for generating mock datasets. Dataset specifics are defined via yaml and dynamically generated using the `read_yaml_spec` method of the `MockDataset` class. More on this below. 

## Requirements

1. [`uv`](https://docs.astral.sh/uv/) Python package and project manager.

    ```sh
    # version 0.8.8 at time of documentation
    brew install uv
    ```


## Setup

1. Install Python interpreter and Python packages.

   ```sh
   # Install uv-managed Python based on project's `.python-version`
   uv python install --managed-python

   # Create Python virtualenv version based on project's `.python-version`
   uv venv

   # Activate the project's Python virtualenv
   source ./.venv/bin/activate

   # Install project's python packages
   uv sync --all-groups
   ```


## Architecture

Todo: this section needs a picture

This package is best thought of as a _framework_ rather than a ready-to-use package. To generate an artificial dataset, each field (column) must be associated with a _backend_. A _backend_ is an abstraction coupling a data type with a statistical distribution. The following 4 _core backends_ are included within the framework. 
- `BoundedNumerical` - Sample ints or floats from a statistical distribution scaled and shifted to a particular range. 
- `BoundedNumericalDatetime` - Sample dates / timestamps from a distribution between a supplied start and end date / timestamp. 
- `WeightedDiscrete` - Sample arbitrary objects with relative frequency specified by the value within a key / value pair.
- `LoremIpsumText` - Similar to BoundedNumerical. Generates lengths of Lorem Ipsum text where length is governed by a statistical distribution with specified bounds. 

### Plugin Architecture to the Rescue

What about instances where your data type doesn't fit nicely into one of the above four categories. An example of this is the Multiple Response data type within SBL. These values are semicolon delimited strings of numbers (e.g. "1;3;10"). You _could_ enumerate every possible combination and leverage `WeightedDiscrete` directly, but that scales horribly. 

The solution is creating a custom data backend, or plugin. You can create a new class that inherits from `AbstractBackendInterface` or any of the above backends. This new class can then be registered via `MockDataset.register_backend` and used during creation of your mock dataset. This plugin architecture makes it possible to extend the core functionality of `mock_data` to generate datasets with any conceivable data type. The idea is that the framework can provide most of what you need out of the box, and anything missing can be easily created using the supplied programming paradigms and api. 

## Example Usage

There is a folder called `examples` within this repo with some example files. There is a Jupyter Notebook illustrating use of the various core data backends, and a Python script called `example.py` demonstrating creation of the `example_mock_data.csv` file within the same folder. This section borrows from `example.py` and `example_spec.yaml`. 

Let's suppose we want to generate a dataset containing four columns: age, employer, income, and a flag indicating whether they are hispanic or latino (hispanic_or_latino). We can accomplish this with a single yaml file and just a few lines of code. 

`example_spec.yaml`:

```yaml
age:
  BoundedNumerical:
    distribution: norm
    lower_bound: 18
    upper_bound: 99
    coerce_to_int: true
employer:
  LoremIpsumText:
    lower_bound: 10
    upper_bound: 30
income:
  BoundedNumerical:
    distribution: chi2
    lower_bound: 10000
    upper_bound: 200000
    df: 10
hispanic_or_latino:
  WeightedDiscrete:
    frequency_dist:
      Yes: 5
      No: 1
```

The top level keys correspond to column names. This dataset will have columns age, employer, income, and hispanic_or_latino. The second level keys correspond to the name of the backend used to generate said field's data. 

The _age_ field is leveraging `BoundedNumerical` and we're passing arguments various keyword arguments to said backend's constructor to control the behavior of the generated data. Here we're restricting the range of values to between 18 and 99, coercing any floats to whole numbers (ints), and setting the sampling distribution to scipy.stats.norm (a bell curve). 

_income_ is very similar to _age_ above. We've switched distributions to a chi square distribution with 10 degrees of freedom and changed the range of values. 

_employer_ is generated using random strings of Lorem Ipsum between the supplied upper and lower length bounds. Distribution is not supplied which means we're leveraging the default distribution (uniform). 

The last field, *hispanic_or_latino*, illustrates how `WeightedDiscrete` can be leveraged to sample arbitrary values from a set with specificied relative frequency. Here we're telling the backend to sample from the set {Yes, No} with Yes appearing 5 times more frequently than No. 

Generating a mock dataset with 100 rows can be accomplished using just four lines of code. 
```python
from mock_data import MockDataset

# instance of the mock dataset class
mock = MockDataset.read_yaml_spec("example_spec.yaml")

# a Pandas dataframe containing 100 rows
df = mock.generate_mock_data(nrows=100)

# write to csv
df.to_csv("example_mock_data.csv", index=False, float_format="%.2f")
```

The beauty of this is that your data generation script is completely separate from the yaml configuration file for the dataset. Want to add 100 more columns? Wash, rinse, and repeat. 

## Custom Data Backends

todo: illustrate how a custom sublcass could be used to produce instances of Multiple Response for SBL. 