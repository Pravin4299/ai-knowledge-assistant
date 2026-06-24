import authApi from "./authApi";

export const getSessions = async () => {
  const response = await authApi.get(
    "/chat/sessions"
  );

  return response.data;
};

export const createSession = async (
  title
) => {

  const response =
    await authApi.post(
      "/chat/sessions",
      {
        title,
      }
    );

  return response.data;
};