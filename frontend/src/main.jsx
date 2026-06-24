
import ReactDOM from "react-dom/client";

import App from "./App";
// main.jsx
import "./styles/app.css";
import {
  AuthProvider,
} from "./context/AuthContext";

ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <AuthProvider>
    <App />
  </AuthProvider>
);