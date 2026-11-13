import { useEffect, useState } from "react";
import { unzipSync, strFromU8 } from "fflate";

// The whole game (page, levels, sound, 3D props, artwork) lives in one bundle uploaded to this app.
const BUNDLES = ["__GAME_ZIP_URL__", "__MODELS_ZIP_URL__"];
const TOTAL_BYTES = 11754074;

const MIME = {
  js: "text/javascript", glb: "model/gltf-binary", png: "image/png", webp: "image/webp",
  gif: "image/gif", jpg: "image/jpeg", mp3: "audio/mpeg",
};

export default function Home() {
  const [src, setSrc] = useState(null);
  const [pct, setPct] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    const urls = [];
    let dead = false;
    (async () => {
      try {
        let got = 0;
        const parts = await Promise.all(BUNDLES.map(async (url) => {
          const res = await fetch(url);
          if (!res.ok) throw new Error("Bundle HTTP " + res.status);
          const reader = res.body.getReader();
          const chunks = [];
          let size = 0;
          for (;;) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            size += value.length;
            got += value.length;
            if (!dead) setPct(Math.min(99, Math.round((got / TOTAL_BYTES) * 100)));
          }
          const buf = new Uint8Array(size);
          let o = 0;
          for (const c of chunks) { buf.set(c, o); o += c.length; }
          return unzipSync(buf);
        }));
        const files = Object.assign({}, ...parts);
        const map = {};
        for (const [name, data] of Object.entries(files)) {
          if (name.endsWith("/") || name === "index.html") continue;
          const url = URL.createObjectURL(new Blob([data], { type: MIME[name.split(".").pop()] || "application/octet-stream" }));
          urls.push(url);
          map[name] = url;
        }
        let html = strFromU8(files["index.html"]);
        html = html
          .replace(/assets\/[\w\-./]+\.(?:png|webp|gif|glb|mp3|jpg)/g, (m) => map[m] || m)
          .replace('src="audio.js"', 'src="' + map["audio.js"] + '"')
          .replace("<head>", "<head><script>window.__F=" + JSON.stringify(map) + "</" + "script>");
        const page = URL.createObjectURL(new Blob([html], { type: "text/html" }));
        urls.push(page);
        if (!dead) setSrc(page);
      } catch (e) {
        if (!dead) setError(String((e && e.message) || e));
      }
    })();
    return () => { dead = true; urls.forEach((u) => URL.revokeObjectURL(u)); };
  }, []);

  const full = { position: "fixed", inset: 0, width: "100vw", height: "100vh", border: 0, margin: 0, background: "#0b0907" };

  if (src) {
    return <iframe title="Gaston Grandiose's Shadow Dept." src={src} style={full} allow="autoplay; fullscreen" />;
  }
  return (
    <div style={{ ...full, display: "grid", placeItems: "center", color: "#f3e8d2", fontFamily: "Georgia, serif", textAlign: "center" }}>
      <div>
        <div style={{ fontSize: 28, letterSpacing: 1 }}>Gaston Grandiose&rsquo;s Shadow Dept.</div>
        <div style={{ marginTop: 12, fontSize: 16, opacity: 0.8 }}>
          {error ? "The lamp would not light: " + error : "Warming up the lamp… " + pct + "%"}
        </div>
        {!error && (
          <div style={{ margin: "18px auto 0", width: 260, height: 6, background: "#3a2a18", borderRadius: 3, overflow: "hidden" }}>
            <div style={{ width: pct + "%", height: "100%", background: "#e0a43a", transition: "width .2s" }} />
          </div>
        )}
      </div>
    </div>
  );
}
