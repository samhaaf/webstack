

<div class='login-form'>
  <div class='card mx-auto'>
    <label for='first_name'>First name:</label>
    <input name='first_name' type='string' value={first_name}>
    <label for='last_name'>Last name:</label>
    <input name='last_name' type='string' value={last_name}>
    <label for='email_address'>Email address:</label>
    <input name='email_address' type='string' value={email_address}>
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

  let first_name = '';
  let last_name = '';
  let email_address = '';
  let username = '';
  let password = '';

  let config = document.config.then((data) => {
    config = data;
    if (config.stage == 'local') {
      first_name = 'John';
      last_name = 'Doe';
      email_address = 'john_doe@example.com';
      username = 'username';
      password = 'password';
    }
  })

  function on_submit(){
    let post_body = {
      first_name: first_name,
      last_name: last_name,
      email_address: email_address,
      username: username,
      password: password
    }
    fetch(config.api.url + '/register', {
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
