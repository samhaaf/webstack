import {GET, POST} from './calls.js'



function do_login(credentials) {
  return document.config.then((config) => {
    return POST(config.api.url + '/login', credentials)
    .then((payload) => {
      console.log('login successful', payload)
      localStorage.setItem('refresh_token_validation_time', Date.now())
      localStorage.setItem('refresh_token_ttl', payload.ttl)
      return payload
    })
    .catch((error) => {
      console.log('refresh token check failed', error)
      return false
    })
  })
}


function get_refresh_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/new_refresh_token')
    .then((payload) => {
      console.log('refresh token gotten', payload)
      localStorage.setItem('refresh_token_validation_time', Date.now())
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

      // send a token invalidation message to other tabs
      localStorage.setItem('refresh_token_invalidation_time', Date.now());

      // send a token invalidation maessage to this tab
      window.dispatchEvent(new Event('refresh_token_invalidation'));

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

      // send a token invalidation message to other tabs
      localStorage.setItem('refresh_token_invalidation_time', Date.now());

      // send a token invalidation maessage to this tab
      window.dispatchEvent(new Event('refresh_token_invalidation'));

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
    localStorage.setItem('access_token_validation_time', Date.now())
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


async function watch_refresh_token(login_callback, logout_callback) {
  let ttl = localStorage.getItem('refresh_token_ttl');
  let validation_time = localStorage.getItem('refresh_token_validation_time');
  let invalidation_time = localStorage.getItem('refresh_token_invalidation_time');

  if (ttl == null) { throw new Error('Missing refresh_token_validation_time in localStorate') }
  if (validation_time == null) { throw new Error('Missing refresh_token_validation_time in localStorate') }

  // check if storage indicates that the token has been invalidated,
  let valid_refresh_token = (invalidation_time == null) || (validation_time > invalidation_time)

  // add an event listener to storage to detect an invalidation from another tab
  window.addEventListener('storage', (event) => {
    if (event.key == 'refresh_token_invalidation_time') {
      invalidation_time = event.newValue;
      if (invalidation_time > validation_time) {
        valid_refresh_token = false;
        logout_callback()
      }
    }
  })

  // add an event listener to storage to detect a validation from another tab
  window.addEventListener('storage', (event) => {
    if (event.key == 'refresh_token_validation_time') {
      if (!valid_refresh_token) {
        validation_time = event.newValue;
        valid_refresh_token = true
        login_callback()
        _manage_refresh()
      }
    }
  })

  // add an event listener to storage to detect an invalidation from this tab
  window.addEventListener('refresh_token_invalidation', () => {
    valid_refresh_token = false;
    logout_callback()
  })


  async function _manage_refresh() {
    // if there is an valid refresh token, monitor the access token
    // if (valid_refresh_token) {
      watch_access_token()
    // }

    // while the session is active, refresh token
    // while (valid_refresh_token) {
    while (true) {
      ttl = localStorage.getItem('refresh_token_ttl');
      validation_time = localStorage.getItem('refresh_token_validation_time');

      // wait 1 hour or until there are only 15 seconds left, whichever comes first
      let time_alive = (Date.now() - validation_time)
      let wait_time =  Math.max(0, Math.min(3600*1000 - time_alive, ttl*1000 - time_alive - 15000))
      console.log('refresh token watch - waiting for:', wait_time);
      await new Promise(r => setTimeout(r, wait_time))

      // wait a random amount of time so that all open tabs don't try at once
      await new Promise(r => setTimeout(r, Math.random() * 5000))

      // check local storage to make sure no other tab has made the request
      if (localStorage.getItem('refresh_token_validation_time') == validation_time) {

        // update the refresh token
        let success = await get_refresh_token()
        console.log('success', success);

        // in the case of failure, send the logout signal
        if (success) {
          valid_refresh_token = true
        } else {
          valid_refresh_token = false
          logout_callback()
          break
        }
      }
    }
  }

  // go ahead and start watching the refresh tokens
  if (valid_refresh_token) {
    _manage_refresh()
  }
}


async function watch_access_token() {
  while (true) {

    // determine if refresh token is still valid, else break
    let refresh_token_ttl = localStorage.getItem('refresh_token_ttl');
    let refresh_token_validation_time = localStorage.getItem('refresh_token_validation_time');
    let refresh_token_invalidation_time = localStorage.getItem('refresh_token_invalidation_time');
    if (refresh_token_invalidation_time > refresh_token_validation_time) {
      break
    }
    if ((Date.now() - refresh_token_validation_time) > refresh_token_ttl * 1000) {
      break
    }

    let validation_time = localStorage.getItem('access_token_validation_time');
    let ttl = localStorage.getItem('access_token_ttl');
    let wait_time = ttl*1000 - (Date.now() - validation_time) - 15000

    // wait 1 hour or until there are only 15 seconds left, whichever comes first
    console.log('access token watch - waiting for:', wait_time);
    await new Promise(r => setTimeout(r, wait_time))

    // wait a random amount of time so that all open tabs don't try at once
    await new Promise(r => setTimeout(r, Math.random() * 5000))

    // check local storage to make sure no other tab has made the request
    if (localStorage.getItem('access_token_validation_time') == validation_time) {
      // update the access token
      let success = await get_access_token()
      if (!success) {
        break
      }
    }
  }
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
