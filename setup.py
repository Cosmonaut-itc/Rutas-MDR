from cx_Freeze import setup, Executable

base = None    

executables = [Executable("rutaMaps.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Rutas la Mejicana",
    options = options,
    version = "1.0.1",
    description = 'Calculo de rutas La Mejicana',
    executables = executables
)