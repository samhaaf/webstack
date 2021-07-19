

<div class='card mx-auto'>
  <button on:click={auth.get_refresh_token}>New refresh token</button>
  <button on:click={auth.check_refresh_token}>Check refresh token</button>
  <button on:click={auth.invalidate_refresh_token}>Invalidate refresh token</button>
  <button on:click={auth.invalidate_all_refresh_tokens}>Invalidate all refresh tokens</button>
  <br>
  <button on:click={auth.get_access_token}>New access token</button>
  <button on:click={auth.check_access_token}>Check access token</button>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>
  import * as auth from '../../utils/auth.js'
</script>
