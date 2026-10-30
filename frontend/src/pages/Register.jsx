import { useState } from "react";
import { Link } from "react-router-dom";
import { errorMessage } from "../api/client";
import { useAuth } from "../context/AuthContext.jsx";

export default function Register() {
  const { register } = useAuth();
  const [form, setForm] = useState({ first_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await register(form);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="card mx-auto mt-16 max-w-sm space-y-4">
      <h1 className="text-xl font-semibold">Create your account</h1>
      {error && <p className="rounded bg-red-50 p-2 text-sm text-red-700">{error}</p>}
      <input className="input" placeholder="First name" value={form.first_name} onChange={set("first_name")} />
      <input className="input" type="email" placeholder="Email" required value={form.email} onChange={set("email")} />
      <input className="input" type="password" placeholder="Password (min 8 chars)" required minLength={8}
        value={form.password} onChange={set("password")} />
      <button className="btn w-full" disabled={busy}>{busy ? "Creating..." : "Sign up"}</button>
      <p className="text-center text-sm text-slate-500">
        Already registered? <Link className="text-indigo-600" to="/login">Login</Link>
      </p>
    </form>
  );
}
