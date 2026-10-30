import { createContext, useContext, useEffect, useState } from "react";
import api, { clearTokens, saveTokens } from "../api/client";

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!localStorage.getItem("tokens")) return setLoading(false);
    api.get("/auth/me/").then((r) => setUser(r.data)).catch(clearTokens).finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    const { data } = await api.post("/auth/login/", { email, password });
    saveTokens(data);
    setUser((await api.get("/auth/me/")).data);
  };

  const register = async (form) => {
    await api.post("/auth/register/", form);
    await login(form.email, form.password);
  };

  const logout = () => {
    clearTokens();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
