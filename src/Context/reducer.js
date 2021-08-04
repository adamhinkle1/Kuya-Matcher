export const initialState = {
    user: null
};

export const initAdminState = {
    isAdmin: false
}
export const actionTypes = {
    SET_USER: "SET_USER",    
    SET_ISADMIN: "SET_ISADMIN",
    SET_Q: "SET_Q",
};

export const initialQuestions = {
    q: {
        big:{},
        little:{}
    }
}
const reducer = (state, action) => {

    switch (action.type) {
        case actionTypes.SET_USER:
            return {
                ...state,
                user: action.user
            };
        case actionTypes.SET_ISADMIN:
            return {
                ...state,
                isAdmin: action.isAdmin
            };
        case actionTypes.SET_Q:
            return {
                ...state,
                q: action.q
            }
        default:
            return state;
    }
};

export default reducer;