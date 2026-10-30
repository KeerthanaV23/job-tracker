import { useState } from "react";
import { STATUSES } from "./ApplicationForm.jsx";

const COLORS = {
  wishlist: "bg-slate-100", applied: "bg-blue-50", interview: "bg-amber-50",
  offer: "bg-emerald-50", rejected: "bg-rose-50",
};

export default function KanbanBoard({ applications, onMove, onEdit }) {
  const [overCol, setOverCol] = useState(null);

  const drop = (e, status) => {
    e.preventDefault();
    setOverCol(null);
    const id = Number(e.dataTransfer.getData("text/plain"));
    const app = applications.find((a) => a.id === id);
    if (app && app.status !== status) onMove(app, status);
  };

  return (
    <div className="grid gap-4 md:grid-cols-5">
      {STATUSES.map((status) => {
        const items = applications.filter((a) => a.status === status);
        return (
          <div
            key={status}
            onDragOver={(e) => { e.preventDefault(); setOverCol(status); }}
            onDragLeave={() => setOverCol(null)}
            onDrop={(e) => drop(e, status)}
            className={`min-h-[200px] rounded-xl p-3 ${COLORS[status]} ${overCol === status ? "ring-2 ring-indigo-400" : ""}`}
          >
            <h3 className="mb-3 flex justify-between text-sm font-semibold capitalize">
              {status} <span className="text-slate-500">{items.length}</span>
            </h3>
            <div className="space-y-2">
              {items.map((a) => (
                <div
                  key={a.id}
                  draggable
                  onDragStart={(e) => e.dataTransfer.setData("text/plain", String(a.id))}
                  onClick={() => onEdit(a)}
                  className="cursor-grab rounded-lg border border-slate-200 bg-white p-3 text-sm shadow-sm hover:shadow"
                >
                  <p className="font-medium">{a.role}</p>
                  <p className="text-slate-500">{a.company}</p>
                  {a.interview_at && a.status === "interview" && (
                    <p className="mt-1 text-xs text-amber-700">
                      Interview: {new Date(a.interview_at).toLocaleString()}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
