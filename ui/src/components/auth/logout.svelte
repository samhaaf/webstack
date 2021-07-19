

<div class='logout-form'>
  <div class='card mx-auto'>
    Are you sure you want to logout?
    <button on:click={() => {logout_and_redirect(false)}}>Logout</button>
    <button on:click={() => {logout_and_redirect(true)}}>Logout of all devices</button>
  </div>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>
  import * as auth from '../../utils/auth.js'
  import { get_query_params } from '../../utils/general.js'

  function logout_and_redirect(everywhere) {
    let logout_method;

    if (everywhere) {
      logout_method = auth.invalidate_all_refresh_tokens;
    } else {
      logout_method = auth.invalidate_refresh_token;
    }

    logout_method().then((success) => {
      auth.check_login().then(() => {
        const url_params = get_query_params(window.location.search);
        if (success) {
          window.location.replace(url_params.return_url || '/login')
        }
      })
    })
  }

</script>
