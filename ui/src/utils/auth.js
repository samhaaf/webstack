import {GET, POST} from './calls.js'



function get_refresh_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/new_refresh_token')
    .then((payload) => {
      console.log('refresh token gotten', payload)
      localStorage.setItem('refresh_token_last_get', Date.now())
      localStorage.setItem('refresh_token_ttl', payload.ttl)
      return payload
    })
    .catch((error) => {
      console.log('refresh token request failed', error)
      return false
    })
  })
}


function check_refresh_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/check_refresh_token')
    .then((payload) => {
      console.log('refresh token valid', payload)
      return payload
    })
    .catch((error) => {
      console.log('refresh token check failed', error)
      return false
    })
  })
}


function invalidate_refresh_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/invalidate_refresh_token')
    .then((payload) => {
      console.log('refresh token invalidated', payload)
      return payload
    })
    .catch((error) => {
      console.log('invalidation of refresh token failed', error)
      return false
    })
  })
}


function invalidate_all_refresh_tokens() {
  return document.config.then((config) => {
    return GET(config.api.url + '/invalidate_all_refresh_tokens')
    .then((payload) => {
      console.log('all refresh tokens invalidated', payload)
      return payload
    })
    .catch((error) => {
      console.log('invalidation of all refresh tokens failed', error)
      return false
    })
  })
}


function get_access_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/new_access_token')
    .then((payload) => {
    localStorage.setItem('access_token_last_get', Date.now())
    localStorage.setItem('access_token_ttl', payload.ttl)
      console.log('access token gotten', payload)
      return payload
    })
    .catch((error) => {
      console.log('access token request failed', error)
      return false
    })
  })
}


function check_access_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/check_access_token')
    .then((payload) => {
      console.log('access token valid', payload)
      return payload
    })
    .catch((error) => {
      console.log('access token check failed', error)
      return false
    })
  })
}


function do_login(credentials) {
  return document.config.then((config) => {
    return POST(config.api.url + '/login', credentials)
    .then((payload) => {
      console.log('login successful', payload)
      localStorage.setItem('refresh_token_last_get', Date.now())
      localStorage.setItem('refresh_token_ttl', payload.ttl)
      return payload
    })
    .catch((error) => {
      console.log('access token check failed', error)
      return false
    })
  })
}


async function check_login() {
  let refresh_token = await check_refresh_token()
  if (!refresh_token) {
    console.log('Login check:', false);
    return false
  } else {
    console.log('Login check:', true);
    return true
  }
}


async function watch_refresh_token(logout_callback) {
  let valid_refresh_token = true;

  // TODO: localStorage event for invalid refresh token

  while (valid_refresh_token) {
    let last_get = localStorage.getItem('refresh_token_last_get');
    let ttl =  localStorage.getItem('refresh_token_ttl');
    let wait_time =  Math.max(0, Math.min(3600*1000, ttl*1000 - (Date.now() - last_get) - 15000))

    // wait 1 hour or until there are only 15 seconds left, whichever comes first
    console.log('refresh token watch - waiting for:', wait_time);
    await new Promise(r => setTimeout(r, wait_time))

    // wait a random amount of time so that all open tabs don't try at once
    await new Promise(r => setTimeout(r, Math.random() * 5000))

    // check local storage to make sure no other tab has made the request
    if (localStorage.getItem('refresh_token_last_get') == last_get) {
      // update the refresh token
      let success = await get_refresh_token()
      if (!success) {
        break
      }
    }
  }
  logout_callback()
}


async function watch_access_token(logout_callback) {
  let valid_refresh_token = true;

  // TODO: localStorage event for invalid refresh token

  while (valid_refresh_token) {
    let last_get = localStorage.getItem('access_token_last_get');
    let ttl =  localStorage.getItem('access_token_ttl');
    let wait_time =  Math.max(0, Math.min(3600*1000, ttl*1000 - (Date.now() - last_get) - 15000))

    // wait 1 hour or until there are only 15 seconds left, whichever comes first
    console.log('access token watch - waiting for:', wait_time);
    await new Promise(r => setTimeout(r, wait_time))

    // wait a random amount of time so that all open tabs don't try at once
    await new Promise(r => setTimeout(r, Math.random() * 5000))

    // check local storage to make sure no other tab has made the request
    if (localStorage.getItem('access_token_last_get') == last_get) {
      // update the access token
      let success = await get_access_token()
      if (!success) {
        break
      }
    }
  }
  logout_callback()
}




export {
  get_refresh_token,
  check_refresh_token,
  invalidate_refresh_token,
  invalidate_all_refresh_tokens,
  get_access_token,
  check_access_token,
  do_login,
  check_login,
  watch_refresh_token,
  watch_access_token,
}
