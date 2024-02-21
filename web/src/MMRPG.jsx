import { useState } from 'react'
import D from './D'
import D1 from './D1'
import D2 from './D2'
import D3 from './D3'
import D4 from './D4'
import D5 from './D5'
import D6 from './D6'
import DM from './DM'

const diceMap = {
    1: D1,
    2: D2,
    3: D3,
    4: D4,
    5: D5,
    6: D6,
    m: DM,
    d: D
}

const Dice = ({ values, setValues, size, value = 'd', first = false, last = false }) => (
    <div className={`has-text-centered ml-${first ? '0' : '1'} mr-${last ? '0' : '1'}`} >
        <h4 className='title is-4 mb-0'>{size.toUpperCase()}</h4>
        <div style={{ height: 50 }}>
            <span className='icon is-large'>
                {diceMap[value]()}
            </span>
        </div>
        <EdgeButton values={values} setValues={setValues} size={size} />
    </div >
)

const PoolStat = ({ name, message, first = false, last = false }) => (
    <div className={`ml-${first ? '0' : '1'} mr-${last ? '0' : '1'}`} >
        <h4 className='title is-4 mb-0'>{name}</h4>
        <span className='is-size-6' style={{ lineHeight: '30px' }}>{message}</span>
    </div>
)

const DicePool = ({ values, setValues }) => (
    <div className='box'>
        <div className='content'>
            <h3 className='title is-3'>Dice pool</h3>
        </div>
        <div className='is-flex'>
            <Dice
                values={values}
                setValues={setValues}
                first
                size='d1'
                value={values.d1}
            />
            <Dice
                values={values}
                setValues={setValues}
                size='d2'
                value={values.d2}
            />
            <Dice
                values={values}
                setValues={setValues}
                first
                size='dm'
                value={values.dm}
            />
            {values.trouble > 0 && <PoolStat
                name='Trouble'
                message={values.trouble}
            />}
            {(values.edge.d1 > 0 || values.edge.d2 > 0 || values.edge.dm > 0) && <PoolStat
                name='Edge'
                message={(
                    <div>
                        {values.edge.d1 > 0 && <p><b>D1</b> {values.edge.d1}</p>}
                        {values.edge.d2 > 0 && <p><b>D2</b> {values.edge.d2}</p>}
                        {values.edge.dm > 0 && <p><b>DM</b> {values.edge.dm}</p>}
                    </div>
                )}
            />}
            {(values.target > 0) && <PoolStat
                name='VS Target'
                message={values.target}
            />}
            {(values.ability > 0) && <PoolStat
                last
                name='Ability Modifier'
                message={values.ability}
            />}
        </div>
        <NewRollControls values={values} setValues={setValues} />
        <p>Nice work</p>
    </div>
)

const NewRollControls = ({ values, setValues }) => {
    const [trouble, setTrouble] = useState(0)
    const [ability, setAbility] = useState(0)
    const [target, setTarget] = useState(0)
    return (
        <div>
            <div className='is-flex'>
                <div className='field has-addons mr-3'>
                    <p className='control'>
                        <button className='button is-static'>
                            Trouble
                        </button>
                    </p>
                    <div className='control' style={{ maxWidth: 100 }}>
                        <input
                            value={trouble}
                            className='input'
                            type='number'
                            placeholder='#trouble'
                            min={0}
                            onChange={(evt) => {
                                const { target: { value } } = evt
                                setTrouble(value)
                            }} />
                    </div>
                </div>
                <div className='field has-addons mr-3'>
                    <p className='control'>
                        <button className='button is-static'>
                            Ability modifier
                        </button>
                    </p>
                    <div className='control' style={{ maxWidth: 100 }}>
                        <input
                            className='input'
                            type='number'
                            value={ability}
                            placeholder='#ability'
                            min={0}
                            onChange={(evt) => {
                                const { target: { value } } = evt
                                setAbility(value)
                            }} />
                    </div>
                </div>
                <div className='field has-addons'>
                    <p className='control'>
                        <button className='button is-static'>
                            VS Target
                        </button>
                    </p>
                    <div className='control' style={{ maxWidth: 100 }}>
                        <input
                            className='input'
                            value={target}
                            type='number'
                            placeholder='#target'
                            min={0}
                            onChange={(evt) => {
                                const { target: { value } } = evt
                                setTarget(value)
                            }} />
                    </div>
                </div>
            </div>
            <div className='buttons'>
                <button
                    className='button is-danger'
                    style={{ backgroundColor: '#EC1D24' }}
                    onClick={() => {
                        setValues({
                            ...values,
                            d1: 1,
                            d2: 1,
                            dm: 1,
                            trouble,
                            ability,
                            target,
                            edge: { d1: 0, d2: 0, dm: 0 }
                        })
                        setTrouble(0)
                        setAbility(0)
                        setTarget(0)
                    }}
                >
                    🎲 New roll
                </button>
                <button
                    className='button is-default'
                    onClick={() => {
                        // work out trouble and update history

                        setValues({
                            ...values,
                            trouble,
                            ability,
                            target
                        })
                    }}
                >
                    🆙 Update without rolling
                </button>

            </div>
        </div>
    )
}

