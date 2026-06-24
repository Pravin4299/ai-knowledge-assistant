import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  getSessions,
  createSession,
} from "../api/sessionApi";

import "../styles/sidebar.css";

export default function Sidebar({
  selectedSession,
  setSelectedSession,
}) {

  const [sessions, setSessions] = useState([]);

  const navigate = useNavigate();

  // useEffect(() => {

  //   window.addEventListener(
  //     "session-updated",
  //     loadSessions
  //   );

  //   return () => {

  //     window.removeEventListener(
  //       "session-updated",
  //       loadSessions
  //     );
  //   };

  // }, []);
  useEffect(() => {

  loadSessions();

  }, []);

  const loadSessions =
    async () => {

      try {

        const data =
          await getSessions();

        setSessions(data);

      } catch (error) {

        console.error(error);
      }
    };

  const handleNewChat =
    async () => {

      try {

        const session =
          await createSession(
            "New Chat"
          );

        setSessions(
          (prev) => [
            session,
            ...prev,
          ]
        );

        setSelectedSession(
          session.id
        );

        navigate("/chat");

      } catch (error) {

        console.error(error);
      }
    };

  const handleSessionClick =
    (sessionId) => {

      setSelectedSession(
        sessionId
      );

      navigate("/chat");
    };

  return (

    <div className="sidebar">

      <div className="sidebar-header">

        <h2 className="sidebar-title">
          AI Assistant
        </h2>

      </div>

      <div className="sidebar-menu">

        <button
          className="sidebar-button"
          onClick={() =>
            navigate("/chat")
          }
        >
          💬 Chat
        </button>

        <button
          className="sidebar-button"
          onClick={() =>
            navigate("/documents")
          }
        >
          📄 Documents
        </button>

        <button
          className="sidebar-button"
          onClick={() =>
            navigate("/search")
          }
        >
          🔍 Search
        </button>

        <button
          className="sidebar-button"
          onClick={handleNewChat}
        >
          ➕ New Chat
        </button>

      </div>

      <div className="sessions-container">

        {sessions.map(
          (session) => (

            <div
              key={session.id}
              className={`session-item ${
                selectedSession === session.id
                  ? "active-session"
                  : ""
              }`}
              onClick={() =>
                handleSessionClick(
                  session.id
                )
              }
            >
              {session.title}
            </div>

          )
        )}

      </div>

    </div>
  );
}