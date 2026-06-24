import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  getMessages,
  streamMessage,
} from "../api/chatApi";
import "../styles/chat.css";
import MessageBubble from "./MessageBubble";

export default function ChatWindow({
  sessionId,
}) {

  
  const [messages, setMessages] =
    useState([]);

  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [isRag, setIsRag] =
    useState(true);

  const bottomRef = useRef(null);

  useEffect(() => {

    if (!sessionId) {

      setMessages([]);

      return;
    }

    loadMessages();

  }, [sessionId]);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);

  const loadMessages = async () => {

    try {

      const data =
        await getMessages(
          sessionId
        );

      setMessages(data);

    } catch (error) {

      console.error(error);
    }
  };

  const handleSend = async () => {

  if (!question.trim()) {
    return;
  }

  if (!sessionId) {

    alert(
      "Please select a chat session"
    );

    return;
  }

  const currentQuestion =
    question;

  setQuestion("");

  setLoading(true);

  setMessages((prev) => [
    ...prev,
    {
      role: "user",
      content:
        currentQuestion,
    },
    {
      role: "assistant",
      content: "",
      loading: true,
      sources: [],
    },
  ]);

  try {

    await streamMessage({

      session_id:
        sessionId,

      question:
        currentQuestion,

      is_rag:
        isRag,

      onToken: (token) => {

        setMessages((prev) => {

          const updated =
            [...prev];

          const lastIndex =
            updated.length - 1;

          if (lastIndex < 0) {
            return prev;
          }

          const currentContent =
            updated[lastIndex]
              .content || "";

          updated[lastIndex] = {

            ...updated[lastIndex],

            content:
              currentContent +
              token,

            loading:
              false,
          };

          return updated;
        });
      },

      onDone: (sources) => {

        setMessages((prev) => {

          const updated =
            [...prev];

          const lastIndex =
            updated.length - 1;

          if (lastIndex < 0) {
            return prev;
          }

          updated[lastIndex] = {

            ...updated[lastIndex],

            loading:
              false,

            sources:
              sources || [],
          };

          return updated;
        });

        setLoading(false);
      },
    });

  } catch (error) {

    console.error(error);

    setMessages((prev) => {

      const updated =
        [...prev];

      const lastIndex =
        updated.length - 1;

      if (lastIndex >= 0) {

        updated[lastIndex] = {

          ...updated[lastIndex],

          content:
            "Something went wrong.",

          loading:
            false,
        };
      }

      return updated;
    });

    setLoading(false);
  }
};

 return (
  <div className="chat-container">

    <div className="messages-container">

      {messages.map(
        (message, index) => (
          <MessageBubble
            key={index}
            message={message}
          />
        )
      )}

      <div ref={bottomRef} />

    </div>

    <div className="chat-input-section">

      <div className="rag-toggle">

        <label>

          <input
            type="checkbox"
            checked={isRag}
            onChange={(e) =>
              setIsRag(
                e.target.checked
              )
            }
          />

          {" "}
          Use RAG

        </label>

      </div>

      <div className="input-row">

        <input
          className="chat-input"
          value={question}
          onChange={(e) =>
            setQuestion(
              e.target.value
            )
          }
          placeholder="Ask something..."
          disabled={loading}
          onKeyDown={(e) => {

            if (
              e.key === "Enter"
            ) {

              handleSend();
            }
          }}
        />

        <button
          className="send-button"
          onClick={handleSend}
          disabled={
            loading ||
            !question.trim() ||
            !sessionId
          }
        >
          {
            loading
              ? "Thinking..."
              : "Send"
          }
        </button>

      </div>

    </div>

  </div>
);
}