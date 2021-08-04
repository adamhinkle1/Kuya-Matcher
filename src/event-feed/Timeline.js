import React, {useState, useEffect} from 'react'
import Post from './Post'
import db from './firebase'
import {makeStyles} from '@material-ui/core/styles'
import {useStateValue} from '../Context/StateProvider'
import {AdminStateValue} from '../Context/AdminProvider'
import EventPoster from './EventPoster'

const useStyles = makeStyles((theme) => ({
    root: {
        height: '87vh',
        justifyContent: 'center',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
    },
    container: {
        overflowY: 'auto',
        backgroundColor: 'whitesmoke',
        width: '150vh',
        minHeight:'87vh',
        boxShadow: '3px 3px 10px 1px rgba(0,0,0,.5)',
        height: 'auto',
        display: 'block',
        marginLeft: 'auto',
        marginRight: 'auto',
    },
    user:{
        display: 'block',
        marginLeft: 'auto',
        marginRight: 'auto',
        textAlign: 'center',
        fontSize: '3rem',
        textShadow: '5px 5px 15px rgba(0, 0, 0, .3)',
    },
    poster: {
        display: 'block',
        marginLeft: 'auto',
        marginRight: 'auto',
        
        width: '70vw',
        padding: '20px 0px',
    },
    feed: {
        padding: '5px',
        display: 'block',
        marginLeft: 'auto',
        marginRight: 'auto',
        width: '70vw',
    }
}))

function Timeline(props) {

    const [{user},dispatch] = useStateValue()
    const classes = useStyles()
    const [posts, setPosts] = useState([])
    const [isAdmin, setIsAdmin] = AdminStateValue()
    useEffect(() => {
        db.collection('timeline').orderBy('timestamp', 'desc').onSnapshot(snapshot => {
            setPosts(snapshot.docs.map(doc => ({id: doc.id, data: doc.data() })))
        })
    }, [])

    function Poster() {
        if (isAdmin.isAdmin) {
            return <EventPoster />
        }
        return <h3 className = {classes.user}>Timeline</h3>
    }
    return (
        <div className = {classes.root}>
            <div className = {classes.container}>
                <div className = {classes.poster}>
                    <Poster />
                </div>
                <div className = {classes.feed}>
                    {posts.map(post => (
                        <Post
                        key = {post.data.id}
                        profilePic = {post.data.profilePic}
                        message={post.data.message}
                        timestamp={post.data.timestamp}
                        username={post.data.username}
                        image={post.data.image}
                        />
                        ))
                    }
                </div>              
            </div>
        </div>
    )
}

export default Timeline