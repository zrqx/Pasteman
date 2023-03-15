# Pasteman
**A Python based CLI Utility built around Pastebin's API**

![Pasteman Banner](res/banner.png)

## Requirements
- Python3 and pip
- A Pastebin Account

[Register](https://pastebin.com/signup) for a Pastebin Account. Copy your Unique Developer API Key from [API Docs](https://pastebin.com/doc_api). Try out the features so as to have a better understanding of this Program.

## Installation and Config
```bash
# Pull the Repository
git clone https://github.com/zrqx/Pasteman.git

# Install the Dependencies
cd Pasteman
pip3 install -r requirements.txt

# Configure Pasteman
python3 pasteman.py configure --username "Pastebin Username" --password "Pastebin Password" --devkey "API Dev Key"
  # Creates `credentials.json` with the data.
```

## Usage
Pastebin's API currently supports these opearations
 - Create New Paste
 - List all Private Pastes
 - Retrieve Raw content of a Paste
 - Delete a Paste

```bash
$ python3 pasteman.py COMMAND {Optional Arguments}
```

### Create New Paste
```python
python3 pasteman.py create --message "Your Message"

     Optional Arguments:
     --title "Title for the Paste"  # Default "Untitled"
     --type "public/private"        # Default "private"
     --expires "option"             # Options - {N,10M,1H,1D,1W,2W,1M,6M,1Y}, Default "10M"
```

### List All Private Pastes
```python
python3 pasteman.py list
```
Returns 2 lists, containing `paste_keys` and `paste_titles` respectively

### Retrieve Raw Contents of a Paste
```python
python3 pasteman.py retrieve --key "paste_key"
```

### Delete a Private Paste
```python
python3 pasteman.py delete --key "paste_key"
```
Returns "Paste Deleted" on Successful operation