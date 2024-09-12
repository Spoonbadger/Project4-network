// import React, {useEffect, useState} from 'react';


function NewPostForm({ onPostCreated }) {
    const [content, setContent] = React.useState('');
    const [loading, setLoading] = React.useState(false);

    const handleSubmitPost = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('/new_post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    post_content: content, // Send content as JSON
                }),
            });

            if (response.ok) {
                const data = await response.json();
                setContent('');
                onPostCreated(); // Callback to refresh the posts list or display a success message
            } else {
                console.error('Error creating post:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ border: 'solid lightgrey 1px', margin: '35px' }}>
            <h3 id="new-post-title">New Post</h3>
            <form style={{ margin: '30px', marginTop: '20px', marginBottom: '20px' }} onSubmit={handleSubmitPost}>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="How are you feeling?..."
                    style={{
                        width: '100%',
                        height: '80px',
                        border: 'solid lightgrey 1px',
                        backgroundColor: 'rgba(217, 253, 208, 0.183)',
                        boxSizing: 'border-box',
                        display: 'block',
                        marginTop: '20px',
                    }}
                />
                <button className="btn btn-primary" style={{ marginTop: '10px' }} type="submit" disabled={loading}>
                    {loading ? 'Posting...' : 'Post'}
                </button>
            </form>
        </div>
    );
}


// Each post element
function Post({ post, liked=false, currentUser=null, handleLike, handleEdit, handleDelete }) {
    const [isEditing, setIsEditing] = React.useState(false);
    const [editedContent, setEditedContent] = React.useState(post.post_content)
    const [originalContent, setOriginalContent] = React.useState(post.post_content)

    const svgPaths = {
        liked: 'M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314',
        unliked: 'm8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15'
    }

    const editClicked = () => {
        setIsEditing(!isEditing);
    }

    const saveEdit = () => {
        handleEdit(post.id, editedContent)
        setIsEditing(false)
    }

    const cancelEdit = () => {
        setEditedContent(originalContent)
        setIsEditing(false)
    }

    const deleteSqueek = () => {
        if (window.confirm("Are you sure you want to delete this squeek?")) {
            handleDelete(post.id)
            setIsEditing(false)
        }
    }

    return (
        <div style={{ border: 'solid lightgray 1px', margin: '35px', padding: '20px', paddingBottom: '8px' }}>
            <div>
                <strong>
                    {currentUser ? (
                        <a href={`/profile/${post.sender_id}`}>{post.sender}</a>
                    ) : (
                        post.sender
                )}
                </strong> squeeks:
            </div>
            {isEditing ? (
                <textarea value={editedContent} onChange={(e) => setEditedContent(e.target.value)}
                style={{width: '100%', marginTop: '10px', marginBottom: '10px'}} />
            ) : (
                <h5 style={{ marginTop: '10px', marginLeft: '20px', marginRight: '20px' }}>{post.post_content}</h5>
            )}
            <div style={{ color: 'grey' }}>
                {post.timestamp}
            </div>
            {post.edited_timestamp !== 'Not edited' && (
                <div style={{ color: 'lightgrey' }}>
                    Edited: {post.edited_timestamp}
                </div>
            )}
            <div id="likeUnlike-button-container">
                <button
                    id={`like-unlike-button-${post.id}`}
                    className="btn btn-icon"
                    onClick={() => handleLike(post.id)}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path fillRule="evenodd" d={liked ? svgPaths.liked : svgPaths.unliked} />
                    </svg>
                </button>
                <span id={`post-like-count-${post.id}`}>Likes: {post.like_count}</span>
            </div>
            {currentUser && post.sender === currentUser && (
                <div>
                    {isEditing ? (
                        <div>
                            <button onClick={saveEdit} className="btn btn-warning" style={{padding: '5px'}} >Save</button>
                            <button onClick={cancelEdit} className="btn btn-light" style={{padding: '5px', marginLeft: '10px'}}>Cancel</button>
                            <button onClick={deleteSqueek} className="btn btn-danger" style={{ padding: '5px', marginLeft: '10px' }}>Delete Squeek</button>
                        </div>
                    ) : (
                        <button onClick={editClicked} className="btn btn-light" style={{ padding: '5px', paddingLeft: '8px', paddingRight: '8px' }}>Edit</button>
                    )}
                </div>
            )}
        </div>
    );
}



