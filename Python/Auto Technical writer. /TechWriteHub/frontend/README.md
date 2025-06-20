# TechWriteHub Frontend

TechWriteHub is a full-stack application designed to teach and assist users in technical writing. This document provides an overview of the frontend setup and usage.

## Project Structure

The frontend of TechWriteHub is built using React and Tailwind CSS. Below is the structure of the frontend directory:

```
frontend/
├── public/
│   └── index.html          # Main HTML file for the React application
├── src/
│   ├── components/         # Contains reusable React components
│   │   ├── Dashboard/      # Dashboard component
│   │   ├── Editor/         # Live writing editor component
│   │   ├── Glossary/       # User-generated glossary component
│   │   ├── ProjectTracker/  # Project management component
│   │   ├── StyleGuide/     # Style guide reference component
│   │   ├── TemplatesLibrary/# Templates library component
│   │   └── Tutorials/      # Writing tutorials component
│   ├── pages/              # Contains page components for routing
│   │   ├── Home.jsx        # Home page component
│   │   ├── Login.jsx       # Login page component
│   │   ├── Register.jsx    # Registration page component
│   │   └── Profile.jsx     # User profile page component
│   ├── App.jsx             # Main application component
│   ├── index.js            # Entry point for the React application
│   └── styles/             # Contains CSS styles
│       └── tailwind.css    # Tailwind CSS styles
├── package.json             # npm configuration file for frontend
└── tailwind.config.js       # Tailwind CSS configuration file
```

## Getting Started

To get started with the frontend application, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd TechWriteHub/frontend
   ```

2. **Install dependencies**:
   ```
   npm install
   ```

3. **Run the application**:
   ```
   npm start
   ```

   This will start the development server and open the application in your default web browser.

## Features

- **Writing Tutorials**: Access structured lessons on various technical writing topics.
- **Templates Library**: Download and edit templates for common technical documents.
- **Live Writing Editor**: Utilize a markdown or rich text editor with helpful tips and error checking.
- **Style Guide Reference**: Searchable style guide for maintaining consistency in writing.
- **Glossary Tool**: Contribute to and utilize a user-generated glossary.
- **Project Tracker**: Manage writing projects with a to-do list or Kanban-style board.
- **Export Options**: Export documents in PDF, HTML, or Markdown formats.
- **User Progress Tracking**: Track completion of tutorials and writing practice.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.