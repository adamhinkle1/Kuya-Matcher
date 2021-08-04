import React, {createContext, useContext, useReducer} from 'react'

export const QuestionContext = createContext()

export const QuestionProvider = ({ reducer, initialState, children }) => (
    <QuestionContext.Provider value={useReducer(reducer, initialState)}>
        {children}
    </QuestionContext.Provider>
);

export const QuestionStateValue = () => useContext(QuestionContext);