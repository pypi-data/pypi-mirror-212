import typer

target_option = typer.Option(
    None,
    "--target",
    "-t",
    help="Target connection configuration as defined as an amora.target.Target",
)

models_option = typer.Option(
    [],
    "--model",
    help="A model to be compiled. This option can be passed multiple times.",
)

force_option = typer.Option(
    False,
    "--force",
    help="Flag to force Amora to recompile all models.",
)
