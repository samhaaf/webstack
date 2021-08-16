

function fetch_manager(url, args, timeout) {
  return new Promise((resolve, reject) => {
    if (typeof timeout !== 'undefined') {
      setTimeout(() => {
        reject('API call timed out after: ' + (timeout / 1000) + ' sec')
      }, timeout)
    }
    fetch(url, args)
    .then((response) => {
     //  for (var pair of response.headers.entries()) {
     //   console.log('header - ' + pair[0]+ ': '+ pair[1]);
     // }
     //  console.log('header - X-custom-header: ' + response.headers.get('X-Custom-header'));

      if (response.ok) {
        try { response.json().then((json) => { resolve(json) }) }
        catch { response.text().then((text) => { resolve(text) })  }
      } else {
        try { response.json().then((json) => { reject(json) })  }
        catch {
          try { response.text().then((text) => { reject(text) }) }
          catch { reject(response) }
        }
      }
    })
    .catch((error) => { reject(error) })
  })
}


function GET(url) {
  return document.config.then((config) => {
    console.log('config', config);
    let mode = !!config.api.cors ? 'cors' : 'no-cors';
    return fetch_manager(url, {
      method: 'GET',
      credentials: 'include',
      mode: mode
    }, 10000)
  })
}


function POST(url, payload) {
  return document.config.then((config) => {
    console.log(config.api);
    let mode = !!config.api.cors ? 'cors' : 'no-cors';
    console.log('mode', mode);
    return fetch_manager(url, {
      method: 'POST',
      headers: {'Content-Type': 'text/plain'},
      body: JSON.stringify(payload),
      credentials: 'include',
      mode: mode,
    }, 10000)
  })
}

export {GET, POST}
