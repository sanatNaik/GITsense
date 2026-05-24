"use client"
import React from 'react'
import { useState } from 'react';
import axios from 'axios';

const RepoInput = ({onSubmit}) => {
	const [repoUrl,setRepoUrl] = useState("");
	function handleSubmit(e) {
		e.preventDefault();
		onSubmit(repoUrl);
	}
  return (
	<div className='flex items-center justify-center w-full h-[10%] '>
	  <input type="text" value={repoUrl} onChange={e => setRepoUrl(e.target.value)} name="reponame" className='flex bg-black text-white text-xl p-2 w-[80%] h-[70%]'/>
	  <button type="submit" onClick={e => handleSubmit(e)} className='flex items-center justify-center bg-gray-200 p-2 w-[10%] h-[70%]'>Submit</button>
	</div>
  )
}

export default RepoInput
