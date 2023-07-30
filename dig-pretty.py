#!/usr/bin/env python3

import yaml
import sys


def run_dig(args):
    import subprocess

    cmd = ["dig"] + args
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode("utf-8")


def pretty_print(output):
    try:
        parsed = yaml.safe_load(output)
    except:
        print(output)
        return

    if len(parsed) == 0:
        raise Exception("No output from dig")
    if len(parsed) > 1:
        for p in parsed:
            print(f"======== Querying: {p['message']['response_address']} =========")
            print("")

            print_record(p["message"]["response_message_data"])
        return
    resp = parsed[0]
    server = f"{resp['message']['response_address']}:{resp['message']['response_port']}"
    print(f"SERVER: {server} ({resp['message']['socket_protocol']})")
    print_record(resp["message"]["response_message_data"])


def format_record(q):
    parts = q.split()
    name, ttl, _class, typ = parts[:4]
    answer = " ".join(parts[4:])
    # Don't include the class because it's basically always IN and I find it
    # redundant.
    # This is maybe a controversial decision but I have personally never seen a
    # HESIOD or CHAOS DNS record in my life.
    return f"{name}\t{ttl}\t{typ}\t{answer}"


def format_question(q):
    name, cls, typ = q.split()
    # again, leave out the class
    return f"{name}\t{typ}"


def color(text, color):
    if color == "green":
        return "\033[92m" + text + "\033[0m"
    elif color == "red":
        return "\033[91m" + text + "\033[0m"
    else:
        raise Exception(f"unknown color {color}")


def color_status(status):
    if status == "NOERROR":
        return color(status, "green")
    else:
        return color(status, "red")


def print_record(data):
    print("HEADER:")
    print(f"  status: {color_status(data['status'])}")
    print(f"  opcode: {data['opcode']}")
    print(f"  id: {data['id']}")
    print(f"  flags: {data['flags']}")
    print(
        f"  records: QUESTION: {data['QUESTION']}, ANSWER: {data['ANSWER']}, AUTHORITY: {data['AUTHORITY']}, ADDITIONAL: {data['ADDITIONAL']}"
    )
    print("")
    if "OPT_PSEUDOSECTION" in data:
        print("OPT PSEUDOSECTION:")
        for k, v in data["OPT_PSEUDOSECTION"].items():
            values = ", ".join([f"{k}: {v}" for k, v in v.items()])
            print(f"  {k}: {values}")
        print("")
    if "QUESTION_SECTION" in data:
        print("QUESTION SECTION:")
        for q in data["QUESTION_SECTION"]:
            print(f"  {format_question(q)}")
        print("")
    if "ANSWER_SECTION" in data:
        print("ANSWER SECTION:")
        for q in data["ANSWER_SECTION"]:
            print(f"  {format_record(q)}")
        print("")
    if "AUTHORITY_SECTION" in data:
        print("AUTHORITY SECTION:")
        for q in data["AUTHORITY_SECTION"]:
            print(f"  {format_record(q)}")
        print("")
    if "ADDITIONAL_SECTION" in data:
        print("ADDITIONAL SECTION:")
        for q in data["ADDITIONAL_SECTION"]:
            print(f"  {format_record(q)}")
        print("")


if __name__ == "__main__":

    args = sys.argv[1:]
    args.append("+yaml")
    output = run_dig(args)
    pretty_print(output)
