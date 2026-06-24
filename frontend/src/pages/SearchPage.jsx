import {
  useState
} from "react";

import {
  searchDocuments
} from "../api/searchApi";

import "../styles/search.css";

export default function SearchPage() {

  const [query, setQuery] =
    useState("");

  const [results, setResults] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const handleSearch =
    async () => {

      if (!query.trim()) {
        return;
      }

      setLoading(true);

      try {

        const data =
          await searchDocuments(
            query
          );

        setResults(data);

      } catch (error) {

        console.error(error);

      } finally {

        setLoading(false);
      }
    };

  return (

    <div className="search-page">

      <h2>
        Search Documents
      </h2>

      <div className="search-bar">

        <input
          className="search-input"
          value={query}
          onChange={(e) =>
            setQuery(
              e.target.value
            )
          }
          placeholder="Search documents..."
        />
        <button
            className="search-button"
            onClick={handleSearch}
            disabled={loading}
            >
            {loading ? "Searching..." : "🔍 Search"}
            </button>
      </div>

      {
        loading && (
          <p>
            Searching...
          </p>
        )
      }

      {
        results.map(
          (
            result,
            index
          ) => (

            <div
              key={index}
              className="search-card"
            >

              <div className="search-header">

                📄
                {" "}
                {
                  result.filename
                }

              </div>

              <div className="search-chunk">

                Chunk:
                {" "}
                {
                  result.chunk_index
                }

              </div>

              <div className="search-content">

                {
                  result.chunk_text
                }

              </div>

              <div className="search-score">

                Score:
                {" "}
                {
                  Number(
                    result.distance
                  ).toFixed(3)
                }

              </div>

            </div>
          )
        )
      }

    </div>
  );
}