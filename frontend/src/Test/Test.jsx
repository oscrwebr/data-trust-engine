import api from "../api/axiosConfig.js";
import { useEffect, useState } from "react";
import { setAccessToken, getAccessToken } from "../Auth/authStore.js";

function Test() {
    const name = "This is the test route!"
    const [user, setUser] = useState({});

    
    useEffect(() => {
        api.get("/auth/test")
        .then(res => {
            console.log(res)
            if (res.data.user) {
                setUser(res.data.user);
            }
        })
        .catch(error => console.log("This is the error from 'Test.jsx'" + error))
    }, []);

    return (
        <>
        <h1>{name}</h1>
        <h3>Firstname: {user.firstname}</h3>
        <h3>Surname: {user.surname}</h3>
        <h3>Email: {user.email}</h3>
        </>
    );
    };

export default Test;