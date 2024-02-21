import { useEffect, useState } from 'react'

const getLogin = async (setState) => {
    const response = await fetch('/login_url')
    if (response.ok) {
        const {url} = await response.json()
        setState({url, error: false})
    } else {
        let error = await response.text()
        try {
            error = JSON.parse(error)
        } catch (e) {
            console.log('error', response.status, error)
        }
        console.log('error', response.status, error)
        setState({error})
    }
}

const Login = () => {
    const [{error, url}, setState] = useState({error: false, url: ''})

    useEffect(() => {
        getLogin(setState)
    }, [])

    return (
        <section className='section'>
            <div className='container'>
                <h1 className='title has-text-centered'>Login to Captain Dice</h1>
                <a className={`button is-info is-large ${url === '' && error === false ? 'is-loading is-disabled' : ''}`} href={url}>Login</a>
            </div>
        </section>
    )
}

export default Login