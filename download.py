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

episodes = {#"Épisode 1.mp4": "https://cvs16-1.sibnet.ru/44/72/25/4472257.mp4?st=wfIbM1g01mmmTp2pcOYPIA&e=1676143000&stor=48&noip=1",
            #"Épisode 2.mp4": "https://cvs113-1.sibnet.ru/44/82/66/4482664.mp4?st=5qBC79NqwI-zx9pu3H_wPA&e=1676143000&stor=9&noip=1",
            #"Épisode 3.mp4": "https://cvs113-2.sibnet.ru/44/82/66/4482666.mp4?st=IIJA15k_wYmpFJ-3Wij6IA&e=1676143000&stor=10&noip=1",
            #"Épisode 4.mp4": "https://cvs14-1.sibnet.ru/44/91/75/4491757.mp4?st=Ahf0vFmxMX__8s-Bcah-cg&e=1676143000&stor=48&noip=1",
            #"Épisode 5.mp4": "https://cvs11-1.sibnet.ru/45/05/74/4505749.mp4?st=tky4OXfnUylH8n_mEX6V-g&e=1676143000&stor=25&noip=1",
            #"Épisode 6.mp4": "https://cvs11-2.sibnet.ru/45/15/54/4515543.mp4?st=zz6Yp_qNAOoxSTjIgTsZIA&e=1676143000&stor=49&noip=1",
            #"Épisode 7.mp4": "https://cvs18-1.sibnet.ru/45/24/27/4524278.mp4?st=6gZo08Qsd0X9S90DoQr0xQ&e=1676143000&stor=8&noip=1",
            #"Épisode 8.mp4": "https://cvs118-2.sibnet.ru/45/33/59/4533595.mp4?st=iZTBZhz3f7p_5StQdyp9dA&e=1676143000&stor=9&noip=1",
            #"Épisode 9.mp4": "https://cvs110-1.sibnet.ru/45/42/09/4542095.mp4?st=yN6p0fh4jzSy7RhHVjUelg&e=1676143000&stor=6&noip=1",
            #"Épisode 10.mp4": "https://cvn21-4.sibnet.ru/45/50/28/4550283.mp4?st=1N3bQbzxEcdvNRIKr9X6Dg&e=1676143000&stor=26&noip=1",
            "Épisode 11.mp4": "https://cvn22-2.sibnet.ru/45/57/97/4557971.mp4?st=a_BvNoy4-9VPIc_XGsteVg&e=1676143000&stor=26&noip=1",
            #"Épisode 12.mp4": "https://cvn22-4.sibnet.ru/46/65/86/4665860.mp4?st=Y0jeQ0I_X1ArFu0Ugv_jsA&e=1676143000&stor=49&noip=1",
            #"Épisode 13.mp4": "https://cvn12-1.sibnet.ru/46/74/01/4674011.mp4?st=J0h8XnbeTR6Qj2gF6BJHqg&e=1676143000&stor=50&noip=1",
            #"Épisode 14.mp4": "https://cvn31-4.sibnet.ru/46/81/46/4681467.mp4?st=b6d3--fFubCBY72714AKWA&e=1676143000&stor=10&noip=1",
            #"Épisode 15.mp4": "https://cvn21-4.sibnet.ru/46/97/72/4697726.mp4?st=II58kjjNU9HY29lRMf91ew&e=1676143000&stor=10&noip=1",
            #"Épisode 16.mp4": "https://cvs13-2.sibnet.ru/46/97/72/4697728.mp4?st=EM-3d-TMSe6jVUv1UvW-ig&e=1676143000&stor=6&noip=1",
            #"Épisode 17.mp4": "https://cvn31-1.sibnet.ru/47/05/23/4705231.mp4?st=y4LjPZZo67n2vxRgB6riFA&e=1676143000&stor=25&noip=1",
            "Épisode 18.mp4": "",
            "Épisode 19.mp4": "",
            "Épisode 20.mp4": "",
            "Épisode 21.mp4": "",
            "Épisode 22.mp4": ""}

download(episodes, calculate_total_size=False)