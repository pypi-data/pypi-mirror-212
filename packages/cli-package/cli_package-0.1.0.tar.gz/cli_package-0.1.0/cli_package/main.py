from pymxs import runtime as rt
import cli_package.my_module.create_geo
def main_cli() -> None:
    opts = rt.maxops.mxsCmdLineArgs
    geometry = opts[rt.name("geometry")]

    print(geometry)
    print(opts)

    cli_package.my_module.create_geo.create(geometry)
