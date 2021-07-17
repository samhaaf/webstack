

<div class='card mx-auto'>
  <button on:click={new_refresh_token}>New refresh token</button>
  <button on:click={check_refresh_token}>Check refresh token</button>
  <button on:click={invalidate_refresh_token}>Invalidate refresh token</button>
  <br>
  <button on:click={new_access_token}>New access token</button>
  <button on:click={check_access_token}>Check access token</button>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>

  let config = document.config.then((data) => {
    config = data;
    if (config.stage == 'local') {
      username = 'test_user';
      password = 'password';
    }
  })

  function new_refresh_token(){
    fetch(
      config.api.url + '/new_refresh_token',
      {
        method: 'GET',
        credentials: 'include'
      }
    )
    .then((response) => {
      if (response.ok) {
        try {
          return response.json();
        } catch {
          response.text().then(text => {
            return text;
          })
        }
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { alert(JSON.stringify(response)) })
    .catch((error) => { alert(error) })
  }

  function check_refresh_token(){
    fetch(
      config.api.url + '/check_refresh_token',
      {
        method: 'GET',
        credentials: 'include'
      }
    )
    .then((response) => {
      if (response.ok) {
        try {
          return response.json();
        } catch {
          response.text().then(text => {
            return text;
          })
        }
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { alert(JSON.stringify(response)) })
    .catch((error) => { alert(error) })
  }

  function invalidate_refresh_token(){
    fetch(
      config.api.url + '/invalidate_refresh_token',
      {
        method: 'GET',
        credentials: 'include'
      }
    )
    .then((response) => {
      if (response.ok) {
        try {
          return response.json();
        } catch {
          response.text().then(text => {
            return text;
          })
        }
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { alert(JSON.stringify(response)) })
    .catch((error) => { alert(error) })
  }

  function invalidate_all_refresh_tokens(){
    fetch(
      config.api.url + '/invalidate_all_refresh_tokens',
      {
        method: 'GET',
        credentials: 'include'
      }
    )
    .then((response) => {
      if (response.ok) {
        try {
          return response.json();
        } catch {
          response.text().then(text => {
            return text;
          })
        }
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { alert(JSON.stringify(response)) })
    .catch((error) => { alert(error) })
  }

  function new_access_token(){
    fetch(
      config.api.url + '/new_access_token',
      {
        method: 'GET',
        credentials: 'include'
      }
    )
    .then((response) => {
      if (response.ok) {
        try {
          return response.json();
        } catch {
          response.text().then(text => {
            return text;
          })
        }
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { alert(JSON.stringify(response)) })
    .catch((error) => { alert(error) })
  }

  function check_access_token(){
    fetch(
      config.api.url + '/check_access_token',
      {
        method: 'GET',
        credentials: 'include'
      }
    )
    .then((response) => {
      if (response.ok) {
        try {
          return response.json();
        } catch {
          response.text().then(text => {
            return text;
          })
        }
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { alert(JSON.stringify(response)) })
    .catch((error) => { alert(error) })
  }
</script>
