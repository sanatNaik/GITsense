"use client"

import React, { useState } from "react";

const TreeNode = ({
    node,
    handleFileClick,
    selectedFile
}) => {

    const [isOpen, setIsOpen] = useState(true);

    const handleClick = () => {
        if (node.type === "folder") {
            setIsOpen(!isOpen);
        }

        if (node.type === "file") {
            handleFileClick(node);
        }
    };

    const isSelected =
        node.type === "file" &&
        selectedFile?.path === node.path;

    return (
        <div className="text-xl">

            <div
                onClick={handleClick}
                className={`
                    flex items-center gap-1
                    px-2 py-1
                    rounded
                    cursor-pointer
                    transition-colors
                    ${isSelected
                        ? "bg-gray-300"
                        : "hover:bg-gray-300/60"
                    }
                `}
            >

                {/* Folder arrow */}
                {node.type === "folder" ? (
                    <span className="w-4 text-sm text-gray-600">
                        {isOpen ? "▼" : "▶"}
                    </span>
                ) : (
                    <span className="w-4"></span>
                )}

                {/* Icon */}
                <span>
                    {node.type === "folder" ? "📁" : "📄"}
                </span>

                {/* Name */}
                <span
                    className={
                        node.type === "folder"
                            ? "font-semibold text-gray-800"
                            : "text-gray-700"
                    }
                >
                    {node.name}
                </span>

            </div>

            {isOpen && node.children && (
                <div className="ml-4">
                    {node.children.map((child) => (
                        <TreeNode
                            key={child.path || child.name}
                            node={child}
                            handleFileClick={handleFileClick}
                            selectedFile={selectedFile}
                        />
                    ))}
                </div>
            )}

        </div>
    );
};


const RepoStatus = ({
    data,
    handleFileClick,
    handleOverview,
    selectedFile
}) => {

    if (!data) {
        return (
            <p className="px-6 mt-4 text-lg text-gray-700">
                No repo data loaded
            </p>
        );
    }

    return (
        <div className="px-6 py-6 overflow-y-auto text-xl">

            {/* Overview */}
            <div
                onClick={handleOverview}
                className={`
                    flex items-center gap-1
                    px-2 py-1
                    mb-2
                    rounded
                    cursor-pointer
                    text-lg
                    transition-colors
                    ${!selectedFile
                        ? "bg-gray-300 text-gray-800"
                        : "text-gray-700 hover:bg-gray-300/60"
                    }
                `}
            >
                <span className="w-4"></span>
                <span className="font-semibold">
                    Overview
                </span>
            </div>

            {/* Repository tree */}
            <TreeNode
                node={data}
                handleFileClick={handleFileClick}
                selectedFile={selectedFile}
            />

        </div>
    );
};

export default RepoStatus;