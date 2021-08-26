

function fetch_manager(url, args, timeout) {
  return new Promise((resolve, reject) => {
    if (typeof timeout !== 'undefined') {
      setTimeout(() => {
        reject('API call timed out after: ' + (timeout / 1000) + ' sec')
      }, timeout)
    }
    fetch(url, args)
    .then((response) => {
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


function GET(path) {
  return document.config.then((config) => {
    let mode = !!config.api.cors ? 'cors' : 'no-cors';
    return fetch_manager(config.api.url + path, {
      method: 'GET',
      credentials: 'include',
      mode: mode
    }, 10000)
  })
}


function POST(path, payload) {
  return document.config.then((config) => {
    let mode = !!config.api.cors ? 'cors' : 'no-cors';
    return fetch_manager(config.api.url + path, {
      method: 'POST',
      headers: {'Content-Type': 'text/plain'},
      body: JSON.stringify(payload),
      credentials: 'include',
      mode: mode,
    }, 10000)
  })
}


export {GET, POST}
