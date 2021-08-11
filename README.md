# Kyocera Address Book Creation Tool

A Python3 tool that I wrote to automate the creation of address books specifically for Kyocera Printers and Scanners. The tool
does not utilize any special technologies created by Kyocera, this was a small project I put together to make the 
administration for Kyocera address books less of a pain as whenever users would come and leave the organization, users needed to be added and removed, so
decided to make the process easier for myself.

## Prerequistes

You will need a system with python3.6 or higher. No external libraries were used to develop the tool to be entirely self contained.
to create tool although I highly recommend installing [sqlite3](https://www.sqlite.org/index.html) to your machine to see
how database is working or if you would add improvements.

## Usage

```
$> python3 main.py
```

## Known Issue

Kyocera has a weird way of encoding passwords into their scanners and pasting clear text passwords into the [constant.py](https://github.com/Kitar0s/Kyocera-Address-Book-Creation-Tool/blob/main/utils/constants.py) file will not work **(and is not encouraged).** I was able to get mine to work by exporting a copy an address book using [Kyocera Net Viewer](https://www.kyoceradocumentsolutions.us/en/products/software/KYOCERANETVIEWER.html) and taking the encoded string and using that for the password string. **USE THIS AT YOUR OWN RISK** This is not advice or a recommendation, only what I have found that works for me. I do not know if this encoded string is easily reversible and therefore do not take responsiblity if you copy these actions which may lead to malicious activities against your system.