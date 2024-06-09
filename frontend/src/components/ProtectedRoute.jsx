import { Navigate } from "react-router-dom"
import { jwtDecode } from "jwt-decode"
import api from "../api"
import { REFRESH_TOKEN, ACCESS_TOKEN } from "../constants"
import { useState, useEffect } from "react"

function ProtectedRoute({children}) {
    const [isAuthorized, setIsAuthorized] = useState(null)

    useEffect(() => {
        auth().catch(() => setIsAuthorized(false));
    }, [])

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);  // get the refresh token
        try {
            // try to send a response to this route with the refresh token which should give us a new access token
            const res = await api.post("/api/token/refresh/", {refresh: refreshToken});
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuthorized(true);
            } else {
                setIsAuthorized(false);
            }
        } catch (error) {
            console.log(error);
            setIsAuthorized(false);
        }
    }

    const auth = async () => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) { 
            setIsAuthorized(false)
            return
        }
        const decoded = jwtDecode(token);  // decode the token and give us access to the value and expiration date
        const tokenExpiration = decoded.exp; 
        const now = Date.now() / 1000;

        if (tokenExpiration < now) {  // checks if token is expired
            await refreshToken();
        } else {
            setIsAuthorized(true);
        }
    };

    if (isAuthorized === null) {
        return <div>Loading...</div>;  // until state of isAuthorized is not null, I'm loading...
    }

    return isAuthorized ? children : <Navigate to="/login" />;  // if authorised, then return children, if not then go to log in route
}

export default ProtectedRoute