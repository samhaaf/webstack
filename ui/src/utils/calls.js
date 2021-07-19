

function handle_response(response) {

}


function fetch_manager(url, args) {
  return new Promise((resolve, reject) => {
    fetch(url, args)
    .then((response) => {
      if (response.ok) {
        try { response.json().then((json) => resolve(json)) }
        catch { response.text().then((text) => { resolve(text) });  }
      } else {
        try { response.json().then((json) => reject(json))  }
        catch { response.text().then((text) => { reject(text) }); }
      }
    })
    .catch((error) => { reject(error) })
  })
}


function GET(url) {
  return fetch_manager(url, {
    method: 'GET',
    credentials: 'include'
  })
}


function POST(url, payload) {
  return fetch_manager(url, {
    method: 'POST',
    headers: {'Content-Type': 'text/plain'},
    body: JSON.stringify(payload),
    credentials: 'include'
  })
}

export {GET, POST}
