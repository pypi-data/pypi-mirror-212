import pandas as pd
import boto3
import json
from btg_investment_flow_portfolio_optimization.btg_api import BTGApiHandler


class PortfolioOptimizer:
    def __init__(self, inputs, aws_credentials: dict, btg_credentials: dict):
        # initialize the s3 interface
        self._init_s3_interface(aws_credentials)
        self.btg_api = BTGApiHandler(
            btg_credentials["base_url"],
            btg_credentials["clientId"],
            btg_credentials["clientSecret"],
        )
        # initialize the forecast and current portfolio data
        self.forecasts = {}
        self.current_portfolio = {}

        # parse the input data
        self.parse_forecast_data(inputs["forecast_inputs"])
        self.parse_current_portfolio(inputs["current_portfolio_inputs"])
        self.get_mean_daily_credit_card_expenses(
            inputs["credit_card_historical_inputs"]
        )

    def _init_s3_interface(self, aws_credentials: dict):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_credentials.get("aws_access_key_id"),
            aws_secret_access_key=aws_credentials.get("aws_secret_access_key"),
        )
        self.s3_resource = boto3.client(
            "s3",
            aws_access_key_id=aws_credentials.get("aws_access_key_id"),
            aws_secret_access_key=aws_credentials.get("aws_secret_access_key"),
        )

    def _process_dependent_variable(self):
        """
        Process and validate dependent variable.
        """
        dv = self.input_dict["dependent_variable"]
        if not isinstance(dv, dict):
            raise ValueError("Dependent variable should be a dictionary.")
        dv_df = pd.DataFrame(dv["data"])
        dv_df["timestamp"] = pd.to_datetime(dv_df["timestamp"])
        self.inputs["dependent_variable"] = dv_df.set_index("timestamp")

    def get_s3_file_key_from_file_path(self, bucket_name, folder_path):
        # define the s3 client
        s3 = self.s3_client
        # List objects in the specified S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
        # Initialize a list to hold the JSON files
        json_files = []
        # Check if the request returned any keys
        if "Contents" in response:
            for item in response["Contents"]:
                file_key = item["Key"]

                # Check if the file is a JSON
                if file_key.endswith(".json"):
                    json_files.append(file_key)
        # Check if there's only one JSON file in the list
        if len(json_files) == 1:
            return json_files[0]
        elif len(json_files) > 1:
            raise ValueError("More than one JSON file found in the folder.")
        else:
            raise ValueError("No JSON files found in the folder.")

    def get_mean_daily_credit_card_expenses(self, credit_card_historical_inputs):
        bucket_name = credit_card_historical_inputs["bucket_name"]
        folder_path = credit_card_historical_inputs["folder_path"]
        # Get the file key from the file folder path
        file_key = self.get_s3_file_key_from_file_path(
            bucket_name,
            folder_path,
        )

        # Get the file object from S3
        file_object = self.s3_resource.get_object(Bucket=bucket_name, Key=file_key)

        # Read the file content
        file_content = file_object["Body"].read().decode("utf-8")

        # Split the content by line to handle each JSON object
        lines = file_content.splitlines()

        # Use list comprehension to parse each line into a Python dictionary
        # If the json object does not contain "timestamp" and "value", raise a ValueError
        data = []
        for line in lines:
            json_obj = json.loads(line)
            try:
                timestamp = json_obj["timestamp"]
                value = json_obj["value"]
                data.append({"timestamp": timestamp, "value": value})
            except KeyError:
                raise ValueError(
                    f"Invalid format. Each line should contain 'timestamp' and 'value'. Problematic line: {line}"
                )

        dv_df = pd.DataFrame(data)
        dv_df["timestamp"] = pd.to_datetime(dv_df["timestamp"])
        dv_df = dv_df.set_index("timestamp")

        # Select the last 30 days
        last_30_days = dv_df.last("30D")
        # Calculate the mean of the selected column
        mean_value = round(last_30_days["value"].mean(), 2)
        self.mean_daily_credit_card_expenses = mean_value * 24
        return

    def parse_forecast_data(self, forecast_inputs):
        data = self.get_forecast_data(forecast_inputs)
        # Parse the input data
        for series_name, series_data in data.items():
            point_forecast_df = pd.DataFrame(
                [forecast["point_forecast"] for forecast in series_data["forecast"]],
                index=[forecast["timestamp"] for forecast in series_data["forecast"]],
                columns=[series_name],
            )
            variance_df = pd.DataFrame(
                [forecast["variance"] for forecast in series_data["forecast"]],
                index=[forecast["timestamp"] for forecast in series_data["forecast"]],
                columns=[series_name],
            )
            scenarios_df = pd.DataFrame(
                [forecast["scenarios"] for forecast in series_data["forecast"]],
                index=[forecast["timestamp"] for forecast in series_data["forecast"]],
            )
            # Since quantiles is a nested dictionary, we flatten it into a single dictionary
            # using dictionary comprehension
            quantiles_df = pd.DataFrame(
                [
                    {k: v for k, v in forecast["quantiles"].items()}
                    for forecast in series_data["forecast"]
                ],
                index=[forecast["timestamp"] for forecast in series_data["forecast"]],
            )
            self.forecasts[series_name] = {
                "point_forecast": point_forecast_df,
                "variance": variance_df,
                "scenarios": scenarios_df,
                "quantiles": quantiles_df,
            }

    def get_forecast_data(self, forecast_inputs):
        forecast_data = {}
        for series_name, series_input in forecast_inputs.items():
            # get the forecast data in s3
            response = self.s3_client.get_object(
                Bucket=series_input["bucket_name"], Key=series_input["file_key"]
            )
            # AWS get_object() returns a dictionary-like object;
            # the actual file content is stored under the key 'Body'
            file_content = response["Body"].read()

            # Assuming the file content is JSON formatted, we parse it
            forecast_data[series_name] = json.loads(file_content)

        return forecast_data

    def parse_current_portfolio(self, current_portfolio_inputs):
        # ToDo - parse the current portfolio data
        # integrate to BTG Api, get the current portfolio data
        # for Treasury, Operationals and Investments
        # For v0 this will not be used

        # get the current portfolio data from BTG API
        self.current_portfolio = {
            "treasury": self.btg_api.get_account_balance(
                current_portfolio_inputs["treasury"]["id"]
            ),
            "boleto": self.btg_api.get_account_balance(
                current_portfolio_inputs["boleto"]["id"]
            ),
            "escrow": self.btg_api.get_account_balance(
                current_portfolio_inputs["escrow"]["id"]
            ),
        }

        # get the current investment data from S3
        # TODO - get the current investment data from BTG API

    def calculate_escrow_adjustment(self):
        return round(
            self.mean_daily_credit_card_expenses * 5
            - self.current_portfolio["escrow"]["balance"],
            2,
        )
