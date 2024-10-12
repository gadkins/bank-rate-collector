# extract.py
from .utils import get_openai_api_key
from typing import List, Dict, Optional
from .models import BankResponse
import os   
import time
from openai import OpenAI
from collections import defaultdict

def chunk_data(data: str, chunk_size: int) -> List[str]:
    """
    Splits a large string into smaller chunks of a specified maximum size.

    Args:
        data (str): The data to be chunked.
        chunk_size (int): The maximum size of each chunk.

    Returns:
        List[str]: A list of data chunks.
    """
    chunks = []
    for i in range(0, len(data), chunk_size):
        chunks.append(data[i:i + chunk_size])
    return chunks

def extract_with_llm(chunk: str) -> BankResponse:
    prompt = f"""
Extract the banking rate data from the following text and structure it according to the provided model.

Special instructions:
- If a property or object does not exist, do not include it in the output.
- Do not include 'www' or other subdomains in the bankRootDomain.
- If dividend rate is given, do not include interest rate.
- Do not convert percentage to decimal. I.e. if the rate is 0.55%, return 0.55 not 0.0055

Text:
{chunk}
"""
    client = OpenAI(api_key=get_openai_api_key())

    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output structured data."},
            {"role": "user", "content": prompt}
        ],
        response_format=BankResponse,  # Directly use the Pydantic model here
    )

    return response.choices[0].message.parsed  # This will be a Pydantic model instance

def process_and_extract_tables_single(
    csv_tables: List[str],
    chunk_size: int
) -> Optional[BankResponse]:
    """
    Processes the CSV tables for a single URL and extracts structured data using OpenAI's API,
    returning a merged BankResponse object.

    Args:
        csv_tables (List[str]): List of CSV tables as strings.
        chunk_size (int): The size of the data chunks to be processed.

    Returns:
        Optional[BankResponse]: A merged BankResponse object or None if unsuccessful.
    """
    if not csv_tables:
        print("No CSV tables to process.")
        return None

    # Assuming all CSV tables belong to the same domain
    combined_csv = ''.join(csv_tables)
    chunks = chunk_data(combined_csv, chunk_size)

    url_responses: List[BankResponse] = []

    start_time = time.time()

    for chunk in chunks:
        try:
            extracted_data_chunk = extract_with_llm(chunk)
            url_responses.append(extracted_data_chunk)
        except Exception as e:
            print(f"Failed to extract data from chunk: {e}")
            return None

    end_time = time.time()
    processing_time = end_time - start_time

    print(f"Processing time: {processing_time:.2f} seconds")

    # Merge all responses into a single BankResponse
    merged_response = merge_bank_responses(url_responses)

    return merged_response

def merge_bank_responses(responses: List[BankResponse]) -> BankResponse:
    """
    Merges a list of BankResponse objects into a single BankResponse object.

    Args:
        responses (List[BankResponse]): A list of BankResponse objects to merge.

    Returns:
        BankResponse: A merged BankResponse object.
    """
    if not responses:
        return None

    # Initialize with the first response
    merged_response = BankResponse(
        bankRootDomain=responses[0].bankRootDomain,
        checkingAccounts=[],
        savingsAccounts=[],
        moneyMarketAccounts=[],
        certificatesOfDeposit=[],
        individualRetirementAccounts=[],
        loans=[],
        creditCards=[],
        fees=[]
    )

    for response in responses:
        if response.checkingAccounts:
            merged_response.checkingAccounts.extend(response.checkingAccounts)
        if response.savingsAccounts:
            merged_response.savingsAccounts.extend(response.savingsAccounts)
        if response.moneyMarketAccounts:
            merged_response.moneyMarketAccounts.extend(response.moneyMarketAccounts)
        if response.certificatesOfDeposit:
            merged_response.certificatesOfDeposit.extend(response.certificatesOfDeposit)
        if response.individualRetirementAccounts:
            merged_response.individualRetirementAccounts.extend(response.individualRetirementAccounts)
        if response.loans:
            merged_response.loans.extend(response.loans)
        if response.creditCards:
            merged_response.creditCards.extend(response.creditCards)
        if response.fees:
            merged_response.fees.extend(response.fees)

    return merged_response

# Define module exports
__all__ = ['process_and_extract_tables_single']
