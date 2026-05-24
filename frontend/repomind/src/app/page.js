	"use client"
	import Image from "next/image";
	import Header from "@/components/header/Header";
	import RepoInput from "@/components/repo/RepoInput";
	import RepoStatus from "@/components/repo/RepoStatus";
	import Chat from "@/components/chat/Chat";
	import ChatInput from "@/components/chat/ChatInput";
	import { useState } from "react";


	export default function Home() {
		const [repoData,setRepoData] = useState(null);

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
				setRepoData(data);
				} catch (err) {
				console.log(err);
			}

		};
	return (
		<div className="min-h-screen flex flex-col">
			<div> 
				<Header/> 
			</div>
			<div className="flex flex-1">
				<div className="flex flex-col w-[40%] bg-gray-400 text-white">
					<RepoInput onSubmit={fetchRepo} />
					<RepoStatus data={repoData}/>
				</div>
				<div className="flex flex-col w-[60%] bg-gray-300 text-white ">
					<Chat/>
					<ChatInput/>
				</div>
			</div>
		</div>
		
	);
	}
