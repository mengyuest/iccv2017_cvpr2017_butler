#!/usr/bin/env python  
# -*- coding: utf-8 -*-  

import csv
import os
import shutil
import errno
from multiprocessing import Process, Pool, Value, Manager
from datetime import datetime
import urllib2
import ConfigParser
import os.path

config = ConfigParser.ConfigParser()


def download(todoitem):
    paper_dir = todoitem[0]
    session_dir = todoitem[1]
    paper_path = todoitem[2]
    dtype = todoitem[3]
    if dtype == "paper":
        command = "mwget -d \"" + paper_dir + "\" -n " + str(connect_num.value) + \
                  " -t 90 " + config.get(mode, "paper") + paper_path
        os.system(command)
    if dtype == "appendix":
        os.system("mwget -d \"" + paper_dir + "\" -n " + str(connect_num.value) + \
                  " -t 90 " + config.get(mode, "appendix") + paper_path)

    while os.path.isfile(paper_dir + paper_path) == False:
        os.system("echo \"\\033[0;33m[NOT FOUND] " + paper_path + "\\033[0m \"")
        os.system("echo \"\\033[0;33m[DONT WORRY] We will try again~ \\033[0m \"")
        os.system("rm -f " + paper_dir + paper_path + ".mg!")

        if dtype == "paper":
            command = "mwget -d \"" + paper_dir + "\" -n " + str(connect_num.value) + \
                      " -t 90 " + config.get(mode, "paper") + paper_path
            os.system(command)
        if dtype == "appendix":
            os.system("mwget -d \"" + paper_dir + "\" -n " + str(connect_num.value) + \
                      " -t 90 " + config.get(mode, "appendix") + paper_path)

    shutil.move(paper_dir + paper_path, session_dir + paper_path)
    os.system("rm -f " + paper_dir + paper_path + ".mg!")
    file_size.value = file_size.value + os.path.getsize(session_dir + paper_path)
    file_downloaded.value = file_downloaded.value + 1
    os.system("echo \"\\033[1;32m[GET] " + paper_path + "\\033[0m \"")
    os.system("echo \"\\033[1;32m[NOW] " + str(file_downloaded.value) + \
              "/" + str(file_todo.value) + " files downloaded" + \
              "\\033[0m \"")


def standarize_html(doc):
    doc = doc.replace("“", "\"")
    doc = doc.replace("”", "\"")
    doc = doc.replace("—", "-")
    doc = doc.replace("°", "deg")
    doc = doc.replace("é", "e")
    doc = doc.replace("&", "and")
    doc = doc.replace("č", "c")
    doc = doc.replace("ć", "c")
    doc = doc.replace("ğ", "g")
    doc = doc.replace("á", "a")
    doc = doc.replace("ü", "u")
    doc = doc.replace("Ö", "O")
    doc = doc.replace("ö", "o")
    doc = doc.replace("š", "s")
    doc = doc.replace("ý", "y")
    doc = doc.replace("ä", "a")

    return doc


def standarize_csv(doc):
    doc = doc.replace("\,", "$")
    doc = doc.replace(",", "\t")
    doc = doc.replace("$", ",")
    doc = doc.replace("\\\"", "\"")
    doc = doc.replace("--", "-")
    doc = doc.replace("&", "and")
    return doc


