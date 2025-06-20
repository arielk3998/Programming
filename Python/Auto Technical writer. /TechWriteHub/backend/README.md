# TechWriteHub Backend

TechWriteHub is a full-stack application designed to teach and assist users in technical writing. This README provides an overview of the backend setup, features, and instructions for running the application.

## Features

- **User Authentication**: Secure user registration and login functionality.
- **Writing Tutorials**: API endpoints to manage structured lessons on technical writing.
- **Templates Library**: Access to downloadable and editable templates for common technical documents.
- **Live Writing Editor**: Integration with a live writing editor for real-time document creation.
- **Style Guide Reference**: Searchable API for terminology, tone, and consistency guidelines.
- **Glossary Tool**: User-generated glossary with definitions and tagging capabilities.
- **Project Tracker**: API for managing writing projects with to-do lists or Kanban-style boards.
- **Export Options**: Functionality to export documents in PDF, HTML, or Markdown formats.
- **User Progress Tracking**: Store and retrieve user progress data for tutorials and writing practice.

## Technologies Used

- **Node.js**: JavaScript runtime for building the backend server.
- **Express**: Web framework for Node.js to handle routing and middleware.
- **PostgreSQL/SQLite**: Database for storing user data, tutorials, and glossary entries.
- **JWT**: JSON Web Tokens for secure user authentication.

## Getting Started

### Prerequisites

- Node.js (version 14 or higher)
- PostgreSQL or SQLite installed
- npm (Node Package Manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/TechWriteHub.git
   cd TechWriteHub/backend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file in the backend directory and add your environment variables:
   ```
   DATABASE_URL=your_database_connection_string
   JWT_SECRET=your_jwt_secret
   ```

4. Run database migrations (if applicable):
   ```
   npm run migrate
   ```

### Running the Application

To start the backend server, run:
```
npm start
```

The server will be running on `http://localhost:5000` (or the port specified in your environment variables).

## API Documentation

Refer to the `/src/routes` directory for detailed API endpoint documentation and usage.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.