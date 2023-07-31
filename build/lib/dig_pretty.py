#!/usr/bin/env python3

import yaml
import sys


def run_dig(args):
    import subprocess

    cmd = ["dig"] + args
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode("utf-8")


def pretty_print(output, is_tty):
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

            print_record(p["message"]["response_message_data"], is_tty)
        return
    resp = parsed[0]
    print_summary(resp)
    print_record(resp["message"]["response_message_data"], is_tty)


def print_summary(resp):
    # Prints a summary of the server/timing, not really sure about this formatting
    server = f"{resp['message']['response_address']}:{resp['message']['response_port']}"
    protocol = resp["message"]["socket_protocol"]
    size = resp["message"]["message_size"].rstrip("b")
    elapsed = resp["message"]["response_time"] - resp["message"]["query_time"]
    # convert timedelta to ms
    elapsed_ms = int(elapsed.total_seconds() * 1000)
    print(
        f"Received response from {server} ({protocol}), {size} bytes in {elapsed_ms}ms"
    )


def format_record(q, is_tty):
    parts = q.split()
    name, ttl, class_, type_ = parts[:4]
    answer = " ".join(parts[4:])
    # the colours here are arbitrary
    return f"{color(name, 'blue', is_tty)}\t{color(ttl, 'cyan', is_tty)}\t{class_}\t{color(type_, 'magenta', is_tty)}\t{color(answer, 'green', is_tty)}"


def format_question(q, is_tty):
    name, class_, type_ = q.split()
    return f"{color(name, 'blue', is_tty)}\t{class_}\t{color(type_, 'magenta', is_tty)}"


def color(text, color, is_tty):
    if not is_tty:
        return text
    if color == "green":
        return "\033[92m" + text + "\033[0m"
    elif color == "red":
        return "\033[91m" + text + "\033[0m"
    elif color == "yellow":
        return "\033[93m" + text + "\033[0m"
    elif color == "blue":
        return "\033[94m" + text + "\033[0m"
    elif color == "magenta":
        return "\033[95m" + text + "\033[0m"
    elif color == "cyan":
        return "\033[96m" + text + "\033[0m"
    else:
        raise Exception(f"unknown color {color}")


def color_status(status, is_tty):
    if status == "NOERROR":
        return color(status, "green", is_tty)
    else:
        return color(status, "red", is_tty)


def print_record(data, is_tty):
    print("HEADER:")
    print(f"  status: {color_status(data['status'], is_tty)}")
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
            print(f"  {format_question(q, is_tty)}")
        print("")
    if "ANSWER_SECTION" in data:
        print("ANSWER SECTION:")
        for q in data["ANSWER_SECTION"]:
            print(f"  {format_record(q, is_tty)}")
        print("")
    if "AUTHORITY_SECTION" in data:
        print("AUTHORITY SECTION:")
        for q in data["AUTHORITY_SECTION"]:
            print(f"  {format_record(q, is_tty)}")
        print("")
    if "ADDITIONAL_SECTION" in data:
        print("ADDITIONAL SECTION:")
        for q in data["ADDITIONAL_SECTION"]:
            print(f"  {format_record(q, is_tty)}")
        print("")


def main():
    args = sys.argv[1:]
    args.append("+yaml")
    # check if output is a pipe
    is_tty = sys.stdout.isatty()
    output = run_dig(args)
    pretty_print(output, is_tty)


if __name__ == "__main__":
    main()
