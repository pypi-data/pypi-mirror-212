import boto3
import botocore
import os
import sys
import yaml
import csv
import json
from typing import List

class Functions:
    """ Helper functions for interacting with AWS"""


    def parse_yaml(file):
        """Exposes configuration YAML file

        Args:
            file (.yml): Config

        Returns:
            dict: access like yml_filename['aws']['our_bucket'] 
        """
        try: 
            with open(file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f'{e}\nDid you create the config file described in the README?')
            sys.exit(1)


    def connect_to_s3():
        """Connect to S3 resource using boto3

        Returns:
            boto3 resource: boto3 S3 resource
        """
        try:
            return boto3.resource("s3")
        except Exception as e:
            print(f"Can't connect to S3. Error: {e}")
            sys.exit(1)

    def assure_s3_bucket(s3, bckt):
        """Check if bucket exists and create if not

        Args:
            s3 (boto3 resource): boto3 S3 resource
            bckt (S3 bucket): S3 bucket
        """
        try:
            s3.meta.client.head_bucket(Bucket = bckt)
            print('Specified bucket exists')
        except botocore.exceptions.ClientError as e:
            print(f'Error code: {e}')
            if e.response["Error"]["Code"] == "404":
                print ('Bucket failed head_bucket() call, likely does not exist')
                s3.create_bucket(Bucket = bckt)
                print(f'Created {bckt}')

    def diff_bucket_objs(s3, bucket_1, prefix_1, bucket_2, prefix_2, match_extensions=False):
        """Identifies the objects in bucket_1 that are not in bucket_2 by key including prefix and extension

        Args:
            s3 (boto3 resource): boto3 S3 resource
            bucket_1 (S3 bucket): 1st S3 bucket
            prefix_1 (String): prefix for objects in bucket 1
            bucket_2 (S3 bucket): 2nd S3 bucket
            prefix_2 (String): prefix for objects in bucket 2
            match_extensions (bool): Flag to consider matching file extensions (default: False)

        Returns:
            set: diff in bucket contents
        """
        def process_objects(bucket, prefix):    
        # returns the set of keys after applying the prefix and optionally removing file extensions.
            keys = set()
            for obj in bucket.objects.filter(Prefix=prefix):
                key = obj.key[len(prefix):] if prefix else obj.key
                if not match_extensions:
                    key = os.path.splitext(key)[0]
                keys.add(key)
            return keys

        bucket_1_keys = process_objects(s3.Bucket(bucket_1), prefix_1)
        bucket_2_keys = process_objects(s3.Bucket(bucket_2), prefix_2)

        diff = bucket_1_keys.difference(bucket_2_keys)
        print(f'There were {len(diff)} objects missing')
        return diff


    def copy_over_all_objects(s3, source, source_prefix, dest, dest_prefix):
        """Copy all prefixed objects from AWS S3 bucket to another

        Args:
            s3 (boto3 resource): boto3 S3 resource
            source (S3 bucket): source S3 bucket
            source_prefix (String): prefix for objects in source
            dest (S3 bucket): destination S3 bucket
            dest_prefix (String): prefix for objects in destination
        """
        missing_keys = Functions.diff_bucket_objs(s3, source, source_prefix, dest, dest_prefix)
        ct = 0
        for key in missing_keys:
            key_dict = {'Bucket' : source, 'Key': f'{source_prefix}{key}'}
            s3.Bucket(dest).copy(key_dict, f'{dest_prefix}{key}')
            print (f'Copied over: {key}')
            ct += 1
        print (f'Copying complete, {dest_prefix} folder on destination bucket updated. {ct} objects copied over.')


    def search_s3_bucket_contents(s3_client, bucket_name, search_term):
        """Searches for a given search term in the contents of an S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket to search.
            search_term (str): The term to search for in the bucket contents.

        """
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        for obj in response.get('Contents', []):
            object_key = obj['Key']
            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read().decode('utf-8')  # Assuming text content, adjust decoding based on content type

            if search_term in content:
                print(f"Found '{search_term}' in object: {object_key}")
                break


    def convert_json_to_csv(json_files: List[str], csv_files: List[str] = None):
        # Takes list of JSON objects and list of CSVs (optional) to convert JSONs line by line and aggregate in existing
        # passed CSVs or new ones if not
        # Opens each file sequentially (TODO vectorize) and reads in each line, identify structure, matches to structure of any
        # CSVs passed or already made, makes if not and binds new row
        """
        Converts JSON objects to CSV format and aggregates them into existing or new CSV files.

        Args:
            json_files (List[str]): List of paths to JSON files.
            csv_files (List[str]): List of paths to existing CSV files. If not provided, new CSV files will be created.

        """
        # proposed implementation follows:
        # get list of json.keys
        # get list of csv cols if csvs were passed
        #loop through json_files
            # if keys of current line match a csv struct, append
            # else create new csv , add to working list of csvs and append
        #return list of csvs with contents of all json files appended



        # if csv_files is None:
        #     csv_files = []

        # for json_file in json_files:
        #     csv_file = csv_files.pop(0) if csv_files else f"output_{len(csv_files) + 1}.csv"

        #     with open(json_file, "r") as file:
        #         json_data = json.load(file)

        #         # Check if the CSV file exists
        #         csv_exists = csv_file in csv_files
        #         if not csv_exists:
        #             # Create the CSV file with headers based on the JSON structure
        #             with open(csv_file, "w", newline="") as csvfile:
        #                 fieldnames = list(json_data[0].keys())
        #                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #                 writer.writeheader()

        #         # Append JSON data to the CSV file
        #         with open(csv_file, "a", newline="") as csvfile:
        #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #             writer.writerows(json_data)
    
    def convert_json_to_csv(json_files: List[str], csv_files: List[str] = None):
        # Takes list of JSON objects and list of CSVs (optional) to convert JSONs line by line and aggregate in existing
        # passed CSVs or new ones if not
        # Opens each file sequentially (TODO vectorize) and reads in each line, identify structure, matches to structure of any
        # CSVs passed or already made, makes if not and binds new row
        """
        Converts JSON objects to CSV format and aggregates them into existing or new CSV files.

        Args:
            json_files (List[str]): List of paths to JSON files.
            csv_files (List[str]): List of paths to existing CSV files. If not provided, new CSV files will be created.

        """
        # proposed implementation follows:
        # get list of json.keys
        # get list of csv cols if csvs were passed
        #loop through json_files
            # if keys of current line match a csv struct, append
            # else create new csv , add to working list of csvs and append
        #return list of csvs with contents of all json files appended



        # if csv_files is None:
        #     csv_files = []

        # for json_file in json_files:
        #     csv_file = csv_files.pop(0) if csv_files else f"output_{len(csv_files) + 1}.csv"

        #     with open(json_file, "r") as file:
        #         json_data = json.load(file)

        #         # Check if the CSV file exists
        #         csv_exists = csv_file in csv_files
        #         if not csv_exists:
        #             # Create the CSV file with headers based on the JSON structure
        #             with open(csv_file, "w", newline="") as csvfile:
        #                 fieldnames = list(json_data[0].keys())
        #                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #                 writer.writeheader()

        #         # Append JSON data to the CSV file
        #         with open(csv_file, "a", newline="") as csvfile:
        #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #             writer.writerows(json_data)

