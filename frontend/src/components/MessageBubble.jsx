import ReactMarkdown from "react-markdown";
import "../styles/chat.css";
import { useState } from "react";
import "../styles/messages.css";
export default function MessageBubble({
  message,
}) {
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);
  const isUser =
    message.role === "user";

  const handleCopy = async () => {

    try {

      await navigator.clipboard.writeText(
        message.content
      );

      setCopied(true);

      setTimeout(() => {

        setCopied(false);

      }, 2000);

    } catch (error) {

      console.error(error);
    }
  };
  if (message.loading) {

    return (

      <div className="message-row message-ai">

        <div className="message-bubble message-bubble-ai">

          <div className="typing-loader">

            <span></span>
            <span></span>
            <span></span>

          </div>

        </div>

      </div>
    );
  }
  return (

    <div
      className={`message-row ${
        isUser
          ? "message-user"
          : "message-ai"
      }`}
    >

      <div
        className={`message-bubble ${
          isUser
            ? "message-bubble-user"
            : "message-bubble-ai"
        }`}
      >

        <div className="markdown-content">
  <ReactMarkdown>
    {message.content}
  </ReactMarkdown>
</div>

        {
          message.sources &&
          message.sources.length > 0 && (

            <div className="sources">

              <button
                className="sources-toggle"
                onClick={() =>
                  setShowSources(
                    !showSources
                  )
                }
              >

                📚 Sources (
                {message.sources.length}
                )

                {" "}

                {
                  showSources
                    ? "▲"
                    : "▼"
                }

              </button>

              {
                showSources && (

                  <div
                    className="sources-list"
                  >

                    {
                      message.sources.map(
                        (
                          source,
                          index
                        ) => (

                          <div
                            key={index}
                            className="source-card"
                          >

                            <div
                              className="source-file"
                            >
                              📄
                              {" "}
                              {
                                source.filename
                              }
                            </div>

                            <div
                              className="source-chunk"
                            >
                              Chunk
                              {" "}
                              {
                                source.chunk_index
                              }
                            </div>

                          </div>
                        )
                      )
                    }

                  </div>
                )
              }

            </div>
          )
        }
        {!isUser && (

          <div
            className="message-actions"
          >

            <button
            className="copy-btn"
            onClick={handleCopy}
          >
            {copied
              ? "✓ Copied"
              : "📋 Copy"}
          </button>

          </div>

        )}

      </div>

    </div>
  );
}