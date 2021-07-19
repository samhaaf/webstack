import {GET, POST} from './calls.js'



function get_refresh_token() {
  return document.config.then((config) => {
    return GET(config.api.url + '/new_refresh_token')
    .then((payload) => {
      console.log('refresh token gotten', payload)
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


async function manage_login_session() {
  async function session_worker(){

  }
  config.then(session_worker)
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
  manage_login_session,
}
