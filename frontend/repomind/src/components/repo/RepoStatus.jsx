import React from 'react'

const TreeNode = ({node}) => {
	return(
		<div>
			<p className='text-black font-semibold text-base'>
				{node.type==="folder"?"📁":"g"}{node.name}
			</p>

			{node.children && (
				<div className="ml-4">
				{node.children.map(child => (
					<TreeNode key={child.name} node={child} />
				))}
				</div>
			)}
		</div>
	)
}

const RepoStatus = ({data}) => {
	if(!data) return <p>No repo data loaded</p>;
	const folders = data.children.filter(item=>
		item.type==='folder'
	);
	return(
		<div className='p-5'>
			<TreeNode node={data}/>
		</div>
	);
  
}

export default RepoStatus
