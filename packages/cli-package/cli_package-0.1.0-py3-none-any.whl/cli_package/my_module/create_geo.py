from pymxs import runtime as rt
def create(geo):
    if geo == "teapot":
        rt.Teapot()
    elif geo == "sphere":
        rt.Sphere()

    rt.saveMaxFile(r"C:\temp\hello_test.max")