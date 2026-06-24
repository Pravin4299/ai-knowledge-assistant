import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import authApi from "../api/authApi";
import "../styles/auth.css";

export default function RegisterPage() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await authApi.post(
        "/auth/register",
        {
          username,
          email,
          password,
        }
      );

      alert("Registration successful!");

      navigate("/login");
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
        "Registration failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (

    <div className="auth-container">

      <div className="auth-card">

        <h2 className="auth-title">
          Create Account
        </h2>

        <form onSubmit={handleSubmit}>

          <input
            className="auth-input"
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }
            required
          />

          <input
            className="auth-input"
            type="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
            required
          />

          <input
            className="auth-input"
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
            required
          />

          <button
            className="auth-button"
            type="submit"
            disabled={loading}
          >
            {
              loading
                ? "Registering..."
                : "Register"
            }
          </button>

        </form>

        <div className="auth-footer">

          Already have an account?

          <span
            onClick={() =>
              navigate("/login")
            }
          >
            Login
          </span>

        </div>

      </div>

    </div>
  );
}

