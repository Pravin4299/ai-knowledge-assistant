import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import { useState } from "react";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ChatPage from "./pages/ChatPage";
import DocumentsPage from "./pages/DocumentsPage";
import SearchPage from "./pages/SearchPage";

import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";

function App() {

  const [
    selectedSession,
    setSelectedSession
  ] = useState(null);

  return (

    <BrowserRouter>

      <Routes>

        {/* Public Routes */}

        <Route
          path="/"
          element={<LoginPage />}
        />

        <Route
          path="/login"
          element={<LoginPage />}
        />

        <Route
          path="/register"
          element={<RegisterPage />}
        />

        {/* Protected Routes */}

        <Route
          path="/chat"
          element={
            <ProtectedRoute>

              <Layout
                selectedSession={
                  selectedSession
                }
                setSelectedSession={
                  setSelectedSession
                }
              >

                <ChatPage
                  sessionId={
                    selectedSession
                  }
                />

              </Layout>

            </ProtectedRoute>
          }
        />

        <Route
          path="/documents"
          element={
            <ProtectedRoute>

              <Layout
                selectedSession={
                  selectedSession
                }
                setSelectedSession={
                  setSelectedSession
                }
              >

                <DocumentsPage />

              </Layout>

            </ProtectedRoute>
          }
        />

        <Route
          path="/search"
          element={
            <ProtectedRoute>

              <Layout
                selectedSession={
                  selectedSession
                }
                setSelectedSession={
                  setSelectedSession
                }
              >

                <SearchPage />

              </Layout>

            </ProtectedRoute>
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;