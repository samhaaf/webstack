

<nav>
  <Link to="/" getProps={getProps('/')} >
    <img src="/static/images/logo.png" class="logo left" alt="3649.design"/>
  </Link>
  <div class='nav-button-container'>
    <!-- <Link getProps={getProps('/spaces')} to="/spaces">
      <div class="nav-button">Spaces</div>
    </Link>
    <Link getProps={getProps('/styles')} to="/styles">
      <div class="nav-button">Styles</div>
    </Link>
    <Link getProps={getProps('/forms')} to="/forms">
      <div class="nav-button">Forms</div>
    </Link>
    <Link getProps={getProps('/gallery')} to="/gallery">
      <div class="nav-button">Gallery</div>
    </Link>
    <Link getProps={getProps('about')} to="/about">
      <div class="nav-button">About</div>
    </Link> -->
    <div class="nav-button dropdown">
      Dev
      <div class="dropdown-content">
        <Link getProps={getProps('tests')} to="/dev/tests"> <p>Tests</p> </Link>
        <Link getProps={getProps('tokens')} to="/dev/tokens"> <p>Tokens</p> </Link>
      </div>
    </div>

    {#if logged_in}
      <Link getProps={getProps('logout')} to="/logout">
        <div class="nav-button">Logout</div>
      </Link>
    {:else}
      <Link getProps={getProps('login')} to="/login">
        <div class="nav-button">Login</div>
      </Link>
    {/if}
  </div>
</nav>


<style>
  nav {
    min-width: 100%;
    /* border: 1px solid; */
    background-color: #9da5b4;
    display: flex;
    flex-direction: row;
    /* height: 80px; */
  }

  .nav-button-container {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: flex-end;
    align-items: center;
    margin-left: auto;
  }

  .nav-button-container :global(a) {
    height: calc(100% - 12px);
    border-style: outset;
    border-width: 0;
  }

  .nav-button-container :global(a.active) {
    height: calc(100% - 12px);
    border-style: inset;
    border-width: 0;
  }

  .nav-button {
    display: flex;
    align-items: center;
    border-width: 2px ;
    border-color: #4b5362;
    border-style: inherit;
    padding: 0 12px 0 12px;
    margin: 0 6px 0 0;
    height: 100%;
    background-color: #9da5b4;
  }

  .nav-button {
    color: #1b1d23;
  }

  .dropdown-content {
    display: none;
    position: absolute;
    padding: 12px 16px;
    text-align: left;
    background-color: #f9f9f9;
    margin-top: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  }

  .dropdown:hover .dropdown-content {
    display: block;
  }

  .logo {
    max-width: 55px;
    margin: 3px;
    background-color: var(--pallete-0-5);
  }
</style>


<script>
  import { Router, Link } from "svelte-routing";
  // import cssVars from './utils/svelte-css-vars';
  import cssVars from 'svelte-css-vars';

  export let logged_in;

  let config = document.config;


  function getProps(to) {

    function inner_fn({ location, href, isPartiallyCurrent, isCurrent }) {
      let props = {
        class: "link-a"
      }

      const isActive = href === to ? isCurrent : isPartiallyCurrent || isCurrent;
      if (isActive) {
        props.class += ' active'
      } else {
        props.class += ' inactive'
      }
      return props;
    }

    return inner_fn
  }

</script>
