import sys
import requests
import os
import warnings
warnings.filterwarnings("ignore")

def sizeof_fmt(num):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1000.0:
            return f"{num:3.1f} {unit}o"
        num /= 1000.0
    return f"{num:.1f} Po"

def get_size(response):

    file_length = response.headers.get('content-length')
    if file_length is None:
        return None
    return int(file_length)

def total_size(dict):

    total_length = 0
    for file_name, link in dict.items():
        if link == "":
            continue

        response = requests.get(link, stream=True, verify=False)
        file_length = get_size(response)

        if file_length is None:
            print(f"No content length header for {file_name}")
            continue

        total_length += file_length

    return total_length

def download(dict, calculate_total_size = True):

    if calculate_total_size:
        print("Calculating total size...")
        print(f"Total size is : {sizeof_fmt(total_size(dict))}.\n")

    for file_name, link in dict.items():
        if link == "":
            continue
        
        if os.path.exists(file_name):
            user_input = input(f"'{file_name}' already exist, override it ? (Y/N) : ").lower()
            while (user_input != "y") or (user_input != "n"):
                user_input = input("\n\rInvalid input. Please enter (Y/N) : ").lower()
            if user_input == "y":
                os.remove(file_name)
                print("\n")
            else:
                print("Skipping this file because user don't want to override.\n")
                continue

        with open(file_name, "wb") as f:

            response = requests.get(link, stream=True, verify=False)
            file_length = get_size(response)

            if file_length is None: # no content length header
                print(f"Downloading '{file_name}'.")
                f.write(response.content)
            else:
                dl = 0
                print(f"Downloading '{file_name}'. File size is {sizeof_fmt(file_length)}.")
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / file_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                    sys.stdout.flush()
        print("\nDownload finished.\n")
