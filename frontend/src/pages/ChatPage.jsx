import Sidebar from "../components/SideBar";
import ChatWindow from "../components/ChatWindow";
import { useEffect, useState } from "react";

export default function ChatPage({sessionId}) {
    const [selectedSession,setSelectedSession] = useState(null);
  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
      }}
    >
      {/* <Sidebar
        selectedSession={
            selectedSession
        }
        setSelectedSession={
            setSelectedSession
        }
        /> */}

        <ChatWindow
        sessionId={
            sessionId
        }
        />
    </div>
  );
}