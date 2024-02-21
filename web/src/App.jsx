import { useEffect, useReducer } from 'react'
import { useLocation, Navigate } from 'react-router-dom'
import MMRPG from './MMRPG'

const getUser = async (dispatch) => {
  const response = await fetch('/get')
  if (response.ok) {
    const user = await response.json()
    dispatch({ type: 'setUser', user: user })
  } else {
    let error = await response.text()
    dispatch({ type: 'setUser', user: { username: false }, error })
  }
}

const getChannels = async (dispatch, guildId) => {
  const response = await fetch(`/channels/${guildId}`)
  if (response.ok) {
    const { channels } = await response.json()
    dispatch({ type: 'setChannels', channels: channels })
  } else {
    let error = await response.text()
    dispatch({ type: 'setChannels', channels: false, error })
  }

}

const reducers = {
  setUser: (state, action) => ({ ...state, ...action.user, error: action.error || false }),
  setChannels: (state, action) => ({ ...state, channels: action.channels, error: action.error || false })
}

const reducer = (state, action) => {
  return reducers[action.type](state, action)
}

const App = () => {
  const location = useLocation();
  const [{ username, guilds, channels, error }, dispatch] = useReducer(reducer, { username: null, error: false, channels: [], guilds: [] })

  useEffect(() => {
    if (username === null) getUser(dispatch)
  }, [username, error])

  if (username === false) return <Navigate to='/login' state={{ from: location }} replace />;
  if (username === null) return <div>Loading...</div>

  return (
    <section className='section'>
      <div className='container'>
        <h1 className='title'>Hello {username}</h1>

        <div className='field'>
          <label className='label'>Server</label>
          <div className='control'>
            <div className='select'>
              <select
                onChange={({ target: { value: guildId } }) => {
                  getChannels(dispatch, guildId)
                }}>
                {guilds.map(guild => <option key={guild.id} value={guild.id}>{guild.name}</option>)}
              </select>
            </div>
          </div>
        </div>

        <div className='field'>
          <label className='label'>Channels</label>
          <div className='control'>
            <div className='select'>
              <select
                onChange={({ target: { value: channelId } }) => {
                  console.log(channelId)
                }}>
                {channels.map(channel => <option key={channel.id} value={channel.id}>{channel.name}</option>)}
              </select>
            </div>
          </div>
        </div>
        <MMRPG />
      </div>
    </section>
  )
}

export default App
