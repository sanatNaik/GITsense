"use client";

import React, { useState } from "react";

const RepoInput = ({ onSubmit }) => {
    const [repoUrl, setRepoUrl] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!repoUrl.trim()) return;

        onSubmit(repoUrl);
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="flex items-center justify-center w-full h-16 pb-5"
        >
            <input
                type="text"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="Enter GitHub repository URL"
                className="flex bg-white text-gray-800 text-xl p-2 w-[70%] h-12 rounded-l-xl"
            />

            <button
                type="submit"
                className="flex items-center justify-center bg-gray-200 text-black text-xl font-bold p-2 w-[20%] h-12 rounded-r-xl hover:bg-black hover:text-white"
            >
                Load
            </button>
        </form>
    );
};

export default RepoInput;