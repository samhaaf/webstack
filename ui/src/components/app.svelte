
<!-- <main use:cssVars={css_vars}> -->
<main>
  {#await document.config}
    <!-- loading config.. -->
  {:then config}
    {#await check_login()}
      <!-- checking login.. -->
    {:then logged_in}
      <div class="content">
        <Router bind:url={url}>
          <!-- <Navbar/> -->
          <div class="route-content">

            <!-- Routes that require being logged in -->
            <AuthRoute {logged_in} path='/dev/tests'><DevTests/></AuthRoute>
            <AuthRoute {logged_in} path='/dev/tokens'><DevTokens/></AuthRoute>
            <AuthRoute {logged_in} path='/logout' return-to='/'><AuthLogout/></AuthRoute>

            <!-- Routes that require NOT being logged in -->
            <AuthRoute reversed {logged_in} path="/login" redirect='/'><AuthLogin/></AuthRoute>
            <AuthRoute reversed {logged_in} path="/register" redirect='/'><AuthRegister/></AuthRoute>

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
  import { Router } from "svelte-routing";
  import Navbar from "./navbar.svelte";
  import AuthLogin from "./auth/login.svelte";
  import AuthLogout from "./auth/logout.svelte";
  import AuthRegister from "./auth/register.svelte";
  import AuthRoute from './auth/route.svelte';
  import DevTests from "./dev/tests.svelte";
  import DevTokens from "./dev/tokens.svelte";
  // import cssVars from 'svelte-css-vars';
  import {check_login, manage_login_session} from '../utils/auth.js'

  export let url;

  // let css_vars = {};


</script>
