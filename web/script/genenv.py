import os

from django.core.management.utils import get_random_secret_key


def generate_env() -> None:
    """
    Generate default env file

    Generate file name is ".env"
    Regenerate django secret key
    """

    # Check exist .evn file
    is_exist_env_file: bool = os.path.exists(".env")
    if is_exist_env_file:
        print('already exists ".env"')
    else:
        secret_key: str = get_random_secret_key()
        writelines: list[str] = [
            "# Basic Setting\n",
            "ALLOWED_HOSTS=*\n",
            "INTERNAL_IPS=127.0.0.1\n",
            f"SECRET_KEY={secret_key}\n",
            "\n",
            "# Database\n",
            "DB_NAME=db\n",
            "DB_USER=admin\n",
            "DB_PASSWORD=password\n",
            "DB_HOST=run-make-db\n",
            "DB_PORT=5432\n",
            "\n",
            "# Email\n",
            "EMAIL_HOST=\n",
            "EMAIL_HOST_USER=\n",
            "EMAIL_HOST_PASSWORD=\n",
            "EMAIL_PORT=\n",
            "DEFAULT_FROM_EMAIL=\n",
            "\n",
            "# Unique\n",
            "SUPPORT_EMAIL_ADDRESS=support@example.com\n",
        ]
        with open(".env", mode="w", newline="\n") as f:
            f.writelines(writelines)


if __name__ == "__main__":
    generate_env()
