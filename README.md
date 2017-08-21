# cvpr2017_butler
A super-fast lightweight gadget to download, organize [cvpr2017](http://cvpr2017.thecvf.com/) papers from [CVF website](http://openaccess.thecvf.com/menu.py), also do listing and statistics (future version)

## Motivation
1. Hard to download all papers for [cvpr2017](http://cvpr2017.thecvf.com/)
2. Even you can download it, still hard to organize it manually

## Features
1. **Really fast** download speed because of multiprocessing. Multiple times than *wget*
2. Organized **wisely**. Use topic-wise and session-wise dir structure to manage your papers.
3. Also downloads supplemental materials for papers 
4. Human readable status during downloading

## Quick guide

### Prerequisites

1. Currently work well on Ubuntu 16.04
2. You computer can visit website to [Computer Vision Foundatiion open access](http://openaccess.thecvf.com)
3. Minimum 4GB disk storage on your workspace

### Installation and Running

#### Installation
1. Using installtion scripts from the software root directory. (Installing intltool and mwget)
  ```shell
  . setup.sh

  ```
#### Running
1. Using running scripts from the software root directory.
  ```shell
  . run.sh

  ```
#### Viewing the Result
After successful running, you can see papers and supplemental materials in `<software directory>/cvpr_lib@local/papers`

## Other words
1. It may take a while for downloading
2. Somewhere still remains slightly-hardcodes. Sorry for that
3. There may be some paper have odd characters in their pics. Though very few but still sorry for that
4. If you have any problems, feel free to contact with me at mengyuethu@gmail.com
