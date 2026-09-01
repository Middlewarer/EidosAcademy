import { useEffect, useState } from "react";
import { apiRequest } from "../components/api/apiRequest";
import { useAuth } from "../components/context/AuthContext";
import { Link, useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast"

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { user } = useAuth();
    const navigator = useNavigate();
    const { login } = useAuth();
    async function handleSubmit(e) {
        e.preventDefault();
        try {
            const response = await fetch("http://127.0.0.1:8000/api/token/", {
                method: "POST",
                headers: { "Content-Type": "application/json",},
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });

            const data = await response.json()
            console.log(`Ответ сервера: ${data}`)

        if (data.access && data.refresh) {

            const meResponse = await apiRequest("/api/me/")
            const userData = await meResponse.json()

            login(data.access, data.refresh, userData);

            toast.success('Вход выполнен!');
            navigator("/courses/1");
        }
            else {
                alert("Ошибка входа")
            }
        }

        catch (error) {
                console.error('Ошибка запроса:', error);
                alert('Не удалось выполнить запрос');
        }
    }

    useEffect(() => {
        if (user) {
            return navigator("/courses")
        }
    }, [])


    return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Вход</h1>
        <p style={styles.subtitle}>Войдите в свой аккаунт</p>

        <form style={styles.form} onSubmit={handleSubmit}>
          <div style={styles.field}>
            <label style={styles.label}>Username</label>
            <input
              type="username"
              placeholder="username"
              style={styles.input}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Пароль</label>
            <input
              type="password"
              placeholder="••••••••"
              style={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" style={styles.button}>
            Войти
          </button>
        </form>

        <p style={styles.registerText}>
          Нет аккаунта? <Link to="/register" style={styles.registerLink}>Зарегистрироваться</Link>
        </p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'radial-gradient(circle at 75% 20%, #eef1ff, transparent 35%), #f7f8fb',
    fontFamily: 'Manrope, sans-serif',
  },
  card: {
    background: '#FFFFFF',
    borderRadius: '24px',
    padding: '46px 40px',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 24px 65px rgba(34, 46, 80, .12)',
    border: '1px solid #e3e7ef',
  },
  title: {
    margin: '0 0 8px',
    fontSize: '28px',
    fontWeight: '700',
    color: '#172033',
    textAlign: 'center',
  },
  subtitle: {
    margin: '0 0 32px',
    fontSize: '15px',
    color: '#6d7688',
    textAlign: 'center',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  label: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#172033',
  },
  input: {
    padding: '12px 14px',
    fontSize: '15px',
    borderRadius: '16px',
    border: '1px solid #e3e7ef',
    outline: 'none',
    transition: 'border-color 0.2s',
    background: '#f7f8fb',
  },
  button: {
    marginTop: '8px',
    padding: '14px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#FFFFFF',
    background: '#4f6df5',
    border: 'none',
    borderRadius: '13px',
    cursor: 'pointer',
    boxShadow: '0 12px 30px rgba(79,109,245,.22)',
  },
  registerText: {
    margin: '24px 0 0',
    paddingTop: '20px',
    borderTop: '1px solid #e3e7ef',
    color: '#6d7688',
    fontSize: '14px',
    textAlign: 'center',
  },
  registerLink: {
    color: '#4f6df5',
    fontWeight: '700',
    textDecoration: 'none',
  },
};

export default Login;
