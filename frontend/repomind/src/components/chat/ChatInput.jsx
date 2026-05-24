import React from 'react'

const ChatInput = () => {
  return (
	<div className='flex justify-center items-center bg-gray-400 h-[20%] w-full'>
	  <input type="text" className='bg-white w-[80%] h-[80%] text-black'/>
	  <button className='flex w-[20%] h-[80%]'>Submit</button>
	</div>
  )
}

export default ChatInput
