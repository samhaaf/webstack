
<!-- <main use:cssVars={css_vars}> -->
<main>
  {#await document.config}
    loading config..
  {:then config}
    {#await login_check}
      checking login..
    {:then logged_in}
      <div class="content">
        <Router bind:url={url}>
          <Navbar {logged_in}/>
          <div class="route-content">

            <!-- Routes that require being logged in -->
            <AuthRoute {logged_in} path='/'>Home</AuthRoute>
            <!-- <AuthRoute {logged_in} path='/dev/tests'><DevTests/></AuthRoute> -->
            <Route path='/dev/tests'><DevTests/></Route>
            <!-- <AuthRoute {logged_in} path='/dev/tokens'><DevTokens/></AuthRoute> -->
            <Route path='/dev/tokens'><DevTokens/></Route>
            <AuthRoute {logged_in} path='/logout' return-to='/'><AuthLogout/></AuthRoute>

            <!-- Routes that require NOT being logged in -->
            <AuthRoute reversed {logged_in} path="/login" redirect='/'><AuthLogin/></AuthRoute>
            <AuthRoute reversed {logged_in} path="/register" redirect='/'><AuthRegister/></AuthRoute>

            <!-- Routes that do not require authorization -->
            <Route path='*'><h1>404</h1></Route>

          </div>
        </Router>
        <div class='dev-stats'>
          logged in: {logged_in}
        </div>
      </div>
    {/await}
  {:catch error}
    ERROR loading config
  {/await}
</main>


<style>
  .dev-stats {
    position: absolute;
    bottom: 0;
  }
</style>


<script>
  import { Router, Route } from "svelte-routing";
  import Navbar from "./navbar.svelte";
  import AuthLogin from "./auth/login.svelte";
  import AuthLogout from "./auth/logout.svelte";
  import AuthRegister from "./auth/register.svelte";
  import AuthRoute from './auth/route.svelte';
  import DevTests from "./dev/tests.svelte";
  import DevTokens from "./dev/tokens.svelte";
  // import cssVars from 'svelte-css-vars';
  import * as auth from '../utils/auth.js'
  import * as general from '../utils/general.js'

  export let url;

  // let css_vars = {};

  let login_check = auth.check_login()

  function login_callback() {
    console.log('login_callback');
    const url_params = general.get_query_params(window.location.search);
    window.location.replace(url_params['return_url'] || '/')
  }

  function logout_callback() {
    console.log('logout_callback');
    window.location.href = '/login/?return_url=' + encodeURIComponent( window.location.pathname)
  }

  login_check.then(logged_in => {
    if (logged_in) {
      auth.watch_refresh_token(login_callback, logout_callback);
    }
  })


</script>
