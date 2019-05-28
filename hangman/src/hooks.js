import { useState, useEffect, useCallback } from 'react';

const GetFetch = (url) => {
    const [data, setData] = useState({});

    async function fetchUrl() {
        const response = await fetch(url);
        const json = await response.json();

        setData(json);
    }

    useEffect(() => {
        fetchUrl();
    }, []);
    return [data, setData];
}

const PostFetch = (url, char, token) => {
    const [res, setRes] = useState({'data': null, 'isLoading': false});

    async function fetchUrl(c, t) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'char': c, 'token': t})
        });
        const json = await response.json();
        console.log(c,t,json);
        setRes(json);
    }

    const cb = useCallback((char, token) => {
        setRes(prevState => ({...prevState, isLoading: true}));
        fetchUrl();
    }, []);
    return [res, cb];
}


export { GetFetch, PostFetch };