if __name__ == "__main__":

    config.read("config.ini")

    dt_start = datetime.now()

    server = Manager()

    mode = config.get("general", "source")

    print("You have choose to download papers and other materials from " + config.get(mode, "title") + " :-)")
    print("Preparing...")

    process_num = config.getint("general", "process_num")
    connect_num = server.Value('i', 4)

    file_size = server.Value('d', 0)

    file_sum = server.Value('i', 0)
    file_saved = server.Value('i', 0)
    file_downloaded = server.Value('i', 0)
    file_todo = server.Value('i', 0)

    root_path = config.get(mode, "root_path")  # "cvpr_lib@local/"  # server.Value(c_char_p, "cvpr_lib@local/")
    src_path = root_path + config.get("general",
                                      "src_path")  # "Zi Other Files/"  # server.Value(c_char_p, root_path+"Zi Other Files/")
    paper_dir = root_path + config.get("general",
                                       "paper_dir")  # "papers/"  # server.Value(c_char_p, root_path+"papers/")

    if not os.path.exists(root_path):
        try:
            os.makedirs(root_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    if not os.path.exists(src_path):
        try:
            os.makedirs(src_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # DOWNLOAD schedule html and turn to csv file
    # Almost same but iccv has one more column called session chair...

    print("Downloading schedule csv files ...")
    stat_csv = urllib2.urlopen(config.get(mode, "schedule_url"))
    w1 = open(src_path + config.get(mode, "html_file"), 'wb')
    w1.write(stat_csv.read())
    w1.close()

    w1 = open(src_path + config.get(mode, "html_file"), 'r')
    w2 = open(src_path + config.get(mode, "csv1_file"), 'wb')

    pencil = csv.writer(w2, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    pencil.writerow(['TOPIC', 'SESSION', 'ID', 'PAPER', 'AUTHOR'])

    csv_content = ['NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL']

    lines = w1.readlines()

    col_id = 0
    start_trim = False

    col_offset = config.getint(mode, "col_offset")

    for line in lines:
        if start_trim == True:
            if "</table>" in line:
                break
            else:
                if "</tr" in line and csv_content[5] != "NULL":
                    col_id = 0
                    pencil.writerow(
                        [csv_content[5], csv_content[4], csv_content[6 + col_offset], csv_content[7 + col_offset],
                         csv_content[8 + col_offset]])

                elif "<td " in line:
                    strs = line.strip().split('>')
                    for item in strs:
                        item = item.strip()
                        if item != "" and item[0] != '<':
                            csv_content[col_id] = standarize_html(item.strip().split('<')[0].strip())
                            break
                    col_id = col_id + 1

        elif "Program Schedule" in line and "<h4" in line:
            start_trim = True

        else:
            continue

    w2.close()
    w1.close()

    # READ from that mapping csv file where CVPR has but ICCV we need to create our own

    print("Trying to get mapping priors...")

    if mode == "cvpr2017":
        os.system("mwget -d \"" + src_path + "\" -n 4 " + \
                  "-t 90 " + config.get(mode, "mapping_url"))

        f2 = open(src_path + config.get(mode, "csv2_file"), 'r')
        f3 = open(src_path + config.get(mode, "csv3_file"), 'wb')

        doc = f2.read()
        doc = standarize_csv(doc)

        f3.write(doc)

        f2.close()
        f3.close()

    else:

        paper_mapping_html = urllib2.urlopen(config.get(mode, "paper_mapping_url"))
        f_prior = open(src_path + config.get(mode, "paper_prior_file"), 'wb')
        f_prior.write(paper_mapping_html.read())
        f_prior.close()

        appendix_mapping_html = urllib2.urlopen(config.get(mode, "appendix_mapping_url"))
        f_prior = open(src_path + config.get(mode, "appendix_prior_file"), 'wb')
        f_prior.write(appendix_mapping_html.read())
        f_prior.close()

        f_prior = open(src_path + config.get(mode, "paper_prior_file"), 'r')
        f_schedule = open(src_path + config.get(mode, "csv1_file"), 'r')
        f_csv = open(src_path + config.get(mode, "csv2_file"), 'w')

        pencil = csv.writer(f_csv, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        csv_content = ['NULL', 'NULL', 'NULL', 'NULL']

        lines = f_prior.readlines()

        tmp_log = dict()

        for line in lines:

            if ".pdf" in line:
                pdf_link = (line.split(".pdf\">")[1].split(".pdf")[0] + ".pdf").strip()

                keywords = pdf_link.split("_")

                author_last_name = keywords[0]

                paper_first_word = keywords[1]

                paper_second_word = keywords[2]

                paper_third_word = keywords[3]

                if author_last_name.strip() + "_" + paper_first_word.strip() + "_" + paper_second_word.strip() + "_" + paper_third_word.strip() in tmp_log:
                    print(666)

                tmp_log[
                    author_last_name.strip() + "_" + paper_first_word.strip() + "_" + paper_second_word.strip() + "_" + paper_third_word.strip()] = [
                    pdf_link]

                findfind = False

        f_prior.close()

        f_prior = open(src_path + config.get(mode, "appendix_prior_file"), 'r')
        lines = f_prior.readlines()

        for line in lines:
            if ".pdf" in line:
                pdf_link = (line.split(".pdf\">")[1].split(".pdf")[0] + ".pdf").strip()
                keywords = pdf_link.split("_")
                author_last_name = keywords[0]
                paper_first_word = keywords[1]
                paper_second_word = keywords[2]

                paper_third_word = keywords[3]
                tmp_log[
                    author_last_name.strip() + "_" + paper_first_word.strip() + "_" + paper_second_word.strip() + "_" + paper_third_word.strip()].append(
                    pdf_link)

        f_prior.close()

        schedule_lines = f_schedule.readlines()
        for keys in tmp_log:

            keyword = keys.split("_")
            author_last_name = keyword[0]
            paper_first_word = keyword[1]
            paper_second_word = keyword[2]
            paper_third_word = keyword[3]
            findfind = False
            for schedule_line in schedule_lines:
                if author_last_name in schedule_line and paper_first_word in schedule_line:

                    findfind = True

                    data = tmp_log[keys]

                    sec_data = schedule_line.split("\t")

                    csv_content[0] = sec_data[3].strip()
                    csv_content[1] = sec_data[4].strip()
                    csv_content[2] = "content_ICCV_2017/papers/" + data[0].strip()
                    if len(data) == 2:
                        csv_content[3] = "content_ICCV_2017/supplemental/" + data[1].strip()
                    else:
                        csv_content[3] = "None"
                    pencil.writerow(csv_content)
                    break

        f_csv.close()

    # COMBINE two csv and find what url to download

    f1 = open(src_path + config.get(mode, "csv1_file"), 'r')

    f3 = open(src_path + config.get(mode, "csv3_file"), 'r')

    catalog = csv.reader(f1, delimiter='\t', quotechar="|")
    mapping = csv.reader(f3, delimiter='\t', quotechar='|')

    if not os.path.exists(paper_dir):
        try:
            os.makedirs(paper_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    todolist = []

    count = 0
    matched_count = 0
    for row in enumerate(catalog):
        if count == 0:
            count = 1
            continue
        topic_name = row[1][0]
        topic_dir = paper_dir + topic_name + "/"
        if not os.path.exists(topic_dir):
            try:
                os.makedirs(topic_dir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

        session_name = row[1][1]
        session_dir = topic_dir + session_name + "/"
        if not os.path.exists(session_dir):
            try:
                os.makedirs(session_dir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

        paper_name = row[1][3].strip()

        f3.seek(0)

        no_matched = True

        for sec_row in enumerate(mapping):
            if (sec_row[1][0][0] == paper_name[0] and sec_row[1][0][1] == paper_name[1]):
                if sec_row[1][0].strip() == paper_name:
                    no_matched = False
                    matched_count = matched_count + 1
                    paper_path = sec_row[1][2].split("/")[2]

                    if (sec_row[1][3] != "None"):
                        appendix_path = sec_row[1][3].split("/")[2]
                        matched_count = matched_count + 1
                    else:
                        appendix_path = "None"
                    isPaperFound = False
                    isAppendixFound = False
                    for root, dirs, files in os.walk(session_dir):
                        if paper_path in files:
                            isPaperFound = True
                            os.system("echo \"\\033[1;32m[FOUND] paper: " + paper_path + "\\033[0m \"")
                            break
                        if appendix_path in files:
                            isAppendixFound = True
                            os.system("echo \"\\033[1;32m[FOUND] appendix: " + appendix_path + "\\033[0m \"")
                            break

                    if isPaperFound != True:
                        dtype = "paper"
                        todolist.append([paper_dir, session_dir, paper_path, dtype])

                    if appendix_path != "None" and isAppendixFound != True:
                        dtype = "appendix"
                        todolist.append([paper_dir, session_dir, appendix_path, dtype])

                    break

    f1.close()
    f3.close()

    file_sum.value = matched_count
    file_todo.value = len(todolist)
    pool = Pool(process_num)
    pool.map(download, todolist)

    print
    os.system("echo \"\\033[1;32mSuccessfuly received " + str(file_sum.value) + \
              " files from " + config.get(mode, "title") + ", " + "\\033[0m \"")
    os.system("echo \"\\033[1;32mwith " + str(file_downloaded.value) + " files downloaded and " + \
              str(file_sum.value - file_downloaded.value) + " files that already had" + "\\033[0m \"")

    dt_end = datetime.now()
    time_interval = (dt_end - dt_start).seconds
    download_speed = file_size.value / 1024 / time_interval
    os.system("echo \"\\033[1;32mElapse time: " + (str)(time_interval) + "s" + "\\033[0m \"")
    os.system("echo \"\\033[1;32mDownload speeds: " + (str)(download_speed) + "KB/s" + "\\033[0m \"")
