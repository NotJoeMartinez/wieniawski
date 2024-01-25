import os
import click
from dotenv import load_dotenv

load_dotenv(".env")

WIENIAWSKI_VERSION = '0.1.0'

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(WIENIAWSKI_VERSION , message='Wieniawski version: %(version)s')
def cli():
    pass


@cli.command()
@click.option("--model-name", "-m", required=True, help="Path to the model")
def train(model_name):

    train_data_path = os.getenv("TRAIN_DATA_PATH")

    if os.path.exists(f"{train_data_path}/models/{model_name}.sav"):
        print(f"Model {model_name} already exists")
        exit(1)
    
    from .train_model import train

    train('NN', 'hog', model_name)



