# cvpr2017_butler
A super-fast lightweight gadget to download, organize [cvpr2017](http://cvpr2017.thecvf.com/) papers from [CVF website](http://openaccess.thecvf.com/menu.py), also do listing and statistics (future version)

## Features
1. **Really fast** download speed because of multiprocessing. Multiple times than *wget*
2. Organized **wisely**. Use topic-wise and session-wise dir structure to manage your papers.
3. Also downloads supplemental materials for papers
4. Human readable status during downloading

## Quick guide

### Prerequisites
1. Currently work well on Ubuntu 16.04
2. Available to visit website to [Computer Vision Foundatiion open access](http://openaccess.thecvf.com)
3. Minimum 4GB disk storage in your workspace

### Installation and Running

#### Installation
1. Make sure your system has installed python
2. Using installtion scripts from the software root directory. (Installing intltool and mwget)
  ```shell
  . setup.sh

  ```
#### Running
1. Using running scripts from the software root directory.
  ```shell
  . run.sh

  ```
2. After successful running, you can see papers and supplemental materials in `<software directory>/cvpr_lib@local/papers`

## Other words
1. If your system don't need to use `sudo` for commands, you can delete them in setup.sh and run.sh.
2. There may be one or two papers having odd characters in their pics. Though very few but still sorry for that
3. If you have any problems, feel free to contact with me at mengyuethu@gmail.com
