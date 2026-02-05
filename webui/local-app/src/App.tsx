import { useState } from "react";

function App() {
  const [files, setFiles] = useState([]);

  const createFile = async () => {
    await fetch("/api/files", { method: "POST" });
    fetchFiles();
  };

  const fetchFiles = async () => {
    const res = await fetch("/api/files");
    const data = await res.json();
    setFiles(data.files);
  };

  const downloadFile = async (filename: string) => {
    const res = await fetch(`/api/files/${filename}`);
    const blob = await res.blob();

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>FastAPI ↔ React + Download</h2>

      <button onClick={createFile}>POST: ファイル作成</button>
      <button onClick={fetchFiles} style={{ marginLeft: 10 }}>
        GET: 一覧取得
      </button>

      <ul>
        {files.map((f) => (
          <li key={f}>
            {f}
            <button
              style={{ marginLeft: 10 }}
              onClick={() => downloadFile(f)}
            >
              ダウンロード
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
