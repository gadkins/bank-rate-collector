import boto3
from botocore.exceptions import ClientError
import os
import json
from dotenv import load_dotenv
from typing import List
from .models import BankResponse

# Fetch OpenAI API key from local environment or AWS Secrets Manager
def get_openai_api_key():
    if os.getenv("ENVIRONMENT") == "local":
        # Use key from .env for local development
        return os.getenv("OPENAI_API_KEY")
    else:
        # The name and region of the secret in AWS Secrets Manager
        secret_name = "bank-rate-collector/openai-api-key" 
        region_name = "us-east-2" 

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)
        return secret_dict["OPENAI_API_KEY"]

# Print the CSV content for each URL
def print_csv_tables(csv_tables_dict):
    for url, csv_tables in csv_tables_dict.items():
        print(f"CSV Tables from {url}:")
        for i, csv_table in enumerate(csv_tables):
            print(f"Table {i+1}:")
            print(csv_table)
            print()  # Print a newline for better readability
