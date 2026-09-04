"use client";

export default function FileContent({
    fileContent,
    architecture,
    selectedFile,
    onShowOverview,
}) {

    // --------------------------------------------------
    // Repository Overview
    // --------------------------------------------------

    if (!selectedFile) {

        if (!architecture) {
            return (
                <div className="h-full flex items-center justify-center text-gray-500">
                    <div className="text-center">
                        <p className="text-lg font-medium">
                            No repository loaded
                        </p>

                        <p className="text-lg mt-2 text-gray-400">
                            Load a repository to view its architecture.
                        </p>
                    </div>
                </div>
            );
        }

        return (
            <div className="h-full overflow-y-auto">

                {/* Header */}
                <div className="px-8 pt-8 pb-6 border-b border-gray-300 bg-white">

                    <div className="flex items-center gap-3">

                        <div className="w-11 h-11 rounded-xl bg-black flex items-center justify-center text-white text-xl">
                            ⌘
                        </div>

                        <div>
                            <p className="text-xs font-medium uppercase tracking-wider text-gray-400">
                                Repository
                            </p>

                            <h1 className="text-2xl font-bold text-gray-900">
                                Architecture Overview
                            </h1>
                        </div>

                    </div>

                </div>


                {/* Content */}
                <div className="p-8 space-y-6">

                    {/* Purpose */}
                    <section className="bg-white rounded-2xl border border-gray-200 p-6 shadow-lg">

                        <div className="flex items-center gap-2 mb-4">

                            

                            <h2 className="font-semibold text-gray-900">
                                Purpose
                            </h2>

                        </div>

                        <p className="text-lg leading-6 text-gray-600">
                            {architecture.purpose}
                        </p>

                    </section>


                    {/* Tech Stack */}
                    <section className="bg-white rounded-2xl border border-gray-200 p-6 shadow-lg">

                        <div className="flex items-center gap-2 mb-4">

                            

                            <h2 className="font-semibold text-gray-900">
                                Technology Stack
                            </h2>

                        </div>

                        <div className="flex flex-wrap gap-2">

                            {architecture.tech_stack?.map((tech, index) => (

                                <span
                                    key={index}
                                    className="
                                        px-3 py-1.5
                                        rounded-lg
                                        bg-gray-100
                                        border border-gray-200
                                        text-lg
                                        font-medium
                                        text-gray-700
                                        hover:bg-gray-200
                                        transition
                                    "
                                >
                                    {tech}
                                </span>

                            ))}

                        </div>

                    </section>


                    {/* Entry Points */}
                    <section className="bg-white rounded-2xl border border-gray-200 p-6 shadow-lg">

                        <div className="flex items-center gap-2 mb-4">

                            

                            <h2 className="font-semibold text-gray-900">
                                Entry Points
                            </h2>

                        </div>

                        <div className="space-y-2">

                            {architecture.entry_points?.map(
                                (entry, index) => (

                                    <div
                                        key={index}
                                        className="
                                            px-4 py-3
                                            rounded-lg
                                            bg-gray-50
                                            border border-gray-200
                                            font-mono
                                            text-lg
                                            text-gray-700
                                        "
                                    >
                                        {entry}
                                    </div>

                                )
                            )}

                        </div>

                    </section>


                    {/* Directory Structure */}
                    <section className="bg-white rounded-2xl border border-gray-200 p-6 shadow-lg">

                        <div className="flex items-center gap-2 mb-4">

                    

                            <h2 className="font-semibold text-gray-900">
                                Project Structure
                            </h2>

                        </div>

                        <div className="space-y-2">

                            {architecture.directory_structure?.map(
                                (item, index) => (

                                    <div
                                        key={index}
                                        className="
                                            flex items-start
                                            gap-3
                                            px-4 py-3
                                            rounded-lg
                                            bg-gray-50
                                            border border-gray-200
                                            text-lg
                                            text-gray-700
                                        "
                                    >
                                        <span>📁</span>

                                        <span>
                                            {item}
                                        </span>

                                    </div>

                                )
                            )}

                        </div>

                    </section>


                    {/* Key Modules */}
                    <section className="bg-white rounded-2xl border border-gray-200 p-6 shadow-lg">

                        <div className="flex items-center gap-2 mb-4">

                            

                            <h2 className="font-semibold text-gray-900">
                                Key Modules
                            </h2>

                        </div>

                        <div className="space-y-3">

                            {architecture.key_modules?.map(
                                (module, index) => (

                                    <div
                                        key={index}
                                        className="
                                            px-4 py-3
                                            rounded-lg
                                            bg-gray-50
                                            border border-gray-200
                                            text-lg
                                            leading-5
                                            text-gray-700
                                        "
                                    >
                                        {module}
                                    </div>

                                )
                            )}

                        </div>

                    </section>


                    {/* Patterns */}
                    <section className="bg-white rounded-2xl border border-gray-200 p-6 shadow-lg">

                        <div className="flex items-center gap-2 mb-4">

                            

                            <h2 className="font-semibold text-gray-900">
                                Architecture Patterns
                            </h2>

                        </div>

                        <div className="space-y-3">

                            {architecture.notable_patterns?.map(
                                (pattern, index) => (

                                    <div
                                        key={index}
                                        className="
                                            flex
                                            gap-3
                                            items-start
                                            text-lg
                                            leading-5
                                            text-gray-600
                                        "
                                    >
                                        <span className="text-gray-400">
                                            •
                                        </span>

                                        <span>
                                            {pattern}
                                        </span>

                                    </div>

                                )
                            )}

                        </div>

                    </section>

                </div>

            </div>
        );
    }


    // --------------------------------------------------
    // File Viewer
    // --------------------------------------------------

    return (
        <div className="h-full flex flex-col bg-gray-950">

            {/* File Header */}
            <div className="
                h-14
                flex
                items-center
                justify-between
                px-5
                border-b
                border-gray-800
                bg-gray-900
            ">

                <div className="flex items-center gap-3 min-w-0">

                    <span className="text-lg">
                        📄
                    </span>

                    <div className="min-w-0">

                        <p className="text-lg font-medium text-white truncate">
                            {selectedFile.name}
                        </p>

                        <p className="text-xs text-gray-500 truncate">
                            {selectedFile.path}
                        </p>

                    </div>

                </div>


                {/* Back to Overview */}
                <button
                    onClick={onShowOverview}
                    className="
                        flex
                        items-center
                        gap-2
                        px-3
                        py-1.5
                        rounded-lg
                        bg-gray-800
                        hover:bg-gray-700
                        text-gray-300
                        hover:text-white
                        text-xs
                        font-medium
                        transition
                    "
                >
                    ← Overview
                </button>

            </div>


            {/* Code */}
            <div className="flex-1 overflow-auto">

                <pre className="
                    p-6
                    text-lg
                    leading-6
                    text-gray-200
                    font-mono
                    whitespace-pre
                ">
                    {fileContent}
                </pre>

            </div>

        </div>
    );
}