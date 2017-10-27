# iccv2017_cvpr2017_butler
A super-fast lightweight gadget to **download**, **organize** [cvpr2017](http://cvpr2017.thecvf.com/) papers and [iccv2017](http://iccv2017.thecvf.com) papers from [CVF website](http://openaccess.thecvf.com/menu.py), also do listing and statistics

## Features
1. **Really fast** download speed because of multiprocessing. Multiple times than *wget*
2. **Organized wisely**. Use topic-based and session-based directory structure to manage your papers
3. Also downloads supplemental materials for papers
4. Human readable status during downloading
5. **Support to download latest iccv2017 papers now!**

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
0. Using running scripts from the software root directory, default setting is to download cvpr2017 papers.
  ```shell
  . run.sh

  ```
1. If you want to download iccv2017 papers, just open the `config.ini` file, modify the value of `source` in `[general]` section from `cvpr2017` to `iccv2017`, and then do the same operation in step 0. If you want to download cvpr2017, just modify it back. 
2. After successful running, you can see papers and supplemental materials in `<software directory>/cvpr2017/papers` or `<software directory>/iccv2017/papers`

## Other words
0. Normally take 20 mins or so to download all the papers
1. If your system don't need to use `sudo` for commands, you can delete them in setup.sh and run.sh
2. There may be one or two cvpr2017 papers having odd characters in their pics. Though very few but still sorry for that
3. I used hard-code for searching iccv2017 papers and deal with author name which includes characters other than A(a)-Z(z), wondering what better option I have
4. If you have any problems, suggestions or interesting points, welcome to contact with me at mengyuethu@gmail.com
