import React, {useState} from 'react'
import './EventPoster.css'
import db from './firebase'
import firebase from 'firebase'

import {useStateValue} from '../Context/StateProvider'

function EventPoster() {

    const [{user},dispatch] = useStateValue()
    const [input, setInput] = useState('')
    const [imageUrl,setImageUrl] = useState('')

    const handleSubmit = e => {
        e.preventDefault()
        db.collection('timeline').add({
            message: input,
            timestamp: firebase.firestore.FieldValue.serverTimestamp(),
            profilePic: user? user.user.picture : '',
            username: user? user.user.name : 'Guest',
            image: imageUrl,
            likes: 0,
        })
        setInput('')
        setImageUrl('')
    }
    return (
        <div className = 'messageSender'>
            <div className='title'>
                <h3>
                    Post an Event
                </h3>
            </div>
            <div className="messageSender_top">
                <form>
                    
                    <input className='messageSender_input' 
                    placeholder={`Comment`}
                    value={input}
                    onChange = {(e) => setInput(e.target.value)}/>
                    <input className='messageSender_img'
                    placeholder='img url' 
                    value={imageUrl}
                    onChange={(e) => setImageUrl(e.target.value)}/>
                    <button onClick={handleSubmit} type='submit'>
                        Hidden Submit
                    </button>
                </form>
            </div>
        </div>
    )
}

export default EventPoster