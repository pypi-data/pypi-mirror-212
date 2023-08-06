import typer
import shutil
import pandas as pd
from pathlib import Path
from rich.progress import track

# Creating a typer app
app = typer.Typer()

# Defining a function to move files based on cluster column
def move_files(input_csv: Path, path_col: str, cluster_col: str, copy: bool, output_dir: Path):
    # Reading the csv file using pandas
    df = pd.read_csv(input_csv)
    # Looping over the rows of the dataframe
    desc = "Copying files..." if copy else "Moving files..."
    for row in track(df.itertuples(), description=desc):
        # Getting the file path and cluster from the row
        file_path = Path(getattr(row, path_col))
        cluster = getattr(row, cluster_col)
        # Creating a subdirectory for the cluster if it does not exist
        cluster_dir = output_dir / cluster
        cluster_dir.mkdir(exist_ok=True)
        destination = cluster_dir / file_path.name
        if file_path.exists():
            if destination.exists():
                stem = destination.stem
                suffix = destination.suffix
                counter = 1
                while True:
                    new_stem = f"{stem}-{counter}"
                    destination = destination.with_name(new_stem + suffix)
                    if destination.exists():
                        counter+=1
                    else:
                        break
            if copy:
                # Copying the file to the cluster subdirectory
                shutil.copy(file_path, destination)
            else:
                # Moving the file to the cluster subdirectory
                file_path.rename(destination)
        else:
            pass

# Defining a command for the app that takes the arguments from the user
@app.command()
def run(
    input_file: Path = typer.Argument(..., help="The input csv file"),
    path: str = typer.Option("path", help="The name of the path column"),
    cluster: str = typer.Option("cluster", help="The name of the cluster column"),
    copy: bool = typer.Option(False, "--copy/--move", help="Whether or not to copy instead of move"),
    output: Path = typer.Option('.', help="The output directory")
):
    # Calling the move_files function with the arguments
    move_files(input_file, path, cluster, copy, output)

# TODO Handle duplicate files in the destination
