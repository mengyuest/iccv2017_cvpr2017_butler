# cvpr2017_butler

Download, organize [cvpr2017](http://cvpr2017.thecvf.com/) papers from [CVF website](http://openaccess.thecvf.com/menu.py), also do listing and statistics (future version)


## Motivation
1. Hard to download all papers for [cvpr2017](http://cvpr2017.thecvf.com/)
2. Even you can download it, still hard to organize it manually

## Quick guide

### Prerequisites

1. Currently work well on Ubuntu 16.04
2. You computer can visit website to [Computer Vision Foundatiion open access](http://openaccess.thecvf.com)
3. Minimum 4GB disk storage on your workspace
4. (Optional but recommended) With docker on your computer

### Installation and Running
There are two ways for running this program, either use docker or run local. Choose one then you can view the result.

#### Running in Docker (Recommended)
1. You can visit the website for [How to Install Docker](https://docs.docker.com/engine/installation/)

2. Going into your workspace(Where you downloaded `cvpr2017_butler`) and run shell scripts 'run_in_docker.sh'
  ```shell
  sudo . run_in_docker.sh
  ```

#### Running in other method
1. Install [python](https://www.python.org/), [pip](https://pip.pypa.io/en/stable/installing/), libxml2, libxslt1, zlib1g, libffi, libssl, [Scrapy](https://doc.scrapy.org/en/latest/intro/install.html) and [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)
  ```shell
  sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
  sudo pip install --upgrade pip
  sudo pip install Scrapy
  sudo pip install beautifulsoup4

  ```
2. Going into your workspace(Where you downloaded `cvpr2017_butler`) and run shell scripts 'execute_in_local.sh'
  ```shell
  cd <where you downloaded>/cvpr2017_butler
  sudo . execute_in_local.sh
  ```

#### Viewing the Result
 After successful running, you can see `cvpr_lib@docker` folder if you run on Docker, or named `cvpr_lib@local` if you run it from local, in the root dir of your `cvpr_butler` project. To simplify, we will call it `cvpr_lib@blabla`. Followed is the descriptions:
  1. In `cvpr_lib@blabla` there will be papers organized by topics(3D Computer Vision/Machine Learning/Bla Bla Bla...) as main-dirs and sessions(oral/spotlight/poster) as sub-dirs.
  2. `cvpr_lib@blabla/Zi Other Files/` is for buffering storage downloading from website. Files like supplementaries and html descriptions are there. If you want to check csv-format inforamtion about CVPR2017, check `cvpr2017.csv` and `stat.csv`.


## Other words
1. It may take a while for downloading (20 minutes or so, as the whole bunch is 3.8GB, with 1850 pages visiting) If you want to enhance the performance, you can modified `settings.py` in `cvpr2017_butler/butler/butler`, try to increase **CONCURRENT_REQUESTS** and **CONCURRENT_REQUEST_PER_DOMAIN**. But if show error like **Connection to the other side was lost in a non-clean fashion**, low them down
2. If you want to display **DEBUG** information for Scrapy, modified in the same `settings.py` in `cvpr2017_butler/butler/butler` and set **LOG_LEVEL** to **'DEBUG'**
3. Somewhere still remains slightly-hardcodes. Sorry for that
4. There may be some paper have odd characters in their pics. Though very few but still sorry for that
5. If you have any problems, feel free to contact with me at mengyuethu@gmail.com