// FETCH ALL THE POSTS
function Posts( {userId} ) {
    const [posts, setPosts] = React.useState([]);
    const [currentUser, setCurrentUser] = React.useState(null);
    const [likedPosts, setLikedPosts] = React.useState({});
    const [loading, setLoading] = React.useState(false)
    const [currentPage, setCurrentPage] = React.useState(1)
    const [postsPerPage] = React.useState(10);

    // Fetch ALL posts
    React.useEffect(() => {
        setLoading(true)
        fetch('/all_posts/')
        .then(response => response.json())
        .then(data => {
            setPosts(data.posts);
            setCurrentUser(data.current_user || null);
            setLikedPosts(data.liked_post || {});
            setLoading(false)
        });
    }, []);


    const handlePostCreated = () => {
        // Refetch posts after a new post is created
        fetch('/all_posts/')
            .then(response => response.json())
            .then(data => {
                setPosts(data.posts);
            });
    };


    const handleLike = (postId) => {
        const csrftoken = getCookie('csrftoken');
        fetch(`/like_unlike/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            setPosts(posts.map(post => post.id === postId ? { ...post, liked: data.liked, like_count: data.like_count } : post));
            setLikedPosts({ ...likedPosts, [postId]: data.liked });
        })
        .catch(error => console.error('Error liking/unliking post:', error));
    };

    const handleEdit = (postId, newContent) => {
        fetch(`/edit_post/${postId}/`, {
            method: 'POST',
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({
                post_content: newContent
            })
        })
        .then(response => response.json())
        .then(data => {
            setPosts(posts.map(post => post.id === postId ? 
                {...post, post_content: newContent, edited_timestamp: post.edited_timestamp} : post));
        })
        .catch(error => console.log("Error editing post: ", error));
    }

    const handleDelete = (postId) => {
        fetch(`/${postId}/delete/`, {
            method: 'DELETE',
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                console.log("Delete squeek successful.")
                window.location.href = '/'
            }
            else {
                console.log("Failure deleting tweet", response.statusText)
            }
        })
    }

    const indexOfLastPost = currentPage * postsPerPage;
    const indexOfFirstPost = indexOfLastPost - postsPerPage;
    const currentPosts = posts.slice(indexOfFirstPost, indexOfLastPost)
    
    const paginate = pageNumber => setCurrentPage(pageNumber)
    React.useEffect(() => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }, [currentPage]);
    

    if (loading) {
        return <div>Loading...</div>
    }
    else {
        return (
            <div>
                <div>
                    <NewPostForm onPostCreated={handlePostCreated} />
                </div>
                <div id="all-posts">
                    {currentPosts.length === 0 ? <div>No posts, yet...</div> : currentPosts.map(post => (
                        <Post 
                            key={post.id} 
                            post={post} 
                            liked={likedPosts[post.id]} 
                            currentUser={currentUser} 
                            handleLike={handleLike}
                            handleEdit={handleEdit}
                            handleDelete={handleDelete}
                        />
                    ))}
                    <Pagination 
                        postsPerPage={postsPerPage}
                        totalPosts={posts.length}
                        paginate={paginate}
                    />
                </div>
            </div>
        );
    }
}
// Put in ? : if no posts to display <div>No posts, yet...</div>


function Pagination({ postsPerPage, totalPosts, paginate }) {
    const pageNumbers = [];
    for (let i = 1; i <= Math.ceil(totalPosts / postsPerPage); i++) {
        pageNumbers.push(i)
    }
    return (
        <nav>
            <ul className = 'pagination'>
                {pageNumbers.map(number => (
                    <li key={number} className='page-item'>
                        <a onClick={() => paginate(number)} href='#!' className='page-link'>
                            {number}
                        </a>
                    </li>
                ))}
            </ul>
        </nav>
    )
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


ReactDOM.render(<Posts />, document.getElementById('all-posts'));