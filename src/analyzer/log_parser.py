
import re


def parse_logs(log_text):
    parsed_logs = []

    pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2}\s+)?"
        r"(\d{2}:\d{2}:\d{2})\s+"
        r"(INFO|DEBUG|WARNING|WARN|ERROR|CRITICAL)\s+"
        r"(.+)",
        re.IGNORECASE
    )

    for line in log_text.splitlines():
        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)

        if match:
            date_part, time_part, level, message = match.groups()

            timestamp = (
                f"{date_part.strip()} {time_part}"
                if date_part
                else time_part
            )

            parsed_logs.append({
                "timestamp": timestamp,
                "level": level.upper(),
                "message": message.strip()
            })

    return parsed_logs