import csv
import json
from typing import List


def flatten_json(json_data):
    """
    Flattens a nested JSON object into a flat dictionary.

    Args:
        json_data: JSON object.

    Returns:
        dict: Flattened dictionary representation of the JSON object.
    """
    flattened = {}

    def flatten(data, prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                flatten(value, prefix + key + "_")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                flatten(item, prefix + str(i) + "_")
        else:
            flattened[prefix[:-1]] = data

    flatten(json_data)
    return flattened


def convert_json_to_csv(json_files: List[str], csv_files: List[str] = None):
    """
    Converts JSON objects to CSV format and aggregates them into existing or new CSV files.

    Args:
        json_files (List[str]): List of paths to JSON files.
        csv_files (List[str]): List of paths to existing CSV files. If not provided, new CSV files will be created.

    Returns:
        List[str]: List of paths to the resulting CSV files.
    """
    if csv_files is None:
        csv_files = []

    csv_file_data = []  # List to store CSV file data (list of rows)

    for json_file in json_files:
        with open(json_file, "r") as file:
            json_data = json.load(file)
            flattened_data = flatten_json(json_data)

            csv_file_matched = False  # Flag to track if JSON data matches an existing CSV file structure

            for i, csv_file in enumerate(csv_files):
                with open(csv_file, "r") as csvfile:
                    reader = csv.reader(csvfile)
                    csv_file_struct = next(reader)

                    if list(flattened_data.keys()) == csv_file_struct:
                        csv_file_matched = True
                        csv_file_data[i].append(flattened_data)  # Append flattened JSON data to existing CSV file data
                        break

            if not csv_file_matched:
                csv_file = f"output_{len(csv_files) + 1}.csv"
                csv_files.append(csv_file)
                csv_file_data.append([flattened_data])  # Create a new list with flattened JSON data

    for i, csv_file in enumerate(csv_files):
        with open(csv_file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(csv_file_data[i][0].keys()))
            writer.writeheader()
            writer.writerows(csv_file_data[i])

    return csv_files

Functions.convert_json_to_csv(['C:\\Users\\D\\Documents\\dev\\vehicle_event_etl\\2019-06-01-15-17-4-events.json'])

Functions.convert_json_to_csv(['C:\\Users\\D\\Documents\\dev\\vehicle_event_etl\\2019-06-01-15-17-4-events.json'])