const EdgeButton = ({ values, setValues, size }) => {
    return (
        <button
            className='button is-info'
            onClick={() => {
                const value = 0
                const d = values[size]
                if (size === 'dm' && value === 1) setValues({ ...values, [size]: 'm', edge: { ...values.edge, [size]: values.edge[size] + 1 } })
                else if (value > d) setValues({ ...values, [size]: value, edge: { ...values.edge, [size]: values.edge[size] + 1 } })
                else setValues({ ...values, edge: { ...values.edge, [size]: values.edge[size] + 1 } })
            }}
        >
            D{size[1].toUpperCase()} Edge
        </button>
    )
}

const SetDice = ({ values, setValues }) => {
    const [overrides, setOverrides] = useState({ d1: undefined, d2: undefined, dm: undefined })
    return (
        <div className='box'>
            <p>If you have values you want to set, use this</p>
            <div className='is-flex'>
                <div className='field has-addons'>
                    <p className='control'>
                        <button className='button is-static'>
                            D1
                        </button>
                    </p>
                    <div className='control' style={{ width: 65 }}>
                        <input
                            className='input'
                            min={1}
                            max={6}
                            type='number'
                            placeholder='D1'
                            onChange={(evt) => {
                                const { target: { value } } = evt
                                setOverrides({ ...overrides, d1: value })
                            }}
                        />
                    </div>
                    <p className='control'>
                        <button className='button is-static'>
                            D2
                        </button>
                    </p>
                    <div className='control' style={{ width: 65 }}>
                        <input
                            className='input'
                            min={1}
                            max={6}
                            type='number'
                            placeholder='D2'
                            onChange={(evt) => {
                                const { target: { value } } = evt
                                setOverrides({ ...overrides, d2: value })
                            }}
                        />
                    </div>
                    <p className='control'>
                        <button className='button is-static'>
                            DM
                        </button>
                    </p>
                    <div className='control' style={{ width: 65 }}>
                        <input
                            className='input'
                            min={1}
                            max={6}
                            type='number'
                            placeholder='DM'
                            onChange={(evt) => {
                                const { target: { value } } = evt
                                setOverrides({ ...overrides, dm: value })
                            }}
                        />
                    </div>
                </div>
                <button
                    className='button is-info ml-3'
                    onClick={() => {
                        setValues({
                            ...values,
                            d1: overrides.d1,
                            d2: overrides.d2,
                            dm: overrides.dm === '1' ? 'm' : overrides.dm
                        })
                    }}
                >Set values</button>
            </div>
        </div>
    )
}

const History = ({ values }) => {
    return (
        <div className='box'>
            <h3 className='title is-3'>Roll history</h3>
            <ul>
                <li>
                    <h4 className='title is-4'>Rolled Edge on</h4>
                    <p>You did a thing</p>
                </li>
            </ul>
        </div>
    )
}

const MMRPG = () => {
    const [values, setValues] = useState({
        d1: undefined,
        d2: undefined,
        dm: undefined,
        trouble: 0,
        edge: {
            d1: 0,
            d2: 0,
            dm: 0
        },
        target: 0,
        ability: 0,
        history: []
    })
    return (
        <div>
            <div className='content'>
                <h2 className='title is-2'>Marvel Multiverse RPG system</h2>
                <p>This follows the rules for dice rolling with some convinces. This allows the additional rule of stackable edge and trouble.<br />You can find more info here <a href='https://www.marvel.com/rpg'>Marvel Multiverse RPG</a></p>
            </div>
            <DicePool values={values} setValues={setValues} />
            <SetDice values={values} setValues={setValues} />
            <History />
        </div>
    )
}

export default MMRPG