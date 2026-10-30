import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

const link = ({ isActive }) =>
  `rounded-lg px-3 py-1.5 text-sm font-medium ${isActive ? "bg-indigo-50 text-indigo-700" : "text-slate-600 hover:bg-slate-100"}`;

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2">
          <span className="mr-4 text-lg font-bold text-indigo-600">JobTracker</span>
          <NavLink to="/" end className={link}>Dashboard</NavLink>
          <NavLink to="/applications" className={link}>Applications</NavLink>
          <NavLink to="/analyzer" className={link}>Resume Analyzer</NavLink>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <span className="hidden text-slate-500 sm:inline">{user.email}</span>
          <button className="btn-ghost" onClick={logout}>Logout</button>
        </div>
      </div>
    </header>
  );
}
