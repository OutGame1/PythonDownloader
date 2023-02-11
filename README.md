# PythonDownloader

Simply create a dictionnary with the wanted name of the file as the key and the download link of the file as the value and call the download function on it.
The 'calculate_total_size' argument provides in the console the total size of all files in the dictionnary and is by default False.

EXEMPLE :
dict = {"file1.txt": "https://<area>w<area>ww.<area>website<area>.com/file1.txt"} <br />
download(dict)

---- << Console >> -----

Downloading 'file1.txt'. File size is 1.02 Ko.
[==================================================]

Download finished.
