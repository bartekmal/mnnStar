pyinstaller ^
    --paths="src" ^
    --add-data="../input;input" ^
    --add-data="../src/resources;src/resources" ^
    --specpath="install" ^
    --workpath="install/build" ^
    --distpath="install" ^
    --name="PhyStar" ^
    --onefile ^
    main.py