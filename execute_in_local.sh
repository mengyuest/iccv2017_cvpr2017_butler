#!/bin/bash

# Step 1: Download papers from website
cd butler
scrapy crawl paper_spider

# Step 2: Organize paper in proper structure
cd ..
python manager.py
python worker.py
