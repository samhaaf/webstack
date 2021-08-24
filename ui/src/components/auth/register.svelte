

<div class='login-form'>
  <div class='card mx-auto'>
    <label for='first_name'>First name:</label>
    <input name='first_name' type='string' bind:value={first_name}>
    <label for='last_name'>Last name:</label>
    <input name='last_name' type='string' bind:value={last_name}>
    <label for='email_address'>Email address:</label>
    <input name='email_address' type='string' bind:value={email_address}>
    <label for='username'>Username:</label>
    <input name='username' type='string' bind:value={username}>
    <label for='password'>Password:</label>
    <input name='password' type='password' bind:value={password}>
    <button on:click={on_submit}>Submit</button>
  </div>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>

  import { register } from '../../utils/auth.js'

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
      username = 'test_user';
      password = 'password';
    }
  })

  function on_submit(){
    register({
      first_name: first_name,
      last_name: last_name,
      email_address: email_address,
      username: username,
      password: password
    })
  }
</script>
