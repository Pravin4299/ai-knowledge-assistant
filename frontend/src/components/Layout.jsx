import Sidebar from "./SideBar";

export default function Layout({
  children,
  selectedSession,
  setSelectedSession,
}) {
  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
      }}
    >
      <Sidebar
        selectedSession={selectedSession}
        setSelectedSession={
          setSelectedSession
        }
      />

      <div
        style={{
          flex: 1,
          overflow: "auto",
        }}
      >
        {children}
      </div>
    </div>
  );
}