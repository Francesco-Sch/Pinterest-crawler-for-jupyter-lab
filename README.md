# Pinterest crawler for jupyter notebooks
Crawl images from pinterest from within a jupyter notebook in jupyter lab.

Based on the crawler from [mirusu400](https://github.com/mirusu400)  
[Original GitHub Repository](https://github.com/mirusu400/Pinterest-infinite-crawler/)

# Requirements
* Python 3.7+
* Selenium, requests, beautifulsoup4, pyyaml
* Chrome + Chromedriver

# Installation
1. Download requirements
```
git clone https://github.com/Francesco-Sch/Pinterest-crawler-for-jupyter-lab ./crawler
cd crawler
pip install -r requirements.txt
```

2. Download chromedriver

You **MUST** download [ChromeDriver](https://chromedriver.chromium.org/downloads) as the same version of [Chrome](chrome://settings/help).

And replace it the same directory with `main.py`.

3. (Optional) Set `config.yaml`

Copy `.config.yaml` to `config.yaml` and fill your Pinterest's email, password and directorys to save images
```
email: [your email here]
password: [your password here]
directory: ./download
```

# Usage
```
python main.py
```

# Using argument
You can also run crawler by passing argument, here are full document:
```
usage: main.py [-h] [-e EMAIL] [-p PASSWORD] [-d DIRECTORY] [-l LINK] [-g PAGE] [-s SCALING]

optional arguments:
  -h, --help                            show this help message and exit
  -e EMAIL, --email EMAIL               Your Pinterest account email
  -p PASSWORD, --password PASSWORD      Your Pinterest account password
  -d DIRECTORY, --directory DIRECTORY   Directory you want to download
  -l LINK, --link LINK                  Link of Pinterest which you want to scrape
  -g PAGE, --page PAGE                  Number of pages which you want to scrape
  -b BATCH, --batch BATCH               Enable batch mode (Please read README.md!!)
  -s SCALING, --scaling SCALING         Pixel value to which the longer side of the image should be scaled down
```

**Example:**
> main.py -e [your_e-mail] -p [your_password] -d download_image -l https://pinterest.com/ -g 10 -s 1000

# Batch mode
You can download multiple Pinterest links in a one, using batch mode

1. Copy and paste `.batch.json` to `batch.json` and modify json array files.
```
[
    {
        "index": "1",
        "link": "https://www.pinterest.co.kr/pin/362750944993136496/",
        "dir": "./download1"
    },
    {
        "index": "2",
        "link": "https://www.pinterest.co.kr/",
        "dir": "./download2"
    },
    ...
]
```

2. Use Batch mode in command line
> main.py -b

# Q & A
### What is `Link to scrape` mean?
You can select **any** pages what you want to scrape in Pinterest, not only main page. Such as:
* [Releative-pins of one pin](https://www.pinterest.co.kr/pin/643240759283703965/)
* [Someone's board](https://www.pinterest.co.kr/eaobrienae/croquies/)
* [A search result](https://www.pinterest.co.kr/search/pins/?q=Github)
* Or anything!

### Does it can download video?
No, you can only download jpg images from this tool. Video is not support for now.

# Contribute
If you find an issue or wants to contribute, please issue or pull request.