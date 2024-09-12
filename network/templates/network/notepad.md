// HANDLE LIKEUNLIKEBUTTON
export function ActionBtn(props) {
    const {tweet, action} = props
    const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0)
    const [clickLikeUnlike, setClickLikeUnlike] = useState(tweet.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    const handleClick = (event) => {
      event.preventDefault()
      if (action.type === 'like') {
        if (clickLikeUnlike === false) {
          setLikes(likes + 1)
          setClickLikeUnlike(true)
        }
        else {
          setLikes(likes - 1)
          setClickLikeUnlike(false)
        }
      }
    }
    return <button className={className} onClick={handleClick}>{display}</button>
  }