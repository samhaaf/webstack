

<div class='login-form'>
  <div class='card mx-auto'>
    <label for='username'>Username:</label>
    <input name='username' type='string' value={username}>
    <label for='password'>Password:</label>
    <input name='password' type='password' value={password}>
    <button on:click={on_submit}>Submit</button>
  </div>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>

  let username = '';
  let password = '';

  let config = document.config.then((data) => {
    config = data;
    if (config.stage == 'local') {
      username = 'username';
      password = 'password';
    }
  })

  function on_submit(){
    let post_body = {
      username: username,
      password: password
    }
    fetch(config.api.url + '/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(post_body)
    })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        response.text().then(text => {
          throw new Error(text);
        })
      }
    })
    .then((response) => { console.log(response) })
    .catch((error) => { alert(error) })
  }
</script>
