# sofe4840u-final

Final Project for SOFE 4840U - Software and Computer Security

## Backend Documentation

### Directory Structure

```sh
backend
├── .gitignore  
├── api.py  
├── posts.json  
├── requirements.txt  
├── users.json  
├── models/  
│   ├── __init__.py  
│   ├── challenge.py  
│   ├── comment.py  
│   ├── post.py  
│   └── user.py  
└── scripts/  
  ├── create_challenge.sh  
  ├── register.sh  
  ├── sign.sh  
  ├── signer.py  
  ├── verifier.py  
  └── verify.sh  
```

### File Explanations

- **.gitignore**  
  Lists files and directories (like `__pycache__/`) that Git should ignore.

- **api.py**  
  Contains the Flask application and defines HTTP endpoints for user registration, login, post interactions (like adding comments and toggling likes), and challenge-based authentication.

- **posts.json**  
  Stores serialized post objects including details like title, description, likes, and comments.

- **requirements.txt**  
  Lists Python dependencies required to run the backend (e.g., Flask, bcrypt).

- **users.json**  
  Contains serialized user objects with their usernames, public keys, and profile picture URLs.

- **models/**  
  This folder contains the data models used in the application:
  - ****init**.py**: Imports and exposes all model classes.
  - **challenge.py**: Manages challenge creation, verification, and disposal for RSA-based authentication.
  - **comment.py**: Defines the Comment model used to represent post comments.
  - **post.py**: Defines the Post model including functionality for saving posts, managing likes, and adding comments.
  - **user.py**: Defines the User model and methods for registering users and persisting them to disk.

- **scripts/**  
  Contains utility scripts to interact with the backend:
  - **create_challenge.sh**: Sends a POST request to generate a new challenge for a user.
  - **register.sh**: Script for registering a new user with their public key and profile picture URL.
  - **sign.sh**: Uses `signer.py` to sign a challenge using a given RSA private key.
  - **signer.py**: Python script that signs challenges with an RSA private key.
  - **verifier.py**: Python script that verifies a signed challenge using the corresponding RSA public key.
  - **verify.sh**: Script that calls `verifier.py` to check if a challenge signature is valid.

### API Specification

Each endpoint except for `/register` will need a challenge string, generated from the `/create_challenge` endpoint, to be signed by the user's private key. The signed challenge will then be sent to the corresponding endpoint for verification.

| Endpoint         | Method(s)   | Description                                                                                                                                                         | Request Payload                                                                                                                   |
|------------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| /register        | POST        | Registers a new user by providing a username, profile picture URL, and public key. Checks for missing fields and duplicate usernames.                              | { "username": string, "profile_picture_url": string, "public_key": string }                                                       |
| /create_challenge| POST        | Creates an authentication challenge for a user. Disposes of any previous active challenge before issuing a new one.                                                   | { "username": string }                                                                                                            |
| /login           | POST        | Verifies the signed challenge and logs in the user if authentication is successful. Returns user details upon successful login.                                      | { "username": string, "challenge_signature": string }                                                                             |
| /toggle_like     | POST, OPTIONS| Toggles the like status of a post by adding or removing the username from the post likes list. Validates the user challenge before executing the toggle.          | { "username": string, "challenge_signature": string, "post_id": string }                                                            |
| /posts           | POST, OPTIONS| Retrieves all posts with enhanced details including author and comment profile pictures. Validates the user challenge before fetching posts.                        | { "username": string, "challenge_signature": string }                                                                             |
| /add_comment     | POST, OPTIONS| Adds a comment to a specific post. Validates the user challenge and requires the post ID and comment text to be provided.                                             | { "username": string, "challenge_signature": string, "post_id": string, "comment": string }                                          |

### Data Models

| Model        | Persisted           | Python File          | Description                                                                                                                                           |
|--------------|---------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| User         | Yes (users.json)    | models/user.py       | Represents a user with a username, public key, and profile picture URL. Users are created, stored, and updated in users.json for persistence.         |
| Post         | Yes (posts.json)    | models/post.py       | Defines a post with attributes such as title, description, image URL, likes, and comments. Posts are saved in posts.json and can be updated or retrieved. |
| Comment      | Embedded            | models/comment.py    | Models a comment with a username and description. Comments are embedded within Post objects in posts.json, not persisted as standalone files.         |
| Challenge    | No                  | models/challenge.py  | Manages authentication challenges for RSA-based authentication. Challenges are created, validated, and disposed in memory during runtime.             |

In our overall application, each model serves to encapsulate a component of the application's data and behavior:

- The User model (models/user.py) handles registration and user persistence.
- The Post model (models/post.py) manages content creation, likes, and comment additions, persisting posts to disk.
- The Comment model (models/comment.py) provides a structure for managing user comments within posts.
- The Challenge model (models/challenge.py) implements temporary authentication challenges essential for secure login and actions.

These models work together to support backend operations such as user management, post interactions, and security through challenge-response authentication.

## Frontend Documentation

The frontend portion of the project is a React application built using Vite. Below is an overview of the key files and packages used in the project.

### Directory Structure

```md
### Directory Structure Overview

frontend
├── index.html  
├── package.json  
└── frontend  
  └── src  
    ├── App.css  
    ├── App.tsx  
    ├── main.tsx  
    ├── components/  
    │   ├── Comment.jsx  
    │   └── Post.jsx  
    ├── pages/  
    │   ├── LoginPage.jsx  
    │   ├── PostsPage.jsx  
    │   └── RegisterPage.jsx  
    └── utils/  
      └── cryptoUtil.js  
```

- **src/components/**  
  Contains reusable UI components.
  
- **src/pages/**  
  Contains page-level components corresponding to different routes in the application.
  
- **src/utils/**  
  Contains utility functions used across the frontend.
  
- **App.tsx**  
  The main application component which sets up routing and global state management.

### File Explanations

#### src/components/

- **Comment.jsx**  
  Renders individual comments on a post. It handles displaying the comment's author, profile picture, and text. This component is used within the post component to render comments dynamically.

- **Post.jsx**  
  Displays a single post including post title, description, image, likes, and comments. It also includes interactive features such as toggling likes and adding new comments. It leverages the Comment component for rendering its list of comments.

#### src/pages/

- **LoginPage.jsx**  
  Provides the login interface. Users are prompted to enter their username and RSA private key. It then uses these credentials to sign a challenge for secure authentication before logging in.

- **PostsPage.jsx**  
  Displays the feed of posts. This page fetches posts from the backend by generating a signed challenge and updating the UI. It also manages user interactions such as liking posts and adding comments.

- **RegisterPage.jsx**  
  Allows users to generate an RSA key pair and register by entering a username, using the generated public key, and providing a profile picture URL. This page includes features to copy keys to the clipboard for secure storage.

#### src/utils/

- **cryptoUtil.js**  
  Contains a helper function `sign` that uses the Web Cryptography API to import RSA private keys and sign a provided challenge string. The generated signature is encoded in Base64 and returned for use in authentication flows.

#### App.tsx

- **App.tsx**  
  The root component that sets up the React Router for navigating between different pages (login, register, posts). It manages global authentication state using React state hooks and persists user information in localStorage and sessionStorage. Additionally, it renders the navigation bar when a user is logged in.

### Packages Used (package.json)

- **react & react-dom**  
  Core libraries for building and rendering the user interface.

- **react-router-dom**  
  Provides routing capabilities to navigate between pages, handling routes like `/login`, `/register`, and `/posts`.

- **tailwindcss**  
  Used for styling the application, providing utility-first CSS classes to create a responsive and modern UI.

- **@vitejs/plugin-react**  
  A Vite plugin that enhances the development experience for React by providing fast HMR and optimized builds.

Other dependencies and devDependencies such as ESLint, TypeScript, and globals assist with code quality, type checking, and overall tooling support.

This documentation outlines the structure and purpose of the main components in the frontend, as well as the key packages utilized to build a secure and responsive application.
