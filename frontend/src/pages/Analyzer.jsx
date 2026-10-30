import { useEffect, useState } from "react";
import api, { errorMessage } from "../api/client";

const scoreColor = (s) => (s >= 70 ? "text-emerald-600" : s >= 40 ? "text-amber-600" : "text-rose-600");

export default function Analyzer() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [applicationId, setApplicationId] = useState("");
  const [apps, setApps] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => { api.get("/applications/", { params: { page_size: 200 } }).then((r) => setApps(r.data.results)); }, []);

  const pickApplication = (id) => {
    setApplicationId(id);
    const app = apps.find((a) => String(a.id) === id);
    if (app?.job_description) setJd(app.job_description);
  };

  const submit = async (e) => {
    e.preventDefault();
    if (!file) return setError("Please choose a PDF resume.");
    setBusy(true); setError(""); setResult(null);
    const body = new FormData();
    body.append("file", file);
    body.append("job_description", jd);
    if (applicationId) body.append("application", applicationId);
    try {
      setResult((await api.post("/resumes/analyze/", body)).data);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <form onSubmit={submit} className="card space-y-4">
        <h1 className="text-xl font-semibold">Resume Analyzer</h1>
        <div>
          <label className="mb-1 block text-sm font-medium">Resume (PDF, max 5 MB)</label>
          <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} className="text-sm" />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Link to application (optional)</label>
          <select className="input" value={applicationId} onChange={(e) => pickApplication(e.target.value)}>
            <option value="">None</option>
            {apps.map((a) => <option key={a.id} value={a.id}>{a.role} - {a.company}</option>)}
          </select>
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">Job description</label>
          <textarea className="input" rows={10} required value={jd} onChange={(e) => setJd(e.target.value)} placeholder="Paste the job description here" />
        </div>
        {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}
        <button className="btn" disabled={busy}>{busy ? "Analyzing..." : "Analyze match"}</button>
      </form>

      <div className="card">
        {!result ? (
          <p className="text-slate-500">Your match score and missing keywords will appear here.</p>
        ) : (
          <div className="space-y-5">
            <div>
              <p className="text-sm text-slate-500">Match score</p>
              <p className={`text-6xl font-bold ${scoreColor(result.score)}`}>{result.score}%</p>
            </div>
            <div>
              <h3 className="mb-2 font-medium text-rose-700">Missing keywords ({result.missing_keywords.length})</h3>
              <div className="flex flex-wrap gap-2">
                {result.missing_keywords.map((k) => <span key={k} className="rounded-full bg-rose-50 px-3 py-1 text-sm text-rose-700">{k}</span>)}
              </div>
              <p className="mt-2 text-xs text-slate-500">Add these to your resume only if you genuinely have the skill.</p>
            </div>
            <div>
              <h3 className="mb-2 font-medium text-emerald-700">Matched keywords ({result.matched_keywords.length})</h3>
              <div className="flex flex-wrap gap-2">
                {result.matched_keywords.map((k) => <span key={k} className="rounded-full bg-emerald-50 px-3 py-1 text-sm text-emerald-700">{k}</span>)}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
