

<div class='login-form'>
  <div class='card mx-auto'>
    <label for='username'>Username:</label>
    <input name='username' type='string' bind:value={credentials.username}>
    <label for='password'>Password:</label>
    <input name='password' type='password' bind:value={credentials.password}>
    <button on:click={login_and_redirect}>Submit</button>
    <div>Or <a href='/register'>register</a></div>
  </div>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>
  import { do_login } from '../../utils/auth.js'
  import { get_query_params } from '../../utils/general.js'

  let credentials = {
    username: '',
    password: ''
  }

  let config = document.config.then((data) => {
    config = data;
    if (config.stage == 'local') {
      credentials = {
        username: 'test_user',
        password: 'password',
      }
    }
  })

  function login_and_redirect() {
    do_login(credentials).then((success) => {
      console.log('success?', success);
      const url_params = get_query_params(window.location.search);
      if (success) {
        // setTimeout(() => {
          console.log('redirecting...');
          window.location.replace(url_params['return_url'] || '/')
        // }, 3000)
      }
    })
  }

</script>
