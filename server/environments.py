from os import getenv, getcwd, sep
import shutil
import dotenv, string, random

class EnvGenerator:

    def __init__(self):
        self.dotenv_path = f"{getcwd()}/.env.example"
        self.new_dotenv_path = f"{getcwd()}/.env"

    def generate_key(self, length, chars=string.ascii_letters + string.digits):
        return "".join(random.choice(chars) for _ in range(length))

    def generate_salt(self, length, chars=string.ascii_letters + string.digits + string.punctuation):
        return "".join(random.choice(chars) for _ in range(length))

    def create_env(self):
        secret_key = self.generate_key(32)

        shutil.copy(self.dotenv_path, self.new_dotenv_path)

        dotenv.load_dotenv(self.new_dotenv_path)
        dotenv.set_key(self.new_dotenv_path, "SECRET_KEY", secret_key)

        db_file = getenv("DATABASE_FILE")

        dotenv.set_key(self.new_dotenv_path, "SQLALCHEMY_DATABASE_URI", f"sqlite:///{db_file}")

if __name__ == "__main__":
    generator = EnvGenerator()
    generator.create_env()