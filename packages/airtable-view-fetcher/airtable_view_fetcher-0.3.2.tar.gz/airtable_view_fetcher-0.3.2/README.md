# Airtable View Fetcher

Airtable View Fetcher is a Python package that allows you to fetch data from Airtable shared views without the need of
an API token.

## Installation

You can install the package using pip:

```bash
pip install airtable-view-fetcher
```

## Usage

To use Airtable View Fetcher, you can execute it as a command-line tool with the shared view URL as the argument:

```bash
airtable-view-fetcher <shared_view_url>
```

Replace `<shared_view_url>` with the URL of the Airtable shared view you want to fetch data from.

To write the output to a JSON file, you can use the following option:

```bash
airtable-view-fetcher <shared_view_url> -o <output_file_name>
```

Replace `<output_file_name>` with the name of the output JSON file

## Requirements

Airtable View Fetcher requires the following dependencies:

- Python 3.8+
- requests
- pytz

## Contributing

Contributions to Airtable View Fetcher are welcome! If you encounter any issues or have suggestions for improvements,
please feel free to open an issue or submit a pull request on
the [GitHub repository](https://github.com/vartur/airtable_view_fetcher).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

