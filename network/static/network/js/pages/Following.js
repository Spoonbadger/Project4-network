


function FollowingPosts({ userId }) {
    const [followingPosts, setFollowingPosts] = React.useState([])
    const [likedPosts, setLikedPosts] = React.useState({})
    const [loading, setLoading] = React.useState(false)
    const [currentPage, setCurrentPage] = React.useState(1)
    const [postsPerPage, setPostsPerPage] = React.useState(10)


    // Fetch Following posts
    React.useEffect(() => {
        setLoading(true)
        fetch('/api/following_posts/')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched data: ', data);
            setFollowingPosts(data.posts)
            setLikedPosts(data.liked_post)
            setLoading(false)
        })
        .catch(error => {
            console.error("Error loading posts: ", error)
            setLoading(false)
        })
}, [userId]);


    const handleLike = (postId) => {
        fetch(`/like_unlike/${postId}/`, {
            method: 'POST',
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            setFollowingPosts(followingPosts.map(post => post.id === postId ?
                {...post,
                    liked: data.liked,
                    like_count: data.like_count
                } : post));
            setLikedPosts({...likedPosts, [post.id]: data.liked})
        })
        .catch(error => console.error("Error handling like: ", error))
    };


    const indexOfLastPost = currentPage * postsPerPage
    const indexOfFirstPost = indexOfLastPost - postsPerPage
    const currentFollowingPosts = followingPosts.slice(indexOfFirstPost, indexOfLastPost)

    const paginate = pageNumber => setCurrentPage(pageNumber)

    if (loading) {
        return (
            <div id="loading-div">Loading...</div>
        )
    }

    if (followingPosts.length === 0) {
        return <div>You're not following anyone, <a href="/">yet...</a></div>
    }

    else {
        return (
            <div id="following-posts">
                {currentFollowingPosts.map(post => (
                    <FollowingPost
                        key={post.id}
                        post={post}
                        liked={likedPosts[post.id]}
                        handleLike={handleLike}
                    />
                ))}
                <Pagination
                    postsPerPage={postsPerPage}
                    totalPosts={followingPosts.length}
                    paginate={paginate}
                />
            </div>
        )
    }
}


function FollowingPost({ post, liked=false, handleLike }) {
    // <!-- why not post.sender.id instead of post.sender_id?? -->
    return (
        <div style={{ border: 'solid lightgray 1px', margin: '35px', padding: '20px', paddingBottom: '8px' }}>
            <div style={{ color: 'blue' }}>
                <strong>
                    <a href={`/profile/${post.sender_id}`}>{post.sender}</a> 
                </strong> squeeks: 
            </div>
            <h5 style={{ marginTop: '10px', marginLeft: '20px', marginRight: '20px'  }}>{post.post_content}</h5>
            <div style={{ color: 'grey' }}>
                {post.timestamp}
            </div>
            {post.edited_timestamp !== 'Not edited' && (
                <div style={{ color: 'lightgray' }}>
                    {post.edited_timestamp}
                </div>     
            )}
            <div id="likeUnlike-button-container">
                <button id={`like-unlike-button-${post.id}`}
                    className='btn btn-icon'
                    onClick={() => handleLike(post.id)}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path fillRule="evenodd" d={liked ? svgPaths.liked : svgPaths.unliked} />
                    </svg>
                </button>
                <span id={`post-like-count-${post.id}`}>Likes: {post.like_count}</span>
            </div>
        </div>
    )
};



const svgPaths = {
    liked: 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314',
    unliked: 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15'
}


const userId = window.userId
ReactDOM.render(<FollowingPosts userId = {userId} />, document.getElementById('following-posts'));