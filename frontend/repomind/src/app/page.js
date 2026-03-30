import Image from "next/image";
import Header from "@/components/header/Header";
import RepoInput from "@/components/repo/RepoInput";
import RepoStatus from "@/components/repo/RepoStatus";
import Chat from "@/components/chat/Chat";
export default function Home() {
  return (
    <div>
		<div> <Header/> </div>
		<div class="flex">
			<div>
				<RepoInput/>
				<RepoStatus/>
			</div>
			<div>
				<Chat/>
			</div>
		</div>
	</div>
	
  );
}
