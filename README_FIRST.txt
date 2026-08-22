SMART HOME AI - CLEAN FINAL PROJECT
====================================

This package is built from the latest uploaded final_app3 code.

IMPORTANT:
- There is NO Streamlit 'pages' folder in this project.
- Do not copy any old app.py over this app.py.
- Keep your old project as a backup.

FOLDER STRUCTURE
----------------
SmartHome_AI_LATEST_CLEAN/
  app.py
  requirements.txt
  run_app.bat
  install_requirements.bat
  database/
      (copy your existing SmartHome.db or smarthome.db here)
  uploads/
      (copy your old uploads folder contents here if you want old documents)
  ai/
  modules/

FIRST RUN
---------
1. Extract this ZIP.
2. Copy your old database file into the database folder.
   Preferred name: SmartHome.db
   smarthome.db is also accepted.
3. Open this folder.
4. Double-click install_requirements.bat once.
5. Double-click run_app.bat.
6. The app opens in your browser.

COMMAND-LINE ALTERNATIVE
------------------------
pip install -r requirements.txt
python -m streamlit run app.py

DATABASE
--------
The app now looks inside the database folder, not the project root.
If database/SmartHome.db exists, it is used first.
Otherwise database/smarthome.db is used/created.

DOCUMENTS
---------
The app stores uploaded user documents under uploads/<user_email>/.
If you have an old uploads folder, copy its contents into this project's uploads folder.

IF AN ERROR APPEARS
-------------------
Stop the Streamlit window (Ctrl+C), then send a screenshot of the full CMD error.
Do not modify app.py randomly.
