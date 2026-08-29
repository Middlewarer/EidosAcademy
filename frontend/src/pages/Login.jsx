import { useEffect, useState } from "react";
import { apiRequest } from "../components/api/apiRequest";
import { useAuth } from "../components/context/AuthContext";
import { useNavigate } from "react-router-dom";

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

            alert("Успешный вход!")
            navigator("/courses/1")
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
    background: 'linear-gradient(135deg, #FFF9E6 0%, #FFE566 100%)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  card: {
    background: '#FFFFFF',
    borderRadius: '16px',
    padding: '40px 36px',
    width: '100%',
    maxWidth: '400px',
    boxShadow: '0 20px 40px rgba(255, 193, 7, 0.25)',
    border: '1px solid #FFE082',
  },
  title: {
    margin: '0 0 8px',
    fontSize: '28px',
    fontWeight: '700',
    color: '#F57F17',
    textAlign: 'center',
  },
  subtitle: {
    margin: '0 0 32px',
    fontSize: '15px',
    color: '#F9A825',
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
    color: '#F57F17',
  },
  input: {
    padding: '12px 14px',
    fontSize: '15px',
    borderRadius: '10px',
    border: '2px solid #FFE082',
    outline: 'none',
    transition: 'border-color 0.2s',
    background: '#FFFDE7',
  },
  button: {
    marginTop: '8px',
    padding: '14px',
    fontSize: '16px',
    fontWeight: '600',
    color: '#FFFFFF',
    background: 'linear-gradient(135deg, #FFCA28 0%, #FFA000 100%)',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    boxShadow: '0 4px 12px rgba(255, 160, 0, 0.4)',
  },
};

export default Login;