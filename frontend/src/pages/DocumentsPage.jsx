import {
  useEffect,
  useState,
} from "react";

import {
  getDocuments,
  uploadDocument,
  deleteDocument,
} from "../api/documentApi";
import "../styles/documents.css";
export default function DocumentsPage() {

  const [documents, setDocuments] =
    useState([]);

  const [file, setFile] =
    useState(null);

  const [uploadProgress,
    setUploadProgress] =
    useState(0);

  const [success,
    setSuccess] =
    useState("");

  const [dragging,
    setDragging] =
    useState(false);

  useEffect(() => {

    loadDocuments();

    const interval =
      setInterval(
        loadDocuments,
        5000
      );

    return () =>
      clearInterval(
        interval
      );

  }, []);

  const loadDocuments =
    async () => {

      try {

        const data =
          await getDocuments();

        setDocuments(data);

      } catch (error) {

        console.error(error);
      }
    };

  const handleUpload =
    async () => {

      if (!file) {

        alert(
          "Please select a file"
        );

        return;
      }

      const allowedTypes = [
        "pdf",
        "docx",
        "txt",
      ];

      const extension =
        file.name
          .split(".")
          .pop()
          .toLowerCase();

      if (
        !allowedTypes.includes(
          extension
        )
      ) {

        alert(
          "Only PDF, DOCX and TXT files are allowed"
        );

        return;
      }

      const maxSize =
        10 * 1024 * 1024;

      if (
        file.size > maxSize
      ) {

        alert(
          "Maximum file size is 10 MB"
        );

        return;
      }

      try {

        setSuccess("");

        await uploadDocument(
          file,
          (percent) => {

            setUploadProgress(
              percent
            );
          }
        );

        setSuccess(
          "Document uploaded successfully"
        );

        setFile(null);

        setUploadProgress(0);

        loadDocuments();

      } catch (error) {

        console.error(error);

        alert(
          "Upload failed"
        );
      }
    };

  const handleDelete =
    async (documentId) => {

      const confirmed =
        window.confirm(
          "Delete document?"
        );

      if (!confirmed) {
        return;
      }

      try {

        await deleteDocument(
          documentId
        );

        loadDocuments();

      } catch (error) {

        console.error(error);
      }
    };

  const getStatusColor =
    (status) => {

      switch (
        status?.toLowerCase()
      ) {

        case "completed":
          return "green";

        case "processing":
          return "orange";

        case "failed":
          return "red";

        default:
          return "gray";
      }
    };

 return (
  <div className="documents-page">

    <h2 className="documents-title">
      Documents
    </h2>

    <div
      className={`drag-area ${
        dragging ? "drag-active" : ""
      }`}
      onDragOver={(e) => {
        e.preventDefault();
        setDragging(true);
      }}
      onDragLeave={() =>
        setDragging(false)
      }
      onDrop={(e) => {
        e.preventDefault();
        setDragging(false);

        const droppedFile =
          e.dataTransfer.files[0];

        if (droppedFile) {
          setFile(droppedFile);
        }
      }}
    >
      Drop file here or select below
    </div>

    <div className="upload-section">

      <label
        htmlFor="file-upload"
        className="file-upload-label"
      >
        📄 Choose Document
      </label>

      <input
        id="file-upload"
        type="file"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
        className="file-upload-input"
      />

      {
        file && (
          <div className="selected-file">
            <span>📎 {file.name}</span>

            <span>
              (
              {(file.size / 1024).toFixed(2)}
              KB)
            </span>
          </div>
        )
      }

      <button
        className="upload-button"
        onClick={handleUpload}
        disabled={!file}
      >
        ⬆ Upload
      </button>

    </div>

    {uploadProgress > 0 &&
      uploadProgress < 100 && (

      <div className="progress-container">

        <div className="progress-bar">

          <div
            className="progress-fill"
            style={{
              width:
                `${uploadProgress}%`,
            }}
          />

        </div>

        <p>
          {uploadProgress}%
        </p>

      </div>
    )}

    {success && (
      <div className="success-message">
        {success}
      </div>
    )}

    <table className="documents-table">

      <thead>

        <tr>
          <th>Filename</th>
          <th>Status</th>
          <th>Action</th>
        </tr>

      </thead>

      <tbody>

        {documents.map((doc) => (

          <tr key={doc.id}>

            <td>
              {doc.filename}
            </td>

            <td>

              <span
                className={`status-badge status-${doc.processing_status?.toLowerCase()}`}
              >
                {doc.processing_status}
              </span>

            </td>

            <td>

              <button
                className="delete-btn"
                onClick={() =>
                  handleDelete(
                    doc.id
                  )
                }
              >
                Delete
              </button>

            </td>

          </tr>

        ))}

      </tbody>

    </table>

  </div>
);
}