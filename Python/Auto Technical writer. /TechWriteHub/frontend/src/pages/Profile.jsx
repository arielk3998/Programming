import React from 'react';

const Profile = () => {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">User Profile</h1>
            <div className="bg-white shadow-md rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-2">Profile Information</h2>
                <p className="mb-2"><strong>Name:</strong> [User Name]</p>
                <p className="mb-2"><strong>Email:</strong> [User Email]</p>
                <p className="mb-2"><strong>Joined:</strong> [Join Date]</p>
            </div>
            <div className="mt-6">
                <h2 className="text-xl font-semibold mb-2">User Progress</h2>
                <ul className="list-disc pl-5">
                    <li>Tutorials Completed: [Number]</li>
                    <li>Projects in Progress: [Number]</li>
                </ul>
            </div>
        </div>
    );
};

export default Profile;