	"use client"
	import Image from "next/image";
	import Header from "@/components/header/Header";
	import RepoInput from "@/components/repo/RepoInput";
	import RepoStatus from "@/components/repo/RepoStatus";
	import Chat from "@/components/chat/Chat";
	import ChatInput from "@/components/chat/ChatInput";
	import FileContent from "@/components/filecontent/FileContent";
	import { useRef } from "react";
	import { useState } from "react";


	export default function Home() {
		const [repoData,setRepoData] = useState(null);
		const [selectedFile,setSelectedFile] = useState(null);
		const [fileContent,setFileContent] = useState("")
		const [messages, setMessages] = useState([]);
		const [architecture, setArchitecture] = useState(null);
		const sessionId = useRef(crypto.randomUUID());

		const fetchRepo = async (repoUrl) => {
			try {
				const res = await fetch("http://127.0.0.1:8000/repo", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({ repourl: repoUrl }),
				});

				const data = await res.json();

				if (!res.ok) {
					throw new Error(data.detail || "Failed to load repository");
				}

				setRepoData(data);
				setArchitecture(data.architecture);

			} catch (err) {
				console.log(err);
				alert(err.message);
			}
		};
		const handleFileClick = async (file) => {

			setSelectedFile(file);
			try {
				const res = await fetch("http://127.0.0.1:8000/file-content", {
					method: "POST",
					headers: {
					"Content-Type": "application/json",
					},
					body: JSON.stringify({
					path: file.path
					}),
				});
				const data = await res.json();
				setFileContent(data.content);

			} catch (err) {
				console.log(err);
			}
		};
		const handleOverview = () => {
			setSelectedFile(null);
			setFileContent("");
		};
		const sendMessage = async (query) => {
			setMessages((prev) => [
				...prev,
				{ role: "user", text: query }
			]);

			try {
				const res = await fetch("http://127.0.0.1:8000/search", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					session_id: sessionId.current,
					query: query
				})
				});

				const data = await res.json();

				setMessages(prev => [
					...prev,
					{
						role: "assistant",
						text: data.answer
					}
				]);
			} catch (err) {
				console.log(err);
			}
		};

	return (
		<div className="h-screen flex flex-col overflow-hidden">
			<div className="h-[13%]"> 
				<Header/> 
			</div>
			<div className="flex flex-1 h-[87%] overflow-hidden">
				<div className="flex flex-col w-[25%] overflow-hidden bg-gray-400 text-white py-10">
					<RepoInput onSubmit={fetchRepo} />
					<RepoStatus
						data={repoData?.tree}
						handleFileClick={handleFileClick}
						handleOverview={handleOverview}
						selectedFile={selectedFile}
					/>
				</div>
				<div className="flex flex-col w-[45%] overflow-hidden bg-gray-200">
					<FileContent
						fileContent={fileContent}
						architecture={architecture}
						selectedFile={selectedFile}
						onShowOverview={() => {
							setSelectedFile(null);
							setFileContent("");
						}}
    				/>
				</div>	
				<div className="flex flex-col w-[30%] bg-gray-300">
					<Chat messages={messages} />
					<ChatInput onSend={sendMessage} />
				</div>
			</div>
		</div>
		
	);
	}
