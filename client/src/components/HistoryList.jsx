import { useEffect, useState } from "react";
import { getAllSettings } from "../api/digicore.api";

export function HistoryList() {
  const [settings, setSettings] = useState([]);

  useEffect(() => {
    async function loadSettings() {
      const res = await getAllSettings();
      setSettings(res.data.settings);
    }
    loadSettings();
  }, []);

  const formatOutput = (output) => {
    if (!output) return ""; 

    const formattedOutput = output.replace(/\$/g, "\n$").trim();
    return formattedOutput;
  };

  return (
    <div className="max-w-4xl mx-auto my-auto mt-20">
      {settings.map(setting => (
        <div key={setting.id} className="flex flex-row items-center mx-4 mb-4 mt-10">
          <div style={{ width: "450px", height: "300px", background: "rgb(63 63 70)", marginRight: "30px", borderRadius: "30px", position: "relative" }}>
            <div style={{ position: "absolute", top: "-30px", left: "10px", color: "#fff", fontSize: "18px" }}>Entrada</div>
            <div style={{ padding: "10px", whiteSpace: "pre-line", overflowWrap: "break-word" }}>{formatOutput(setting.input)}</div>
          </div>
          <div style={{ width: "450px", height: "300px", background: "rgb(63 63 70)", borderRadius: "30px", position: "relative" }}>
            <div style={{ position: "absolute", top: "-30px", left: "10px", color: "#fff", fontSize: "18px" }}>Salida</div>
            <div style={{ padding: "10px", whiteSpace: "pre-line", overflowWrap: "break-word" }}>{formatOutput(setting.output)}</div>
          </div>
        </div>
      ))}
    </div>
  );
}




