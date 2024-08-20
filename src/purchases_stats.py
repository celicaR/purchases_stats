import json
import logging
import sys
import traceback

import pandas as pd
from pandas import DataFrame
from rich import box
from rich.console import Console
from rich.table import Table

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

pd.set_option("display.max_columns", None)
pd.options.mode.copy_on_write = True  # When adding a calculated column, make sure deep copy is allowed


def load_data(file_path: str) -> json:
    """Function to load the JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        logging.error(f"File {file_path} does not exist. {str(e)}, {traceback.print_tb(e.__traceback__)}")
        sys.exit(1)
    except KeyError as e:
        logging.error(f"Input JSON file is empty or data is malformed. {str(e)}, {traceback.print_tb(e.__traceback__)}")
        sys.exit(1)


def convert_data_to_df(data) -> DataFrame:
    """Function to convert the JSON data to a Panda DataFrame."""
    try:
        if len(data) == 0:
            raise ValueError("There is no JSON data to convert to a DataFrame.")

        # Create the DataFrame from the json file with normalized items array to individual columns
        df = pd.json_normalize(data, "items", ["brand", "customer_id", "purchase_id"])

        # Rearrange the DataFrame columns
        df = df.filter(
            [
                "brand",
                "customer_id",
                "purchase_id",
                "department",
                "product_category",
                "product_name",
                "price",
                "quantity",
            ]
        )

        df.rename(
            columns={
                "department": "item_department",
                "product_category": "item_product_category",
                "product_name": "item_product_name",
                "price": "item_price",
                "quantity": "item_quantity",
            },
            inplace=True,
        )

        return df
    except ValueError:
        logging.error("Input JSON data is empty or data is malformed. {str(e)}, {traceback.print_tb(e.__traceback__)}")
        sys.exit(1)
    except KeyError as e:
        logging.error(f"Input JSON KeyError is empty or malformed. {str(e)}, {traceback.print_tb(e.__traceback__)}")
        sys.exit(1)


def transform_df(df: DataFrame) -> DataFrame:
    """Function to transform the data.
    Transformation performed are:
        - get rid of duplicates
        - work out the product purchased value for each purchase items'."""
    try:

        if df.empty:
            raise ValueError("There is no data in the DataFrame to perform the transform on.")

        # Remove duplicates rows
        df = df.drop_duplicates()

        # Work out the product_values for each item in a purchase
        df.loc[:, "item_product_value"] = df.apply(lambda row: pd.to_numeric(row["item_price"]) * row["item_quantity"], axis=1)
        return df

    except Exception as e:
        logging.error(f"Failed to process the purchases: {str(e)}, {traceback.print_tb(e.__traceback__)}")
        sys.exit(1)


def calculate_statistics(df: DataFrame) -> json:
    """Function to calculate the purchases statistics based on purchases' totals."""
    try:
        if df.empty:
            raise ValueError("There is no data in the DataFrame to perform the calculations on.")

        # DISPLAYING OF THE TABLE - COMMENTED OUT SINCE NOT REQUIRED FOR SOLUTION, BUT USEFUL WHEN TESTING
        # console = Console()
        # table = Table("Original Purchase Data", box=box.SQUARE)
        # table.add_row(df.to_string(float_format=lambda _: "${:.2f}".format(_)))
        # console.print(table)

        # Work out the total a purchase per brand, customer_id and purchase_id
        purchase_total = df.sort_values(["brand", "customer_id", "purchase_id"]).groupby(["brand", "customer_id", "purchase_id"])["item_product_value"].sum()

        # DISPLAYING OF THE TABLE - COMMENTED OUT SINCE NOT REQUIRED FOR SOLUTION, BUT USEFUL WHEN TESTING
        # table = Table("Purchase Totals per purchase_id", box=box.SQUARE)
        # table.add_row(purchase_total.to_string(float_format=lambda _: "${:.2f}".format(_)))
        # console.print(table)

        # Calculations

        # Assumptions: all required calculations are to be done on the purchase totals
        # As in calculate the average/max/median based on purchase total not individual product values in a purchase items listed.

        results = {
            "total_volume_of_spend": f"${purchase_total.sum():.2f}",
            "average_purchase_value": f"${purchase_total.mean():.2f}",
            "maximum_purchase_value": f"${purchase_total.max():.2f}",
            "median_purchase_value": f"${purchase_total.median():.2f}",
            "unique_products_purchased": len(pd.unique(df["item_product_name"])),
        }

        return json.dumps(results, indent=4)

    except Exception as e:
        logging.error(f"An error occurred while processing the data: {str(e)}, {traceback.print_tb(e.__traceback__)}")
        sys.exit(1)


def get_purchase_stats(file_path) -> json:
    """Function to return the calculated purchases statistics."""
    logging.debug(file_path)

    json_data = load_data(file_path)
    logging.debug(json_data)

    data_df = convert_data_to_df(json_data)
    logging.debug(data_df)

    transformed_data_df = transform_df(data_df)
    logging.debug(transformed_data_df)

    stats = calculate_statistics(transformed_data_df)
    logging.debug(stats)

    return stats


def main(file_path):
    stats = get_purchase_stats(file_path)
    print(stats)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Usage: python cli_app.py <purchases.json>")
        sys.exit(1)

    main(sys.argv[1])
