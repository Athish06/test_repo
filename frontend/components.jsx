import React, { useState, useEffect } from 'react';

// [Easy 10] Frontend Hardcoded Secret
// Exposing AWS keys or private API keys in the client bundle.
const AWS_PRIVATE_KEY = "AKIAIOSFODNN7EXAMPLE_PRIVATE_KEY";

export function UserProfile({ userData }) {
  const [profile, setProfile] = useState(null);
  
  useEffect(() => {
    // [Medium 8] Improper LocalStorage Usage
    // Storing raw PII or Auth Tokens in LocalStorage
    localStorage.setItem("user_session", JSON.stringify({
      token: "raw_jwt_token_here",
      ssn: userData.ssn
    }));
    
    // [Hard 8] DOM-based XSS
    // Executing payload directly from the URL hash
    const hash = window.location.hash.substring(1);
    if (hash) {
      setTimeout(hash, 1000); // setTimeout evaluates strings as code if passed directly
    }
  }, []);

  const handleDelete = async () => {
    // [Medium 7] Optimistic UI De-Sync
    // Updating local state without verifying the network response
    fetch('/api/users/delete', { method: 'DELETE' });
    setProfile(null); // Contact vanishes even if the server threw a 500
  };

  const syncData = () => {
    // [Medium 10] Unhandled Promise Rejection
    // A fire-and-forget API call with no .catch() block
    fetch('/api/sync', { method: 'POST', body: JSON.stringify(userData) });
  };

  return (
    <div>
      <h1>User Profile</h1>
      {/* [Easy 9] Frontend XSS */}
      {/* Rendering unsanitized user input directly into the DOM */}
      <div dangerouslySetInnerHTML={{ __html: userData.bio }} />
      
      <button onClick={handleDelete}>Delete Account</button>
      <button onClick={syncData}>Sync Data</button>
    </div>
  );
}

export function LiveSearch() {
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState("");

  const handleSearch = (e) => {
    const q = e.target.value;
    setQuery(q);
    
    // [Medium 9] State Race Condition
    // Sending multiple requests rapidly. If a slow request finishes after a fast one,
    // the UI will show outdated results. Needs an AbortController or effect cleanup.
    fetch(`/api/search?q=${q}`)
      .then(res => res.json())
      .then(data => {
        setResults(data);
      });
  };

  return (
    <div>
      <input type="text" value={query} onChange={handleSearch} placeholder="Search..." />
      <ul>
        {results.map(r => <li key={r.id}>{r.name}</li>)}
      </ul>
    </div>
  );
}
