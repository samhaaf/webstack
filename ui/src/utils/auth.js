import {GET, POST} from './calls.js'


function validation_alert(token_name, ttl){
  // send a token validation message to other tabs
  localStorage.setItem(token_name + '_ttl', ttl)
  localStorage.setItem(token_name + '_validation_time', Date.now())

  // send a token invalidation maessage to this tab
  window.dispatchEvent(new Event(token_name + '_validation'));
}


function invalidation_alert(token_name){
    // send a token invalidation message to other tabs
    localStorage.setItem(token_name + '_invalidation_time', Date.now());

    // send a token invalidation maessage to this tab
    window.dispatchEvent(new Event(token_name + '_invalidation'));
}


function login(credentials) {
  return POST('/auth/login', credentials)
  .then((payload) => {
    console.log('login successful', payload)
    validation_alert('refresh_token', payload.refresh_token.ttl)
    return payload
  })
  .catch((error) => {
    console.log('failed to login', error)
    return false
  })
}


function register(user_params) {
  return POST('/auth/register', user_params)
  .then((payload) => {
    console.log('register successful', payload)
    validation_alert('refresh_token', payload.refresh_token.ttl)
    return payload
  })
  .catch((error) => {
    console.log('failed to register', error)
    return false
  })
}


function get_refresh_token() {
  return GET('/auth/refresh_token')
  .then((payload) => {
    console.log('refresh token gotten', payload)
    validation_alert('refresh_token', payload.refresh_token.ttl)
    return payload
  })
  .catch((error) => {
    console.log('refresh token get request failed', error)
    if (error['refresh_token_invalidated']) {
      invalidation_alert('refresh_token')
    }
    return false
  })
}


function check_refresh_token() {
  return GET('/auth/refresh_token/check')
  .then((payload) => {
    console.log('refresh token check valid', payload)
    validation_alert('refresh_token', payload.refresh_token.time_left)
    return payload
  })
  .catch((error) => {
    console.log('refresh token check failed', error)
    if (!!error['refresh_token_invalidated']) {
      invalidation_alert('refresh_token')
    }
    return false
  })
}


function invalidate_refresh_token() {
  return GET('/auth/refresh_token/invalidate')
  .then((payload) => {
    console.log('refresh token invalidated', payload)
    invalidation_alert('refresh_token')
    return payload
  })
  .catch((error) => {
    console.log('invalidation of refresh token failed', error)
    if (!!error['refresh_token_invalidated']) {
      invalidation_alert('refresh_token')
    }
    return false
  })
}


function invalidate_all_refresh_tokens() {
  return GET('/auth/refresh_token/invalidate_all')
  .then((payload) => {
    console.log('all refresh tokens invalidated', payload)
    invalidation_alert('refresh_token')
    return payload
  })
  .catch((error) => {
    console.log('invalidation of all refresh tokens failed', error)
    if (!!error['refresh_token_invalidated']) {
      invalidation_alert('refresh_token')
    }
    return false
  })
}


function get_access_token() {
  return GET('/auth/access_token')
  .then((payload) => {
    console.log('access token gotten', payload)
    validation_alert('access_token', payload.access_token.ttl)
    return payload
  })
  .catch((error) => {
    console.log('access token request failed', error)
    if (!!error['refresh_token_invalidated']) {
      invalidation_alert('refresh_token')
    }
    return false
  })
}


function check_access_token() {
  return GET('/auth/access_token/check')
  .then((payload) => {
    console.log('access token check valid', payload)
    validation_alert('access_token', payload.access_token.time_left)
    return payload
  })
  .catch((error) => {
    console.log('access token check failed', error)
    if (!!error['access_token_invalidated']) {
      invalidation_alert('access_token')
    }
    return false
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

  // if (ttl == null) {
  //   throw new Error('Missing refresh_token_validation_time in localStorage')
  // }
  // if (validation_time == null) {
  //   throw new Error('Missing refresh_token_validation_time in localStorate')
  // }

  // check if storage indicates that the token has been invalidated
  let valid_refresh_token = (invalidation_time == null) ? true : (validation_time > invalidation_time)

  // add an event listener to storage to detect an invalidation from another tab
  window.addEventListener('storage', (event) => {
    if (event.key == 'refresh_token_invalidation_time') {
      console.log('refresh-token invalidation detected');
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
      console.log('refresh-token validation detected');
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
    console.log('refresh-token invalidation detected');
    valid_refresh_token = false;
    logout_callback()
  })


  // add an event listener to storage to detect an validation from this tab
  window.addEventListener('refresh_token_validation', () => {
    console.log('refresh-token validation detected');
    valid_refresh_token = true;
    login_callback()
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
    let invalidation_time = localStorage.getItem('access_token_invalidation_time');
    let ttl = localStorage.getItem('access_token_ttl');
    let wait_time = ttl*1000 - (Date.now() - validation_time) - 15000


    // add an event listener to storage to detect an invalidation from another tab
    window.addEventListener('storage', (event) => {
      if (event.key == 'access_token_invalidation_time') {
        console.log('access-token invalidation detected');
        invalidation_time = event.newValue;
        if (invalidation_time > validation_time) {
          if (check_refresh_token()) {
            get_access_token()
          }
        }
      }
    })

    // add an event listener to storage to detect an invalidation from this tab
    window.addEventListener('access_token_invalidation', () => {
      console.log('access-token invalidation detected');
      invalidation_time = event.newValue;
      if (invalidation_time > validation_time) {
        if (check_refresh_token()) {
          get_access_token()
        }
      }
    })


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
  login,
  register,
  check_login,
  watch_refresh_token,
  watch_access_token,
}
