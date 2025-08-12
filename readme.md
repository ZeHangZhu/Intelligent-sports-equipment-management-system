     # Sport Equipment Controller (SEC)
Refer to `"./help/sec.help.md"` for related help documentation.
Used to manage equipment in the equipment room, and can also be used for managing experimental equipment, books, etc.

## Installation
### Install ollama
1. Visit [ollama](https://ollama.com/) to install the ollama framework.
2. Execute `ollama run qwen2.5:7b` to install the model.
3. Wait for the model installation to complete.

### Install Dependencies
Enter the directory and execute the following command in cmd to install the dependencies:
```bash
pip install -r requirements.txt
```
Ensure that the dependencies are properly installed.

## Documentation
Maintenance documentation can be found in the `\doc` folder.
| File Name | Documentation |
|---|---|
| chart.py | "\doc\chart.py.doc.md" |
| db.py | "\doc\db.py.doc.md" |
| MDViewer.py | "\doc\MDViewer.py.doc.md" |
| sec-GUI.py | "\doc\sec-GUI.py.doc.md" |
| server.py | "\doc\server.py.doc.md" |

## Start Network Service
Run `RunServer.bat` to start the server.

## Start GUI Interface
Open the command prompt and navigate to the directory containing the setup.py file.
Run the following command to start the GUI interface:
```bash
python sec-GUI.py
```

## Compile GUI Interface (Optional)
1. Install the pyinstaller library by executing the following command:
```bash
pip install pyinstaller
```
2. Run `Compile.bat` to compile the GUI into an executable exe file.
3. Enter the `dist\sec-GUI` folder and copy the `\data`, `\help`, `web`, and `\ICONs` folders to the same directory as `sec-GUI.exe`.
4. Run `sec-GUI.exe` to start the GUI interface.
        