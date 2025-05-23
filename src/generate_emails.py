import random
import string
from pathlib import Path


def random_email(length: int = 10) -> str:
    domain = ["@ya.ru", "@yohoo.com", "@gmai.com", "@mail.ru"]
    name = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{name}{random.choice(domain)}\n"


def main() -> None:
    target_size = 2 * 1024**3
    current_size = 0
    chunk_size = 1024 * 65
    with Path("emails.txt").open("w") as f:
        while current_size < target_size:
            buffer = [f"{random_email()}" for _ in random_email(chunk_size // 20)]
            f.writelines(buffer)
            current_size += chunk_size


if __name__ == "__main__":
    main()
