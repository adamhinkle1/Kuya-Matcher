import React, {createContext, useContext, useReducer} from 'react'

export const AdminContext = createContext()

export const AdminProvider = ({ reducer, initialState, children }) => (
    <AdminContext.Provider value={useReducer(reducer, initialState)}>
        {children}
    </AdminContext.Provider>
);

export const AdminStateValue = () => useContext(AdminContext);