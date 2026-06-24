import authApi from "./authApi";

export const sendMessage = async (payload) => {
  const response = await authApi.post(
    "/chat/message",
    payload
  );

  return response.data;
};

export const getMessages = async (
  sessionId
) => {

  const response = await authApi.get(
    `/messages/${sessionId}`
  );

  return response.data;
};


export const streamMessage = async ({
  session_id,
  question,
  is_rag,
  onToken,
  onDone,
}) => {

  const accessToken =
    localStorage.getItem(
      "access_token"
    );

  const response =
    await fetch(
      "http://localhost:8000/chat/message/stream",
      {
        method: "POST",
        headers: {
          "Content-Type":
            "application/json",
          Authorization:
            `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          session_id,
          question,
          is_rag,
        }),
      }
    );

  if (!response.ok) {

    throw new Error(
      `HTTP Error: ${response.status}`
    );
  }

  const reader =
    response.body.getReader();

  const decoder =
    new TextDecoder();

  let buffer = "";

  while (true) {

    const {
      done,
      value,
    } = await reader.read();

    if (done) {

      break;
    }

    buffer += decoder.decode(
      value,
      {
        stream: true,
      }
    );

    const lines =
      buffer.split("\n");

    buffer =
      lines.pop() || "";

    for (const line of lines) {

      if (
        !line.startsWith(
          "data:"
        )
      ) {

        continue;
      }

      // IMPORTANT:
      // Don't use trim()
      const data =
        line.substring(5);

      try {

        const parsed =
          JSON.parse(data);

        if (
          parsed.done === true
        ) {

          onDone?.(
            parsed.sources || []
          );

          continue;
        }

        if (
          parsed.token
        ) {

          onToken?.(
            parsed.token
          );

          continue;
        }

      } catch {

        // Fallback for plain text tokens

        onToken?.(
          data
        );
      }
    }
  }
};