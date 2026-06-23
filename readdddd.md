# Fixora SAST/LLM Calibration Repository

This repository contains 30 deliberately injected vulnerabilities across backend (Python) and frontend (React) files. It is the "Ground Truth" matrix used to calibrate and test the Fixora SAST and AI engines.

## 🟢 Easy Layer (The "Must Catch" Layer)
These are 10 highly visible, classic vulnerabilities. Any SAST scanner worth its salt should catch these with 100% precision.

1. **[Backend] Hardcoded Secret** (`easy.py`): A `JWT_SECRET` for production is hardcoded directly into the file.
2. **[Backend] SQL Injection** (`easy.py`): User input (`user_id`) is directly concatenated into a raw SQL `SELECT` query.
3. **[Backend] Command Injection** (`easy.py`): User input (`ip_address`) is passed directly to `os.system()` without sanitization.
4. **[Backend] Path Traversal** (`easy.py`): User input (`filename`) is concatenated into a file path and opened for reading.
5. **[Backend] Plaintext Password Comparison** (`easy.py`): The login route compares the password using `==` instead of a hashing function.
6. **[Backend] Missing Authentication** (`easy.py`): The `/api/admin/delete_all_users` route lacks an authentication decorator, allowing anyone to wipe the database.
7. **[Backend] Insecure Deserialization** (`easy.py`): Unpickling arbitrary request data using `pickle.loads()`.
8. **[Backend] Debug Mode Enabled** (`easy.py`): The Flask application is started with `debug=True` in a production-like block.
9. **[Frontend] XSS via dangerouslySetInnerHTML** (`components.jsx`): Rendering raw user input directly into the DOM using React's dangerous HTML injection property.
10. **[Frontend] Hardcoded Secret** (`components.jsx`): Exposing a private AWS Key in the client bundle.

## 🟡 Medium Layer (The "Context & Logic" Layer)
These 10 vulnerabilities test whether the scanner understands the boundaries of the application and the context in which the code executes.

1. **[Backend] SSRF (Server-Side Request Forgery)** (`medium.py`): The backend makes an outbound `requests.get()` call to a URL completely controlled by the user.
2. **[Backend] Mass Assignment** (`medium.py`): Taking raw JSON from the request and spreading it into `User.update()`, allowing attackers to override administrative fields.
3. **[Backend] IDOR / Broken Access Control** (`medium.py`): Fetching user documents based on a URL parameter without validating that the authenticated user actually owns that parameter ID.
4. **[Backend] Weak Cryptography** (`medium.py`): Generating secure tokens using the broken `md5` hashing algorithm.
5. **[Backend] ReDoS (Regular Expression Denial of Service)** (`medium.py`): Validating emails with a poorly written regex pattern that is vulnerable to catastrophic backtracking.
6. **[Backend] XXE (XML External Entity)** (`medium.py`): Parsing XML user input with `resolve_entities=True`, allowing internal file disclosure.
7. **[Frontend] Optimistic UI De-Sync** (`components.jsx`): A business logic flaw where a `fetch` is fired and the local UI state is updated *without* checking if the network request actually succeeded (`res.ok`).
8. **[Frontend] Improper LocalStorage Usage** (`components.jsx`): Dumping raw PII and auth tokens directly into `localStorage`.
9. **[Frontend] State Race Condition** (`components.jsx`): Rapidly typing in a search bar fires multiple requests without an `AbortController`. If a slow request resolves after a fast one, the UI shows stale data.
10. **[Frontend] Unhandled Promise Rejection** (`components.jsx`): A fire-and-forget API call that lacks a `.catch()` block, potentially causing silent failures.

## 🔴 Hard Layer (The "Ultra Pro Max" Layer)
These 10 vulnerabilities are incredibly sneaky. They are designed to completely break traditional Regex scanners and test the deep semantic reasoning of the LLM.

1. **[Backend] Second-Order SQL Injection** (`hard.py`): User input is safely inserted into the database in one route, but retrieved and unsafely concatenated into a query in a completely different route.
2. **[Backend] Sneaky IDOR** (`hard.py`): Instead of putting the ID in the URL, an attacker injects `{"target_user_id": 1}` into the JSON body of a POST request to override the authenticated user's ID during a database update.
3. **[Backend] HTTP Verb Bias Trap** (`hard.py`): A wildly destructive action (`DROP TABLE`) is hidden inside a `PUT` request. (Testing if the AI only looks for destructive actions in `DELETE` routes).
4. **[Backend] Timing Attack** (`hard.py`): Using standard `==` to verify an HMAC signature instead of `hmac.compare_digest`, allowing an attacker to brute force the signature character-by-character based on response times.
5. **[Backend] Logic Bypass** (`hard.py`): The validation block is wrapped in `if 'payment_token' in data:`. If the attacker simply omits the key from the JSON, they skip the check entirely and check out for free.
6. **[Backend] Server-Side Attribute Override** (`hard.py`): Dynamically setting object properties using `setattr(config, key, value)` with untrusted user dictionaries, potentially overriding critical system flags.
7. **[Backend] NoSQL Injection** (`hard.py`): Passing the raw JSON body directly to a PyMongo `find()` query, allowing the attacker to send MongoDB operators like `{"$gt": ""}` to bypass filters.
8. **[Frontend] DOM-based XSS via location.hash** (`components.jsx`): Taking the URL hash fragment and passing it directly to `setTimeout`, which evaluates strings as executable JavaScript code.
9. **[Backend] Blind Command Injection** (`hard.py`): An OS command injection vulnerability where the payload is sent to a background worker (`subprocess.Popen`), meaning the attacker never sees the output on the screen.
10. **[Backend] Misplaced / Ineffective Auth** (`hard.py`): *(Pending Implementation - placeholder for missing decorator logic)*.
