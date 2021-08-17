

<div class='card mx-auto'>
  <button on:click={auth.get_refresh_token}>New refresh token</button>
  <button on:click={auth.check_refresh_token}>Check refresh token</button>
  <button on:click={auth.invalidate_refresh_token}>Invalidate refresh token</button>
  <button on:click={auth.invalidate_all_refresh_tokens}>Invalidate all refresh tokens</button>
  <br>
  <button on:click={auth.get_access_token}>New access token</button>
  <button on:click={auth.check_access_token}>Check access token</button>
  <br>
  <label for='samesite'>SameSite:</label>
	<select bind:value={SameSite} name="samesite">
    <option value="Strict">Strict</option>
    <option value="Lax">Lax</option>
    <option value="None">None</option>
    <option value="">[empty]</option>
	</select>
  <label for='secure'>Secure:</label>
  <input type='checkbox' bind:checked={Secure} name='secure'>
  <label for='domain'>Domain:</label>
  <input type='text' bind:value={Domain} name='domain'>
  <label for='path'>Path:</label>
  <input type='text' bind:value={Path} name='path'>

  <button on:click={setSimpleCookie}>Set simple cookie</button>
  <button on:click={setServerCookie}>Set server cookie</button>
</div>


<style>
  .card {
    max-width: 300px;
  }
</style>


<script>
  import * as auth from '../../utils/auth.js'
  import {POST} from '../../utils/calls.js'

  let Path = '/';
  let SameSite = '';
  let Secure = false;
  let Domain = '';

  function setSimpleCookie(){
    let cookie = 'simple_key=simple_value'
    if (Path != '') {
      cookie += '; Path=' + Path
    }
    if (Domain != '') {
      cookie += '; Domain=' + Domain
    }
    if (SameSite != '') {
      cookie += '; SameSite=' + SameSite
    }
    if (Secure != false) {
      cookie += '; Secure';
    }
    console.log('setting cookie:', cookie);
    document.cookie = cookie
  }

  function setServerCookie(){
    console.log('server cookie config', {
      path: Path,
      same_site: SameSite,
      secure: Secure,
      domain: Domain
    });
    document.config.then((config) => {
      POST(config.api.url + '/set_cookie', {
        path: Path,
        same_site: SameSite,
        secure: Secure,
        domain: Domain
      })
    })
  }
</script>
