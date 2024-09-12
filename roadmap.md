Plan 6th Sep. 2024
- Im going to do post submission via HTML (consider updating to React later)
- I'm going to load posts via React including likeUnlikeBtn
it does it!


    created the models
    updated admin
    completed login, logout, registration with AbstractUser
    created a couple of users
    made a superuser
    create a post form in html
    posted and check it works
    load all posts:
        post and posts...
    
    -> LikeUnlike button working and showing likes -phew
    -> Edit button working
    -> Add cancel button to post while editing
    own profile
    -> link to own profile from the navbar
    -> set the title correctly, can i do it with react or better with just html for now?
    pagination
    clicking profile link on that person's profile page gives a 404 - remove the link option seems easiest.
    when logged out, no posts show (set the values that won't be there as null in the React components)
    other's profile page
        following and unfollowing
    follow/unfollow button
    following feed page
    delete tweet
    delete tweet works in profile but not all-posts. cancel edit neither.
    delete user
    tricky -> have the new post box as a form rather than through a html render
    tests in test to test the backend
        NEXT:
    other tests (see harvard lectures)

    TODO (not in order):
    @api_view??
    is edit PUT??
    organzie javascript files in a correct manner

    further ahead:
    get rid of the following.html and just have it load on the index, same with the profile.
    like/unlike counts as an edit??
    comment on posts
    repost
    images
    change html create post to React create post




then assess if next is own profile or others' profile.

Long-term
- add followUnfollow button to each post and to each users profile page


1. Tweets
    -> User Permissions
        -> Creating
            -> Text
            -> Image -> Media Storage Server
        -> Delete
        
        -> LONG TERM: Retweeting
            -> Read only serializer
            -> Create only serializer
        -> Liking or Unliking

2. Users
    -> Register
    -> Login
    -> Logout
    -> Profile
        -> Image?
        -> Text?
        -> Follow Button
    -> Feed
        -> User's feed only?
        -> User + who they follow?

3. Following / Followers


Long term todos
- Notifications
- DM
- Explore -> finding hashtags