import { useState, useEffect } from 'react';

const GetFetch = (url, initialState) => {
  const [data, setData] = useState(initialState);

  function updateData(inputData) {
    let newData = {
      'life': inputData.hasOwnProperty('life') ? inputData.life : data.life,
      'spaces': inputData.hasOwnProperty('spaces') ? inputData.spaces : data.spaces,
      'guesses': inputData.hasOwnProperty('guesses') ? inputData.guesses : data.guesses,
      'alert': inputData.hasOwnProperty('alert') ? inputData.alert : data.alert,
      'token': inputData.hasOwnProperty('token') ? inputData.token : data.token,
      'status': inputData.hasOwnProperty('status') ? inputData.status : data.status,
      'stoken': inputData.hasOwnProperty('stoken') ? inputData.stoken : data.stoken,
    };
    setData(newData);
  }

  async function fetchUrl() {
    const response = await fetch(url);
    const json = await response.json();
    updateData(json);
  }

  useEffect(() => {
    fetchUrl();
  }, []);

  return [data, updateData, fetchUrl];
}

const PostFetch = (url, callback) => {
    
    async function fetchUrl(payload) {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      const json = await response.json();
      callback(json);
    }

    return fetchUrl;
}

export { GetFetch, PostFetch };