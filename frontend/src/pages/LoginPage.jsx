import { useState } from "react";
import { useNavigate } from "react-router-dom";
import authApi from "../api/authApi";
import { useAuth } from "../context/AuthContext";
import "../styles/auth.css";

export default function LoginPage() {

  const navigate = useNavigate();

  const { login } = useAuth();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        try {

            const response =
            await authApi.post(
                "/auth/login",
                {
                email,
                password,
                }
            );

            login(
            response.data.access_token
            );

            navigate("/chat");

        } catch (error) {

            console.error(error);

            alert("Login Failed");
        }
    };
    
  return (

    <div className="auth-container">

      <div className="auth-card">

        <h2 className="auth-title">
          Login
        </h2>

        <form onSubmit={handleSubmit}>

          <input
            className="auth-input"
            placeholder="Email"
            value={email}
            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }
          />

          <input
            className="auth-input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }
          />

          <button
            className="auth-button"
            type="submit"
          >
            Login
          </button>

        </form>

        <div className="auth-footer">

          Don't have an account?

          <span
            onClick={() =>
              navigate("/register")
            }
          >
            Register
          </span>

        </div>

      </div>

    </div>
  );

}