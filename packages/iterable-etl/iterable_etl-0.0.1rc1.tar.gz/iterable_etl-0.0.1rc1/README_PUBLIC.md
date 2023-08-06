# `iterable_etl`

> Replicate data from iterable in databricks

## Usage

```bash
python -m iterable_etl --table <table-name>
```

where <table-name> is one of the following: `campaign_history`, `campaign_metrics`, `campaign_list_history`, `list`, or `ALL`.

Further configs are set via environment variables:

- `ITERABLE_KEY`: API access
- `APP_ENV`: <development/production> - debug mode
- `SAMPLE_OUTPUT`: <True/False> - Save dataframes to csv

## DEV

### Create venv

```bash
python -m venv env
```

### Activate venv

- unix

```bash
source env/bin/activate
```

- windows

```bash
env\Scripts\activate.bat
```

### Install Packages

```bash
pip install -r requirements.txt
```

## Test

```bash
make test
```

## Format

```bash
make format
```

```bash
make lint
```
