import React from 'react';

const Home = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-4xl font-bold mb-4">Welcome to TechWriteHub</h1>
            <p className="text-lg text-center mb-8">
                Your go-to platform for mastering technical writing. Explore tutorials, templates, and tools to enhance your writing skills.
            </p>
            <div className="flex flex-wrap justify-center">
                <a href="/tutorials" className="m-2 p-4 bg-blue-500 text-white rounded hover:bg-blue-600">
                    Explore Tutorials
                </a>
                <a href="/templates" className="m-2 p-4 bg-green-500 text-white rounded hover:bg-green-600">
                    View Templates
                </a>
                <a href="/editor" className="m-2 p-4 bg-purple-500 text-white rounded hover:bg-purple-600">
                    Open Editor
                </a>
                <a href="/glossary" className="m-2 p-4 bg-orange-500 text-white rounded hover:bg-orange-600">
                    Access Glossary
                </a>
            </div>
        </div>
    );
};

export default Home;