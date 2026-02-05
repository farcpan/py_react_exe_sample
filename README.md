# py_react_exe_sample

## api

```bash
pip install uvicorn fastapi
```

---

## installer

```bash
pyinstaller app.py --onedir --noconsole ★これでOK
pyinstaller app.py --onedir ★コンソールを閉じるとexeをkillできるので、こっちの方が良いかも
```


`dist/*.exe`, `dist/_internal`, `config.json`および`frontend`フォルダを配布する。

```
app.exe
\_internal
config.json
\frontend
```

---
