import authApi from "./authApi";

export const getDocuments = async () => {

  const response =
    await authApi.get(
      "/documents"
    );

  return response.data;
};


export const uploadDocument = async (
  file,
  onProgress
) => {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const response =
    await authApi.post(
      "/documents/upload",
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },

        onUploadProgress:
          (progressEvent) => {

            const percent =
              Math.round(
                (
                  progressEvent.loaded /
                  progressEvent.total
                ) * 100
              );

            onProgress?.(
              percent
            );
          },
      }
    );

  return response.data;
};

export const deleteDocument =
  async (documentId) => {

    const response =
      await authApi.delete(
        `/documents/${documentId}`
      );

    return response.data;
};