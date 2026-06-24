import axios from "axios";

const API_URL ="http://localhost:8000";

export const searchDocuments =
  async (query) => {

    const token =
      localStorage.getItem(
        "access_token"
      );

    const response =
      await axios.get(
        `${API_URL}/documents/search`,
        {
          params: {
            query
          },
          headers: {
            Authorization:
              `Bearer ${token}`
          }
        }
      );

    return response.data;
  };