import { useState } from "react";
import { errorMessage } from "../api/client";

export const STATUSES = ["wishlist", "applied", "interview", "offer", "rejected"];

const EMPTY = {
  company: "", role: "", location: "", job_url: "", salary: "", notes: "",
  job_description: "", status: "applied", interview_at: "",
};

const toLocalInput = (iso) => (iso ? new Date(iso).toISOString().slice(0, 16) : "");

export default function ApplicationForm({ initial, onSave, onCancel, onDelete }) {
  const [form, setForm] = useState(initial ? { ...EMPTY, ...initial, interview_at: toLocalInput(initial.interview_at) } : EMPTY);
  const [error, setError] = useState("");
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await onSave({ ...form, interview_at: form.interview_at ? new Date(form.interview_at).toISOString() : null });
    } catch (err) {
      setError(errorMessage(err));
    }
  };

  return (
    <div className="fixed inset-0 z-10 flex items-center justify-center bg-black/40 p-4">
      <form onSubmit={submit} className="card max-h-[90vh] w-full max-w-lg space-y-3 overflow-y-auto">
        <h2 className="text-lg font-semibold">{initial ? "Edit application" : "Add application"}</h2>
        {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}
        <div className="grid grid-cols-2 gap-3">
          <input className="input" placeholder="Company *" required value={form.company} onChange={set("company")} />
          <input className="input" placeholder="Role *" required value={form.role} onChange={set("role")} />
          <input className="input" placeholder="Location" value={form.location} onChange={set("location")} />
          <input className="input" placeholder="Salary" value={form.salary} onChange={set("salary")} />
          <select className="input" value={form.status} onChange={set("status")}>
            {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          <input className="input" type="datetime-local" title="Interview date/time" value={form.interview_at} onChange={set("interview_at")} />
        </div>
        <input className="input" placeholder="Job URL" value={form.job_url} onChange={set("job_url")} />
        <textarea className="input" rows={3} placeholder="Job description (used by Resume Analyzer)" value={form.job_description} onChange={set("job_description")} />
        <textarea className="input" rows={2} placeholder="Notes" value={form.notes} onChange={set("notes")} />
        <div className="flex items-center justify-between pt-2">
          {onDelete ? <button type="button" className="text-sm text-red-600" onClick={onDelete}>Delete</button> : <span />}
          <div className="flex gap-2">
            <button type="button" className="btn-ghost" onClick={onCancel}>Cancel</button>
            <button className="btn">Save</button>
          </div>
        </div>
      </form>
    </div>
  );
}
