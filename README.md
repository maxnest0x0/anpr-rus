# ANPR RUS
Automatic Russian number plate recognition system

## Installation for Debian Linux
### Clone the repository
```sh
$ git clone https://github.com/maxnest0x0/anpr-rus.git
$ cd anpr-rus
```

### Make sure Git LFS is installed or install it
It is recommended to use the latest version. Versions below 3.6.1 [contain a vulnerability](https://github.com/git-lfs/git-lfs/security/advisories/GHSA-q6r2-x2cc-vrp7).
```sh
$ curl --silent https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
$ sudo apt-get install --assume-yes git-lfs
$ git lfs install
```

### Download LFS files
```sh
$ git lfs pull
```

### Set up Python environment and install dependencies
```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --requirement requirements.txt
```

### Set the `BOT_TOKEN` environment variable
This is a token for your Telegram bot. You may want to use `.env` for more security.
```sh
$ export BOT_TOKEN='token'
```

### Run the program
We use the Flask development server as it is a prototype program.
```sh
$ python main.py
```

## Dataset
We have collected a dataset of 10007 images.
They are located [here](https://drive.google.com/drive/folders/1hSRh3G7xV808UyMl6CouE4Bj75XGBi3f?usp=sharing).
The [Dataset/license_plates.json](https://github.com/maxnest0x0/anpr-rus/blob/master/Dataset/license_plates.json) file contains the object detection markup and the car number text for each image.
The `box` property contains `x`, `y`, `width`, `height` values ​​relative to the image dimensions.

## Usage
### Web page
For PC users we host the web page at http://176.222.54.175:5000/.

### Telegram bot
For mobile users we run the Telegram bot [@AnprRusBot](https://t.me/AnprRusBot).

### API
For developers we provide an API endpoint, `POST http://176.222.54.175:5000/api/predict`, that accepts an `image` parameter.

## Screencasts
### Web page

https://github.com/user-attachments/assets/90fdc453-fd1b-424b-b0b4-4eb3e50105e7

### Telegram bot

https://github.com/user-attachments/assets/68edc6be-d087-4539-b554-31e0d333bd05
