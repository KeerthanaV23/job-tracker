import { useCallback, useEffect, useState } from "react";
import api from "../api/client";
import ApplicationForm from "../components/ApplicationForm.jsx";
import KanbanBoard from "../components/KanbanBoard.jsx";

export default function Applications() {
  const [apps, setApps] = useState([]);
  const [search, setSearch] = useState("");
  const [editing, setEditing] = useState(null); // null | "new" | application
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    const { data } = await api.get("/applications/", { params: { search, page_size: 200 } });
    setApps(data.results);
    setLoading(false);
  }, [search]);

  useEffect(() => {
    const t = setTimeout(load, 250); // debounce search
    return () => clearTimeout(t);
  }, [load]);

  const move = async (app, status) => {
    setApps((list) => list.map((a) => (a.id === app.id ? { ...a, status } : a))); // optimistic
    try {
      await api.patch(`/applications/${app.id}/`, { status });
    } catch {
      load();
    }
  };

  const save = async (payload) => {
    if (editing === "new") await api.post("/applications/", payload);
    else await api.patch(`/applications/${editing.id}/`, payload);
    setEditing(null);
    load();
  };

  const remove = async () => {
    if (!window.confirm("Delete this application?")) return;
    await api.delete(`/applications/${editing.id}/`);
    setEditing(null);
    load();
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h1 className="text-2xl font-semibold">Applications</h1>
        <div className="flex gap-2">
          <input className="input w-56" placeholder="Search company / role" value={search} onChange={(e) => setSearch(e.target.value)} />
          <button className="btn" onClick={() => setEditing("new")}>+ Add</button>
        </div>
      </div>
      <p className="text-sm text-slate-500">Drag cards between columns to update status. Click a card to edit.</p>
      {loading ? <p className="text-slate-500">Loading...</p>
        : apps.length === 0 && !search ? <div className="card text-center text-slate-500">No applications yet. Click "+ Add" to start tracking.</div>
        : <KanbanBoard applications={apps} onMove={move} onEdit={setEditing} />}
      {editing && (
        <ApplicationForm
          initial={editing === "new" ? null : editing}
          onSave={save}
          onCancel={() => setEditing(null)}
          onDelete={editing === "new" ? null : remove}
        />
      )}
    </div>
  );
}
