# mvt-bugreport-dumpsys-settings-poc
PoC for a MVT module to extract **Settings** form dumpsys and use it on bugreports analisys

## Run
### 1. Clone the repo and enter to the directory:
`git clone https://github.com/karisma-klab/mvt-bugreport-dumpsys-settings-poc.git`
`cd mvt-bugreport-dumpsys-settings-poc`

### 2. Create virtual env and activate:
`python3 -m venv venv`
`source venv/bin/activate`

### 3. Install MVT:
`pip install mvt`

### 4. Run the module:
`python3 run_module.py path/to/bugreport/extraction` 
The path could be a .zip file or a directory resulted of a bugreport

