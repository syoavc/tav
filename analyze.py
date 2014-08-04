"""
    Text Analysis and Visualization system

    Analyzing and visualizing the stats from the DAAP system.
    Going over the raw text file and the corresponding stats file. Creating an HTML file with
    different styles that represent different sections in the text. In addtion produces statistics
    for the various combinations of the measures.
"""
import sys
import re
import json
import argparse
import logging

import numpy as np
import pandas as pd


def main():
    args = parse_args()
    conf = json.load(open(args.conf))

    if args.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    )

    logging.info("Starting analysis")

    logging.info("Creating dataframe and calculating conditions")
    raw = pd.read_csv(conf["raw_file"])

    # opening measures file and adding the word and speaker columns
    measures = pd.read_csv(conf["measures_file"])
    measures["Word"] = raw["Word"]
    measures["Spkr"] = raw["Spkr"]

    # removing second speaker
    measures = measures[raw["Spkr"] == 1]

    measures = measures_cond(measures, conf["cond"])
    logging.info("Done - creating dataframe and calculating conditions")

    logging.info("Calculating stats")
    stats(conf, measures)

    if args.stats_only:
        sys.exit(0)

    html_out = """
        <html>
        <head>
        <style type="text/css">
        .DFS1-0 {font-size:medium;}
        .DFS1-1 {font-size:large;}
        .DFS1-2 {font-size:x-large;}
        .RS1-0 {background-color:#99FF00;}
        .RS1-1 {}
        .RS1-2 {background-color:yellow;}
        .WRADS1-0 {font-style:italic;}
        .WRADS1-1 {}
        .WRADS1-2 {text-decoration:underline;}
        p {color:blue;}
        .interviewee {color:black;}

       .fixedElement {
            background-color: #c0c0c0;
            position:fixed;
            top:0;
            width:100%;
            z-index:100;
        }

        </style>
        </head>

        <body>
        <div class="fixedElement"><b>Legend: </b><span class="DFS1-0">DFS1-0 </span><span class="DFS1-1">DFS1-1 </span><span class="DFS1-2">DFS1-2 </span><span class="RS1-0">RS1-0 </span><span class="RS1-1">RS1-1 </span><span class="RS1-2">RS1-2 </span><span class="WRADS1-0">WRADS1-0 </span><span class="WRADS1-1">WRADS1-1 </span><span class="WRADS1-2">WRADS1-2 </span></div>
        &nbsp;
    """

    logging.info("Going over words")
    f = open(conf["text_file"])
    word_idx = 0
    cnt = 1

    for line in f.readlines():
        if not line.startswith("\\s 1"):  # not interviewee text - sending to output as is
            html_out += '<p class="nochange">{}</p>'.format(line)
        else:
            # removing prefix
            line = line.lstrip("\\s 1 ")

            # removing paranthesis
            line = re.sub(" *\(.*?\)[,\.]* *", " ", line)
            line = re.sub(" *\[.*?\][,\.]* *", " ", line)

            # replacing weird 92 char with single quote
            line = line.replace('\x92', "'")

            # removing extra spaces
            line = re.sub(" +", " ", line)

            line = line.strip()

            html_out += '<p class="interviewee">'

            # tokenizing
            words = line.split(" ")
            prev_classes = None
            for word in words:
                # checking if the word containing ' (two words)
                if "'" in word and word[-1] != "'":
                    sub_words = word.split("'")

                    new_classes, measures_word = check_cond(conf, measures, word_idx)
                    html_out += add_word_to_output(sub_words[0], prev_classes, new_classes)
                    logging.debug("Words: {}  --- {}".format(measures_word, sub_words[0]))
                    # check_words(measures_word, sub_words[0])
                    word_idx += 1
                    prev_classes = new_classes

                    html_out += "'"

                    new_classes, measures_word = check_cond(conf, measures, word_idx)
                    html_out += add_word_to_output(sub_words[1], prev_classes, new_classes)
                    logging.debug("Words: {}  --- {}".format(measures_word, sub_words[1]))
                    # check_words(measures_word, sub_words[1])
                    word_idx += 1
                    prev_classes = new_classes
                else:
                    new_classes, measures_word = check_cond(conf, measures, word_idx)
                    html_out += add_word_to_output(word, prev_classes, new_classes)
                    logging.debug("Words: {}  --- {}".format(measures_word, word))
                    # check_words(measures_word, word)
                    word_idx += 1
                    prev_classes = new_classes

                if not cnt % 1000:
                    logging.info("Done iterating over {} words".format(cnt))
                cnt += 1

            html_out += '</span></p>'

    logging.info("Writing html file")
    out = open(conf["out_file"], "w")
    out.write(html_out)
    out.close()

    logging.info("Done")


def add_word_to_output(word, prev_classes, new_classes):
    if prev_classes == new_classes:
        return word + " "
    else:
        return '</span><span class="{}">{}'.format(new_classes, word)


def check_words(df_word, text_word):
    if df_word.lower() not in text_word.lower():
        logging.exception("Words don't match: {} --- {}".format(df_word, text_word))


def check_cond(conf, df, line_num):
    ret = []
    for i in conf["cond"]:
        class_base_name = re.sub('[\W_]+', '', i[0])
        ret.append("{}-{}".format(class_base_name, df.iloc[line_num]["{}_val".format(i[0])]))

    return " ".join(ret), df.iloc[line_num]["Word"]


def measures_cond(df, cond):
    """Checking the measures conditions, and adding boolean columns accordingly to the dataframe"""
    def calc_cond(row, name, min_val, max_val):
        val = 0
        if row[name] >= min_val and row[name] <= max_val:
            val = 1
        elif row[name] > max_val:
            val = 2

        return val

    for cond_arr in cond:
        df["{}_val".format(cond_arr[0])] = df.apply(calc_cond, args=cond_arr, axis=1)

    return df


def stats(conf, df):
    """ Genereting the stats """
    num_of_words = len(df)
    # filtering according to stats config
    for fltr, val in conf['stats'].iteritems():
        df = df[df["{}_val".format(fltr)] == val]

    num_of_words_after_filter = len(df)

    logging.info("Number of words before filtering: {}".format(num_of_words))
    logging.info("Number of words after filtering: {} ({}%)".format(num_of_words_after_filter, float(num_of_words_after_filter) / num_of_words * 100))

    # counting only combinations over the consecutive threshold
    consecutive_groups = np.array_split(np.array(df.index), np.where(np.diff(np.array(df.index)) != 1)[0] + 1)
    count = 0
    for consecutive_group in consecutive_groups:
        if len(consecutive_group) >= conf["consecutive_threshold"]:
            count += len(consecutive_group)

    logging.info("Number of words after filtering, of groups of {} and more: {} ({}%)".format(conf["consecutive_threshold"], count, float(count) / num_of_words * 100))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--conf", default="conf.js", help="name of config file")
    parser.add_argument("--debug", default=False, action="store_true", help="debug mode")
    parser.add_argument("--stats-only", default=False, action="store_true", help="only calculate stats")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
